import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

FAISS_PATH = "../faiss_index"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = FAISS.load_local(FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

retriever = db.as_retriever(search_kwargs={"k": 3})

SYSTEM_PROMPT = '''
You are a helpful assistant.
Use the context to answer the question in max three sentences.
If you don't know , just say don't know.
Context: {context}
'''

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{input}")
])

qa_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Query(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "RAG API is running!"}

@app.post("/query")
def query_rag(query: Query):
    response = rag_chain.invoke({"input": query.text})
    return {"answer": response.get("answer", "No answer found")}
