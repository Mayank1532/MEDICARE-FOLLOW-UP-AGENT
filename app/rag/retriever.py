from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


class KnowledgeRetriever:
    """Retrieves relevant follow-up guidance from the knowledge base."""

    def __init__(
        self,
        knowledge_dir: Path,
        embedding_function: Embeddings,
        persist_directory: Path,
    ) -> None:
        self.knowledge_dir = knowledge_dir
        self.embedding_function = embedding_function
        self.persist_directory = persist_directory

        self.vector_store: Chroma | None = None

    def build(self) -> None:
        from app.rag.loader import KnowledgeDocumentLoader

        documents = KnowledgeDocumentLoader(
            self.knowledge_dir
        ).load_documents()

        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embedding_function,
            persist_directory=str(self.persist_directory),
        )

    def retrieve(
        self,
        query: str,
        k: int = 3,
    ) -> list[Document]:
        if self.vector_store is None:
            self.build()

        if self.vector_store is None:
            return []

        return self.vector_store.similarity_search(query, k=k)
