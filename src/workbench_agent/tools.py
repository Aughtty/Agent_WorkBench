"""工具注册、参数校验和三个 MVP 工具。"""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterator

from jsonschema import Draft202012Validator

from .rag import HybridKnowledgeBase, SQLiteChunkStore, TextChunker


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict[str, Any]
    handler: Callable[..., dict[str, Any]]

    def schema(self) -> dict[str, Any]:
        """转换成主流模型原生 Function Calling 接受的 JSON Schema。"""

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


class ToolRegistry:
    """集中管理工具，避免 Agent 主循环写死 if/elif 分支。"""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"工具已注册：{tool.name}")
        self._tools[tool.name] = tool

    def schemas(self) -> list[dict[str, Any]]:
        return [tool.schema() for tool in self._tools.values()]

    def execute(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        tool = self._tools.get(name)
        if tool is None:
            return {"ok": False, "error": f"未知工具：{name}"}

        try:
            errors = sorted(Draft202012Validator(tool.parameters).iter_errors(arguments), key=lambda error: list(error.path))
            if errors:
                details = [error.message for error in errors]
                return {"ok": False, "error": "工具参数校验失败", "details": details}
            return {"ok": True, "data": tool.handler(**arguments)}
        except Exception as exc:  # 工具失败必须成为 Observation，而不是让 Agent 崩溃。
            return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}


class TodoStore:
    """用 SQLite 保存待办，重启程序后数据仍然存在。"""

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS todos ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, "
                "done INTEGER NOT NULL DEFAULT 0)"
            )

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        """提交事务后关闭连接，保证临时数据库可立即清理。"""

        conn = sqlite3.connect(self.database_path)
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def add(self, title: str) -> dict[str, Any]:
        title = title.strip()
        if not title:
            raise ValueError("待办标题不能为空")
        with self._connect() as conn:
            cursor = conn.execute("INSERT INTO todos(title) VALUES (?)", (title,))
            return {"id": cursor.lastrowid, "title": title, "done": False}

    def list(self, include_done: bool = False) -> dict[str, Any]:
        query = "SELECT id, title, done FROM todos"
        if not include_done:
            query += " WHERE done = 0"
        query += " ORDER BY id"
        with self._connect() as conn:
            rows = conn.execute(query).fetchall()
        return {"items": [{"id": row[0], "title": row[1], "done": bool(row[2])} for row in rows]}

    def complete(self, todo_id: int) -> dict[str, Any]:
        with self._connect() as conn:
            cursor = conn.execute("UPDATE todos SET done = 1 WHERE id = ?", (todo_id,))
        if cursor.rowcount == 0:
            raise ValueError(f"不存在待办：{todo_id}")
        return {"id": todo_id, "done": True}


class KnowledgeBase(HybridKnowledgeBase):
    """兼容早期测试的内存构造方式，内部已经使用完整混合检索实现。"""

    def __init__(self, documents: list[dict[str, str]], database_path: Path | None = None) -> None:
        path = database_path or Path(":memory:")
        if str(path) == ":memory:":
            # SQLite 的多个 :memory: 连接不共享数据，因此兼容层使用临时命名文件。
            import tempfile
            path = Path(tempfile.mkdtemp(prefix="workbench-kb-")) / "knowledge.db"
        super().__init__(SQLiteChunkStore(path), TextChunker(chunk_size=500, overlap=80))
        for document in documents:
            self.ingest_text(document["text"], document["source"], document.get("title", ""))


class FileFinder:
    """受根目录约束的本地文件搜索，避免模型传入任意路径。"""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def find(self, keyword: str, limit: int = 20) -> dict[str, Any]:
        keyword = keyword.lower().strip()
        if not keyword:
            raise ValueError("文件关键词不能为空")
        matches = []
        for path in self.root.rglob("*"):
            if path.is_file() and keyword in path.name.lower():
                matches.append({"path": str(path.relative_to(self.root)), "size": path.stat().st_size})
                if len(matches) >= max(1, min(limit, 100)):
                    break
        return {"root": str(self.root), "matches": matches}


def create_registry(
    database_path: Path,
    workspace_root: Path,
    documents: list[dict[str, str]] | None = None,
    knowledge: HybridKnowledgeBase | None = None,
) -> ToolRegistry:
    """创建 MVP 工具集；这里就是 Tool 注册发生的位置。"""

    registry = ToolRegistry()
    todos = TodoStore(database_path)
    knowledge = knowledge or KnowledgeBase(documents or [], database_path.with_name("knowledge.db"))
    files = FileFinder(workspace_root)

    registry.register(Tool(
        name="search_knowledge",
        description="从个人知识库检索与问题相关的资料，并返回来源。",
        parameters={"type": "object", "properties": {
            "query": {"type": "string", "description": "要检索的问题或关键词"},
            "top_k": {"type": "integer", "minimum": 1, "maximum": 10, "default": 3},
            "mode": {"type": "string", "enum": ["bm25", "vector", "hybrid"], "default": "hybrid"},
        }, "required": ["query"], "additionalProperties": False},
        handler=knowledge.search,
    ))
    registry.register(Tool(
        name="find_files",
        description="在允许的工作目录中按文件名关键词查找文件。",
        parameters={"type": "object", "properties": {
            "keyword": {"type": "string"}, "limit": {"type": "integer", "default": 20},
        }, "required": ["keyword"], "additionalProperties": False},
        handler=files.find,
    ))
    registry.register(Tool(
        name="add_todo",
        description="新增一条待办事项。",
        parameters={"type": "object", "properties": {"title": {"type": "string"}},
                    "required": ["title"], "additionalProperties": False},
        handler=todos.add,
    ))
    registry.register(Tool(
        name="list_todos",
        description="列出待办事项。",
        parameters={"type": "object", "properties": {
            "include_done": {"type": "boolean", "default": False}}, "additionalProperties": False},
        handler=todos.list,
    ))
    registry.register(Tool(
        name="complete_todo",
        description="根据待办 ID 将其标记为完成。",
        parameters={"type": "object", "properties": {"todo_id": {"type": "integer"}},
                    "required": ["todo_id"], "additionalProperties": False},
        handler=todos.complete,
    ))
    return registry


def tool_result_message(call_id: str, result: dict[str, Any]) -> dict[str, Any]:
    return {"role": "tool", "tool_call_id": call_id, "content": json.dumps(result, ensure_ascii=False)}
