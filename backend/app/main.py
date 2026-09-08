from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.upload import router as upload_router
from app.api.chat import router as chat_router


app = FastAPI(
    title="Campus Digital Brain API",
    description="AI-powered knowledge assistant for university documents.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    upload_router,
    prefix="/api",
    tags=["Documents"],
)

app.include_router(
    chat_router,
    prefix="/api",
    tags=["Chat"],
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Campus Digital Brain API"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }