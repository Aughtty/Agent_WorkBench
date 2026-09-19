"""Agent、模型适配器和工具之间共享的数据契约。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class ToolCall:
    """模型请求执行一次工具调用。

    name 对应注册工具名，arguments 必须符合该工具的 JSON Schema。
    call_id 用来把执行结果准确地回传给模型。
    """

    name: str
    arguments: dict[str, Any]
    call_id: str


@dataclass(frozen=True)
class ModelTurn:
    """模型一轮输出：要么给最终文本，要么给一个或多个 Tool Call。"""

    content: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    usage: dict[str, Any] = field(default_factory=dict)
    model: str = ""


class ModelClient(Protocol):
    """模型适配器协议，让 Agent 主循环与具体厂商 SDK 解耦。"""

    def complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> ModelTurn:
        ...
