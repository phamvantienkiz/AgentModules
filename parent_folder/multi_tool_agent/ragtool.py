from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# define variable
vector_db_path = "vectorstores/db_faiss"

class RAGScienceTool:
    def __init__(self, db_path: str="vectorstores/db_faiss"):
        self.embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        self.vector_db = FAISS.load_local(db_path, self.embedding_model, allow_dangerous_deserialization=True)

    def research_papers(self, query: str) -> str:
        """Tìm kiếm thông tin từ các bài báo khoa học về Fall Detection"""
        documents = self.vector_db.similarity_search(query=query, k=3)
        return "\n\n".join([doc.page_content for doc in documents])


