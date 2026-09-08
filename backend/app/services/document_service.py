import pymupdf


class DocumentService:

    def extract_pages(self, pdf_path: str) -> list[dict]:
        """
        Extract digital text from a PDF page by page.

        Version 1 supports normal text-based PDFs.
        """

        pdf = pymupdf.open(pdf_path)

        pages = []

        try:
            for page_number, page in enumerate(pdf, start=1):

                text = page.get_text().strip()

                if not text:
                    continue

                print(
                    f"Page {page_number}: "
                    "Using digital text extraction"
                )

                pages.append(
                    {
                        "page": page_number,
                        "text": text,
                        "extraction_type": "text",
                    }
                )

        finally:
            pdf.close()

        return pages