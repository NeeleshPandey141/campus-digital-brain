from google import genai

from app.config import settings
from app.services.rag_service import RAGService


class ChatService:

    def __init__(self):

        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found in .env"
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.rag = RAGService()


    def ask(self, question: str):

        # Retrieve relevant chunks
        documents = self.rag.retrieve(question)

        # No documents found
        if not documents:
            return {
                "answer": (
                    "I couldn't find that information "
                    "in the uploaded document."
                ),
                "sources": [],
            }

        # Build context for Gemini
        context_parts = []

        for index, doc in enumerate(
            documents,
            start=1,
        ):

            source = doc.metadata.get(
                "source",
                "Unknown document",
            )

            page = doc.metadata.get(
                "page",
                "Unknown page",
            )

            context_parts.append(
                f"""
SOURCE {index}

Document: {source}
Page: {page}

Content:
{doc.page_content}
"""
            )

        context = "\n\n".join(context_parts)

        # Prompt Gemini
        prompt = f"""
You are Campus Digital Brain, an AI assistant for university students.

Answer the student's question using ONLY the provided context.

Rules:

1. Do not use outside knowledge.
2. Give a clear and concise answer.
3. If the answer is not available in the context, say exactly:

I couldn't find that information in the uploaded document.

Context:

{context}

Question:

{question}
"""

        try:

            response = self.client.models.generate_content(
                model=settings.MODEL_NAME,
                contents=prompt,
            )

            answer = response.text.strip()

        except Exception as error:

            raise RuntimeError(
                f"Gemini generation failed: {str(error)}"
            )

        # Create unique sources
        sources = []
        seen = set()

        for doc in documents:

            source = doc.metadata.get(
                "source",
                "Unknown document",
            )

            page = doc.metadata.get(
                "page",
                "Unknown",
            )

            key = (
                source,
                page,
            )

            if key not in seen:

                seen.add(key)

                sources.append(
                    {
                        "document": source,
                        "page": page,
                    }
                )

        return {
            "answer": answer,
            "sources": sources,
        }