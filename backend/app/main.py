from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.upload import router as upload_router
from app.api.chat import router as chat_router


app = FastAPI(
    title="Campus Digital Brain API"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://campus-digital-brain.vercel.app",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API routes
app.include_router(
    upload_router,
    prefix="/api",
)

app.include_router(
    chat_router,
    prefix="/api",
)


@app.get("/")
def root():
    return {
        "message": "Campus Digital Brain API is running"
    }