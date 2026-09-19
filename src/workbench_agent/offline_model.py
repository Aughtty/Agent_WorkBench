"""无需 API Key 的确定性模型替身，仅用于演示和自动测试。"""

from __future__ import annotations

import json
from typing import Any

from .contracts import ModelTurn, ToolCall


class OfflineDemoModel:
    """根据输入生成 Tool Call，验证协议和循环，不宣称具备 LLM 推理能力。"""

    def complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> ModelTurn:
        last = messages[-1]
        if last["role"] == "tool":
            observations = [json.loads(item["content"]) for item in messages if item["role"] == "tool"]
            user_text = next(item["content"] for item in reversed(messages) if item["role"] == "user")
            called = [item["tool_call_id"] for item in messages if item["role"] == "tool"]
            if "记录" in user_text and not any("todo" in call_id for call_id in called):
                return ModelTurn(tool_calls=[ToolCall("add_todo", {"title": "复习 Agent Memory"}, "todo-1")])
            return ModelTurn(content=f"任务已完成。工具返回：{json.dumps(observations, ensure_ascii=False)}")

        text = last["content"]
        if "列出" in text and "待办" in text:
            return ModelTurn(tool_calls=[ToolCall("list_todos", {}, "list-todo-1")])
        if "文件" in text:
            keyword = text.split("文件", 1)[0].split()[-1] if text.split("文件", 1)[0].split() else "py"
            return ModelTurn(tool_calls=[ToolCall("find_files", {"keyword": keyword}, "file-1")])
        if "知识库" in text or "Agent" in text or "Memory" in text:
            return ModelTurn(tool_calls=[ToolCall("search_knowledge", {"query": text, "top_k": 2}, "kb-1")])
        return ModelTurn(content="离线演示模型无法判断该任务；请接入真实 LLM 模型。")

