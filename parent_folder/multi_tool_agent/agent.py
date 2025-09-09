import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

class RAGScienceTool:
    def __init__(self, db_path):
        self.embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        self.vector_db = FAISS.load_local(db_path, self.embedding_model, allow_dangerous_deserialization=True)

    def research_papers(self, query: str) -> str:
        """Tìm kiếm thông tin từ các bài báo khoa học về Fall Detection"""
        documents = self.vector_db.similarity_search(query=query, k=3)
        return "\n\n".join([doc.page_content for doc in documents])

rag_tool = RAGScienceTool(db_path="vectorstores/db_faiss")

def get_weather(city: str) -> dict:
    """Retrieve the current weather report for a specified city.
    
    Args:
        city (str): The name of the city for which to get the weather report.
        
    Returns:
        dict: status and result or error message.
    """
    if city.lower() == "ho chi minh":
        return {
            "status": "success",
            "result": {
                "temperature": 30,
                "condition": "Sunny",
                "report": ("The weather in New York is sunny with a temperature of 25 degrees"
                        " Celsius (41 degrees Fahrenheit)."
                ),
            }
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }
    
def get_current_time(city: str) -> dict:
    """Retrieve the current time in a specified city.
    
    Args:
        city (str): The name of the city for which to get the current time.
        
    Returns:
        dict: status and result or error message.
    """
    if city.lower() == "ho chi minh":
        tz_identifier = "Asia/Ho_Chi_Minh"
    else: 
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }
    
    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f"The current time in {city} is {now.strftime('%Y-%m-%d %H:%M:%S')}."
    )
    return {"status": "success", "result": report}


# RAG Tool
def research_fall_detection(query: str) -> str:
    """Tìm kiếm thông tin từ các bài báo về Fall Detection"""
    
    return rag_tool.research_papers(query=query)


root_agent = Agent(
    name="fall_detection_research_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent nghiên cứu về Fall Detection kết hợp thông tin thời tiết và thời gian"
    ),
    instruction=(
        "Bạn là trợ lý nghiên cứu thông minh. Sử dụng các công cụ sau:\n"
        "- get_weather: Cho thông tin thời tiết\n"
        "- get_current_time: Cho thông tin thời gian\n"
        "- research_fall_detection: Truy xuất thông tin từ các bài báo khoa học\n\n"
        "Luôn ưu tiên sử dụng research_fall_detection khi câu hỏi liên quan đến Fall Detection"
    ),
    tools=[get_weather, get_current_time, research_fall_detection],
)