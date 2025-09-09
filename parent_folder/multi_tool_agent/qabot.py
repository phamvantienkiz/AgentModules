from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS




vector_db_path = "vectorstores/db_faiss"



# Read tu VectorDB
def read_vectors_db():
    # Embeding
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    db = FAISS.load_local(vector_db_path, embedding_model, allow_dangerous_deserialization=True)
    return db


# Bat dau thu nghiem
db = read_vectors_db()
print("\n ###### DONE #########")
