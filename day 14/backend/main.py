import os
import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# RAG Imports
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

# Load .env file from the parent directory
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


# --- RAG Setup ---
FAISS_PATH = "../faiss_index/"

print("Loading embeddings...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("Loading FAISS index...")
db = FAISS.load_local(FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

retriever = db.as_retriever(search_kwargs={"k": 3})

SYSTEM_PROMPT = '''
You are a helpful assistant.
Use the context to answer the question in max three sentences.
If you don't know , just say don't know.
Context: {context}
Chat History: {chat_history}
'''

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ]
)

qa_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)

print("RAG chain created.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
def get_db_conn():
    conn = psycopg2.connect(DB_URL)
    return conn


class QueryRequest(BaseModel):
    user_id: int
    text: str


class HistoryRequest(BaseModel):
    user_id: int


class UserRequest(BaseModel):
    username: str

#api endpoint

#login/signup

@app.post("/get_or_create_user")
def get_or_create_user(req: UserRequest):
    conn = get_db_conn()
    cur = conn.cursor()
    
    # 1. Try to find the user
    cur.execute("SELECT id FROM users WHERE username = %s", (req.username,))
    user_row = cur.fetchone() #(1,)

    
    if user_row:
        user_id = user_row[0] #1
    else:
        # 2. If not found, create them
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (req.username,))
        conn.commit()
        user_id = cur.fetchone()[0] #2
        
    cur.close()
    conn.close()
    return {"user_id": user_id, "username": req.username}

#chat history

@app.post("/get_history")
def get_history(req:HistoryRequest):
    conn = get_db_conn()
    cur = conn.cursor()
    
    cur.execute("SELECT prompt, answer FROM chat_history WHERE user_id = %s ORDER BY id ASC", (req.user_id,))
    history = cur.fetchall() #[("hi","hello how i can help you"),("hi","hello how i can help you")]
    
    cur.close()
    conn.close()
    
    # Format for frontend
    formatted_history = []
    for p, a in history:
        formatted_history.append({"role": "human", "content": p})
        formatted_history.append({"role": "ai", "content": a})

    #[{"role": "human", "content": "hi"}, {"role": "ai", "content": "hello how i can help you"}, {"role": "human", "content": "hi"}, {"role": "ai", "content": "hello how i can help you"}]
    return {"history": formatted_history}

@app.post("/query")
def query_rag(req: QueryRequest):
    conn=get_db_conn()
    cur=conn.cursor()
    cur.execute("SELECT prompt, answer FROM chat_history WHERE user_id = %s ORDER BY id ASC", (req.user_id,))
    db_history = cur.fetchall() #[("hi","hello how i can help you"),("what is web scraping","Web scraping is extraction of data ...")]
    
    chat_history_messages = []
    for prompt, answer in db_history:
        chat_history_messages.append(HumanMessage(content=prompt))
        chat_history_messages.append(AIMessage(content=answer))
    
    response = rag_chain.invoke({
        "input": req.text,
        "chat_history": chat_history_messages
    })
    answer = response.get("answer", "No answer found.")
    
    # Save new Q&A to database
    cur.execute("INSERT INTO chat_history (user_id, prompt, answer) VALUES (%s, %s, %s)", (req.user_id, req.text, answer))
    conn.commit()  
    cur.close()
    conn.close()

    return {"answer": answer}
@app.get("/")
def read_root():
    return {"message": "welcome to fastapi.go to /docs to get started"}
