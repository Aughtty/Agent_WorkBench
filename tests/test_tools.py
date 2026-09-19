from pathlib import Path

from workbench_agent.tools import FileFinder, KnowledgeBase, TodoStore


def test_todo_round_trip(tmp_path: Path) -> None:
    store = TodoStore(tmp_path / "test.db")
    created = store.add("准备面试")
    assert store.list()["items"][0]["title"] == "准备面试"
    store.complete(created["id"])
    assert store.list()["items"] == []
    assert store.list(include_done=True)["items"][0]["done"] is True


def test_knowledge_search_returns_source() -> None:
    knowledge = KnowledgeBase([
        {"source": "agent.md", "text": "Agent 使用工具完成任务"},
        {"source": "rag.md", "text": "RAG 包含检索和生成"},
    ])
    result = knowledge.search("Agent 工具", top_k=1)
    assert result["matches"][0]["source"] == "agent.md"
    assert result["retrieval"] == "hybrid"
    assert result["matches"][0]["citation"] == "[agent.md#chunk-0]"


def test_tool_registry_rejects_wrong_argument_type() -> None:
    from workbench_agent.tools import Tool, ToolRegistry

    registry = ToolRegistry()
    registry.register(Tool(
        name="limited",
        description="类型校验测试",
        parameters={
            "type": "object",
            "properties": {"count": {"type": "integer", "minimum": 1, "maximum": 3}},
            "required": ["count"],
            "additionalProperties": False,
        },
        handler=lambda count: {"count": count},
    ))
    result = registry.execute("limited", {"count": "three"})
    assert result["ok"] is False
    assert result["error"] == "工具参数校验失败"


def test_file_finder_is_scoped_to_root(tmp_path: Path) -> None:
    (tmp_path / "面试笔记.md").write_text("test", encoding="utf-8")
    result = FileFinder(tmp_path).find("面试")
    assert result["matches"][0]["path"] == "面试笔记.md"
