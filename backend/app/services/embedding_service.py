from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import settings


class EmbeddingService:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in .env")

        self.model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=settings.GEMINI_API_KEY,
        )

    def embed_documents(self, texts: list[str]):
        return self.model.embed_documents(texts)

    def embed_query(self, query: str):
        return self.model.embed_query(query)