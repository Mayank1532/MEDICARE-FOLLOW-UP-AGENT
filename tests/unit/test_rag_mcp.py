from pathlib import Path

from langchain_core.documents import Document

from app.mcp.registry import (
    get_mcp_server_instance,
    get_mcp_tool,
    list_mcp_tools,
)
from app.rag.loader import KnowledgeDocumentLoader

KNOWLEDGE_PATH = Path("knowledge")


def test_knowledge_loader() -> None:
    loader = KnowledgeDocumentLoader(KNOWLEDGE_PATH)

    documents = loader.load_documents()

    assert len(documents) >= 1
    assert "Follow-Up Prioritization" in documents[0].page_content
    assert documents[0].metadata["document_type"] == "follow_up_guideline"


def test_mcp_tool_registry() -> None:
    tools = list_mcp_tools()

    assert "search_followup_knowledge" in tools
    assert get_mcp_tool("search_followup_knowledge") is not None


def test_knowledge_tool_can_be_mocked(monkeypatch) -> None:
    class FakeRetriever:
        def retrieve(
            self,
            query: str,
            k: int = 3,
        ) -> list[Document]:
            assert "follow-up" in query
            assert k == 2

            return [
                Document(
                    page_content="Follow-up guidance for human review.",
                    metadata={"source": "test.md"},
                )
            ]

    monkeypatch.setattr(
        "app.mcp.knowledge_tools.get_knowledge_retriever",
        lambda: FakeRetriever(),
    )

    tool = get_mcp_tool("search_followup_knowledge")
    result = tool("follow-up patient", k=2)

    assert result[0]["content"] == "Follow-up guidance for human review."
    assert result[0]["source"] == "test.md"


def test_mcp_server_instance() -> None:
    server = get_mcp_server_instance()

    assert server is not None
    assert server.name == "medicare-followup"
