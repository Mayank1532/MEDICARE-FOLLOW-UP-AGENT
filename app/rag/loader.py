from pathlib import Path

from langchain_core.documents import Document


class KnowledgeDocumentLoader:
    """Loads healthcare follow-up guidance documents."""

    def __init__(self, knowledge_dir: Path) -> None:
        self.knowledge_dir = knowledge_dir

    def load_documents(self) -> list[Document]:
        documents: list[Document] = []

        for path in sorted(self.knowledge_dir.glob("*.md")):
            content = path.read_text(encoding="utf-8")

            documents.append(
                Document(
                    page_content=content,
                    metadata={
                        "source": path.name,
                        "document_type": "follow_up_guideline",
                    },
                )
            )

        return documents
