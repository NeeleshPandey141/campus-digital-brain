import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "gemini-2.5-flash",
    )

    CHROMA_DB_PATH = os.getenv(
        "CHROMA_DB_PATH",
        "chroma_db",
    )

    UPLOAD_DIR = os.getenv(
        "UPLOAD_DIR",
        "uploads",
    )


settings = Settings()