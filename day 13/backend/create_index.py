#read files
#break in chunks
#embeddings 
#store in vector store -> FAISS

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


DATA_PATH="../knowledge_base"
FAISS_PATH="../faiss_index"

print("Loading text files ...")

txt_loader=DirectoryLoader(DATA_PATH,glob="**/*.txt",loader_cls=TextLoader,loader_kwargs={"encoding":"utf-8"})

txt_docs=txt_loader.load()

pdf_loader=DirectoryLoader(DATA_PATH,glob="**/*.pdf",loader_cls=PyPDFLoader)

pdf_docs=pdf_loader.load()

docs=txt_docs+pdf_docs

text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=150)

docs=text_splitter.split_documents(docs)

print("Creating embeddings (this may take a moment)...")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = FAISS.from_documents(docs, embeddings)

db.save_local(FAISS_PATH)

print("Embeddings created and saved successfully!")