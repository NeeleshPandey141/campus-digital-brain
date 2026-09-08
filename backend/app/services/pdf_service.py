from pathlib import Path

from pypdf import PdfReader


class PDFService:
    @staticmethod
    def extract_pages(file_path: str) -> list[dict]:
        """
        Extract text page by page from a PDF.

        Returns:
            [
                {
                    "page": 1,
                    "text": "..."
                }
            ]
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {file_path}")

        reader = PdfReader(path)

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            pages.append(
                {
                    "page": page_number,
                    "text": text.strip(),
                }
            )

        return pages

    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extract all text from a PDF.
        """

        pages = PDFService.extract_pages(file_path)

        return "\n".join(
            page["text"]
            for page in pages
            if page["text"]
        ).strip()