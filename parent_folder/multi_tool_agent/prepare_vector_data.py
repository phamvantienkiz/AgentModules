from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
# Define variable
pdf_data_path = "data"
vector_db_path = "vectorstores/db_faiss"

def create_db_from_files():
    # Load folder
    loader = DirectoryLoader(pdf_data_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents=documents)

    # Embedding
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    # embedding_model = VertexAIEmbeddings(model_name="text-embedding-004")
    db = FAISS.from_documents(chunks, embedding_model)

    # save local
    db.save_local(vector_db_path)
    return db

create_db_from_files()