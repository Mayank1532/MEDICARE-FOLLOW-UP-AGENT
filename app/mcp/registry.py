from collections.abc import Callable
from typing import Any

from app.mcp.knowledge_tools import search_followup_knowledge
from app.mcp.server import get_mcp_server

MCP_TOOLS: dict[str, Callable[..., Any]] = {
    "search_followup_knowledge": search_followup_knowledge,
}


def get_mcp_tool(name: str) -> Callable[..., Any]:
    if name not in MCP_TOOLS:
        raise KeyError(f"MCP tool not found: {name}")

    return MCP_TOOLS[name]


def list_mcp_tools() -> list[str]:
    return sorted(MCP_TOOLS)


def get_mcp_server_instance() -> Any:
    return get_mcp_server()
