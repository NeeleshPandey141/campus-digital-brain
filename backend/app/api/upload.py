from pathlib import Path
import shutil
import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import settings
from app.services.rag_service import RAGService


router = APIRouter()


UPLOAD_DIR = Path(settings.UPLOAD_DIR)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    # Validate file exists
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided.",
        )

    # Validate PDF
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    # Create unique filename
    file_id = uuid.uuid4()

    safe_filename = (
        f"{file_id}_{file.filename}"
    )

    file_path = (
        UPLOAD_DIR / safe_filename
    )

    try:

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        # Process PDF
        rag = RAGService()

        chunks = rag.ingest_pdf(
            pdf_path=str(file_path),
            original_filename=file.filename,
        )

        # Detect empty / unreadable PDF
        if chunks == 0:
            if file_path.exists():
                file_path.unlink()

            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text was found in this PDF. "
                    "Please upload a digital text-based PDF."
                ),
            )

        return {
            "message": "PDF uploaded and processed successfully.",
            "filename": file.filename,
            "chunks": chunks,
        }

    except HTTPException:
        raise

    except Exception as error:

        print(
            f"PDF processing error: {error}"
        )

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to process this PDF. "
                "Please make sure it is a valid PDF and try again."
            ),
        )

    finally:
        await file.close()