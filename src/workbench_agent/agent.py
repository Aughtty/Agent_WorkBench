"""不依赖 Agent 框架的 Tool Calling 主循环。"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .contracts import ModelClient
from .memory import MemoryStore
from .tools import ToolRegistry, tool_result_message
from .prompts import SYSTEM_PROMPT


@dataclass(frozen=True)
class AgentResult:
    answer: str
    steps: int
    trace: list[dict[str, Any]]


class Agent:
    """执行“模型决策 → 工具执行 → Observation → 再决策”的循环。

    框架通常会隐藏这段逻辑。本项目把它显式写出，便于解释 Tool Schema、
    call_id、失败回传和最大步数保护分别解决什么问题。
    """

    def __init__(
        self,
        model: ModelClient,
        registry: ToolRegistry,
        memory: MemoryStore,
        log_path: Path,
        max_steps: int = 6,
        system_prompt: str = SYSTEM_PROMPT,
    ) -> None:
        self.model = model
        self.registry = registry
        self.memory = memory
        self.log_path = log_path
        self.max_steps = max_steps
        self.system_prompt = system_prompt
        log_path.parent.mkdir(parents=True, exist_ok=True)

    def run(self, user_input: str, session_id: str = "default") -> AgentResult:
        if not user_input.strip():
            raise ValueError("用户输入不能为空")

        messages = [{"role": "system", "content": self.system_prompt}, *self.memory.recent(session_id)]
        user_message = {"role": "user", "content": user_input.strip()}
        messages.append(user_message)
        self.memory.append(session_id, user_message)
        trace: list[dict[str, Any]] = []

        for step in range(1, self.max_steps + 1):
            model_started = time.perf_counter()
            turn = self.model.complete(messages, self.registry.schemas())
            model_ms = round((time.perf_counter() - model_started) * 1000, 2)
            if not turn.tool_calls:
                answer = turn.content.strip() or "模型未返回有效答案。"
                assistant_message = {"role": "assistant", "content": answer}
                self.memory.append(session_id, assistant_message)
                trace.append({
                    "step": step, "type": "final_answer", "model_ms": model_ms,
                    "model": turn.model, "usage": turn.usage,
                })
                self._write_trace(session_id, user_input, trace, answer)
                return AgentResult(answer=answer, steps=step, trace=trace)

            assistant_tool_message = {
                "role": "assistant",
                "content": turn.content,
                "tool_calls": [
                    {"id": call.call_id, "type": "function", "function": {
                        "name": call.name,
                        "arguments": json.dumps(call.arguments, ensure_ascii=False),
                    }} for call in turn.tool_calls
                ],
            }
            messages.append(assistant_tool_message)

            for call in turn.tool_calls:
                tool_started = time.perf_counter()
                result = self.registry.execute(call.name, call.arguments)
                tool_ms = round((time.perf_counter() - tool_started) * 1000, 2)
                observation = {
                    "step": step,
                    "type": "tool_call",
                    "model_ms": model_ms,
                    "model": turn.model,
                    "usage": turn.usage,
                    "tool_ms": tool_ms,
                    "tool": call.name,
                    "arguments": call.arguments,
                    "result": result,
                }
                trace.append(observation)
                messages.append(tool_result_message(call.call_id, result))

        answer = f"任务在 {self.max_steps} 步后仍未完成，已停止以避免无限工具循环。"
        self._write_trace(session_id, user_input, trace, answer)
        return AgentResult(answer=answer, steps=self.max_steps, trace=trace)

    def _write_trace(self, session_id: str, user_input: str, trace: list[dict[str, Any]], answer: str) -> None:
        record = {"session_id": session_id, "input": user_input, "trace": trace, "answer": answer}
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
