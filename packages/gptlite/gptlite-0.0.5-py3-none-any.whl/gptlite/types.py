import sys
from typing import Any, Callable, List, Literal

if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

# from langchain_core.tools import BaseTool as LangchainBaseTool

__all__ = ["BaseTool", "Message", "ToolResult"]

BaseTool = Any
# BaseTool = LangchainBaseTool


class Message(TypedDict, total=False):
    role: str
    content: str
    tool_call_id: str
    tool_calls: List[dict]


class FileInfo(TypedDict):
    id: str
    bytes: int
    filename: str
    purpose: str
    created_at: float


class ToolResult(TypedDict):
    type: Literal["string", "json", "bytes"]
    data: Any


class OnFcMethods(TypedDict, total=False):
    meta: Callable[[dict], None]
    params: Callable[[str], None]
    result: Callable[[str], None]
