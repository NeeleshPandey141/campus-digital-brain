from pathlib import Path

import pytesseract
from pdf2image import convert_from_path


class OCRService:

    @staticmethod
    def extract_pages(pdf_path: str) -> list[dict]:
        """
        Convert PDF pages to images and extract text using OCR.
        """

        path = Path(pdf_path)

        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        images = convert_from_path(path)

        pages = []

        for page_number, image in enumerate(images, start=1):

            text = pytesseract.image_to_string(
                image,
                lang="eng",
            )

            pages.append(
                {
                    "page": page_number,
                    "text": text.strip(),
                }
            )

        return pages

    @staticmethod
    def extract_text(pdf_path: str) -> str:

        pages = OCRService.extract_pages(pdf_path)

        return "\n".join(
            page["text"]
            for page in pages
            if page["text"]
        ).strip()