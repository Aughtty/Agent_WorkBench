from pathlib import Path

from workbench_agent.agent import Agent
from workbench_agent.contracts import ModelTurn, ToolCall
from workbench_agent.memory import MemoryStore
from workbench_agent.tools import Tool, ToolRegistry


class ScriptedModel:
    def __init__(self) -> None:
        self.calls = 0

    def complete(self, messages, tools):
        self.calls += 1
        if self.calls == 1:
            return ModelTurn(tool_calls=[ToolCall("echo", {"text": "hello"}, "call-1")])
        assert messages[-1]["role"] == "tool"
        return ModelTurn(content="已根据工具结果完成任务")


def test_agent_executes_tool_and_returns_final_answer(tmp_path: Path) -> None:
    registry = ToolRegistry()
    registry.register(Tool(
        name="echo",
        description="回显文本",
        parameters={"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]},
        handler=lambda text: {"echo": text},
    ))
    agent = Agent(
        model=ScriptedModel(),
        registry=registry,
        memory=MemoryStore(tmp_path / "memory.db"),
        log_path=tmp_path / "agent.jsonl",
    )
    result = agent.run("执行回显", session_id="test")
    assert result.answer == "已根据工具结果完成任务"
    assert result.trace[0]["result"]["data"]["echo"] == "hello"
    assert (tmp_path / "agent.jsonl").exists()


class LoopingModel:
    def complete(self, messages, tools):
        return ModelTurn(tool_calls=[ToolCall("missing", {}, "loop")])


def test_agent_stops_infinite_tool_loop(tmp_path: Path) -> None:
    agent = Agent(
        model=LoopingModel(),
        registry=ToolRegistry(),
        memory=MemoryStore(tmp_path / "memory.db"),
        log_path=tmp_path / "agent.jsonl",
        max_steps=2,
    )
    result = agent.run("循环测试")
    assert result.steps == 2
    assert "避免无限工具循环" in result.answer

