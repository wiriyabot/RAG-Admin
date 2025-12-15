from rag.loader import load_docs
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

docs = load_docs()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=100
)
splits = splitter.split_documents(docs)

embeddings = OpenAIEmbeddings(model='text-embedding-3-large')

vectordb = Chroma.from_documents(
    documents=splits, 
    embedding=embeddings,
    persist_directory="./chroma_db" 
)
