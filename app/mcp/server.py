from mcp.server.mcpserver import MCPServer

from app.mcp.knowledge_tools import search_followup_knowledge

mcp = MCPServer("medicare-followup")


@mcp.tool()
def search_followup_knowledge_mcp(
    query: str,
    k: int = 3,
) -> list[dict[str, object]]:
    """Retrieve healthcare follow-up guidance for care coordination."""
    return search_followup_knowledge(query=query, k=k)


def get_mcp_server() -> MCPServer:
    return mcp
