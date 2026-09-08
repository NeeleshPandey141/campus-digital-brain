import pymupdf


class DocumentService:

    def extract_pages(self, pdf_path: str):

        document = pymupdf.open(pdf_path)

        pages = []

        for page_number, page in enumerate(document, start=1):

            text = page.get_text().strip()

            if text:
                print(
                    f"Page {page_number}: Using digital text extraction"
                )

                pages.append(
                    {
                        "page": page_number,
                        "text": text,
                        "extraction_type": "digital",
                    }
                )

        document.close()

        return pages