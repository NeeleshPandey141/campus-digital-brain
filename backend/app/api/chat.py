from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.chat_service import ChatService


router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
async def chat(request: ChatRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        service = ChatService()

        return service.ask(question)

    except Exception as error:

        error_message = str(error).lower()

        if (
            "resource_exhausted" in error_message
            or "quota" in error_message
            or "429" in error_message
        ):
            raise HTTPException(
                status_code=429,
                detail=(
                    "AI service quota is temporarily exhausted. "
                    "Please try again later."
                ),
            )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to generate an AI response right now. "
                "Please try again later."
            ),
        )