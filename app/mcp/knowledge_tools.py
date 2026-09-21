from pathlib import Path

from app.rag.embeddings import get_embeddings
from app.rag.retriever import KnowledgeRetriever

KNOWLEDGE_DIR = Path("knowledge")
VECTORSTORE_DIR = Path("knowledge/.chroma")


def get_knowledge_retriever() -> KnowledgeRetriever:
    return KnowledgeRetriever(
        knowledge_dir=KNOWLEDGE_DIR,
        embedding_function=get_embeddings(),
        persist_directory=VECTORSTORE_DIR,
    )


def search_followup_knowledge(
    query: str,
    k: int = 3,
) -> list[dict[str, object]]:
    """MCP-facing tool for retrieving follow-up guidance."""

    retriever = get_knowledge_retriever()
    documents = retriever.retrieve(query, k=k)

    return [
        {
            "content": document.page_content,
            "source": document.metadata.get("source", "unknown"),
        }
        for document in documents
    ]
