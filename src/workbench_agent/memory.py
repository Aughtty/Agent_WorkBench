"""短期会话记忆：保存最近消息，支持多轮任务。"""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


class MemoryStore:
    def __init__(self, database_path: Path, window_size: int = 12, max_chars: int = 12000) -> None:
        self.database_path = database_path
        self.window_size = window_size
        self.max_chars = max_chars
        database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS messages ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT NOT NULL, "
                "payload TEXT NOT NULL)"
            )

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        """统一管理事务和连接生命周期，避免 SQLite 句柄泄漏。"""

        conn = sqlite3.connect(self.database_path)
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def append(self, session_id: str, message: dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO messages(session_id, payload) VALUES (?, ?)",
                (session_id, json.dumps(message, ensure_ascii=False)),
            )

    def recent(self, session_id: str) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT payload FROM messages WHERE session_id = ? ORDER BY id DESC LIMIT ?",
                (session_id, self.window_size),
            ).fetchall()
        messages = [json.loads(row[0]) for row in reversed(rows)]
        selected: list[dict[str, Any]] = []
        used = 0
        for message in reversed(messages):
            size = len(json.dumps(message, ensure_ascii=False))
            if selected and used + size > self.max_chars:
                break
            selected.append(message)
            used += size
        return list(reversed(selected))

    def count(self, session_id: str) -> int:
        with self._connect() as conn:
            return int(conn.execute("SELECT COUNT(*) FROM messages WHERE session_id = ?", (session_id,)).fetchone()[0])

    def clear(self, session_id: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
