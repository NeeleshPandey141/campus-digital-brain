from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma

from app.config import settings
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService


class RAGService:

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.vectorstore = Chroma(
            persist_directory=settings.CHROMA_DB_PATH,
            embedding_function=self.embedding_service.model,
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )


    def clear_database(self):
        """
        Clear all existing documents from ChromaDB.
        Used because Version 1 supports one PDF at a time.
        """

        print("Clearing previous document knowledge...")

        self.vectorstore.delete_collection()

        self.vectorstore = Chroma(
            persist_directory=settings.CHROMA_DB_PATH,
            embedding_function=self.embedding_service.model,
        )

        print("Previous knowledge cleared.")


    def ingest_pdf(
        self,
        pdf_path: str,
        original_filename: str | None = None,
    ):

        stored_filename = Path(pdf_path).name

        file_name = (
            original_filename
            if original_filename
            else stored_filename
        )

        print(f"\nProcessing PDF: {file_name}")

        # Clear previous PDF knowledge
        self.clear_database()

        # Extract PDF pages
        document_service = DocumentService()

        pages = document_service.extract_pages(
            pdf_path
        )

        # Convert pages into LangChain documents
        documents = []

        for page_data in pages:

            text = page_data["text"]

            if not text:
                continue

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": file_name,
                        "page": page_data["page"],
                        "extraction_type": page_data[
                            "extraction_type"
                        ],
                    },
                )
            )

        # Split documents into chunks
        chunks = self.splitter.split_documents(
            documents
        )

        # Store chunks in ChromaDB
        if chunks:

            self.vectorstore.add_documents(
                chunks
            )

        print(f"Created {len(chunks)} chunks.")

        return len(chunks)


    def retrieve(
        self,
        query: str,
        k: int = 6,
    ):

        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": k,
            },
        )

        return retriever.invoke(query)