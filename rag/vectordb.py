from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

def get_vectorstore():
    embeddings = OpenAIEmbeddings(model='text-embedding-3-large')
    return Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )