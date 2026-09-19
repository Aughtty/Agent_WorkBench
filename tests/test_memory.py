from pathlib import Path

from workbench_agent.memory import MemoryStore


def test_memory_isolates_sessions_and_clears(tmp_path: Path) -> None:
    memory = MemoryStore(tmp_path / "memory.db")
    memory.append("a", {"role": "user", "content": "A 的消息"})
    memory.append("b", {"role": "user", "content": "B 的消息"})
    assert memory.recent("a")[0]["content"] == "A 的消息"
    assert memory.count("b") == 1
    memory.clear("a")
    assert memory.recent("a") == []


def test_memory_respects_character_budget(tmp_path: Path) -> None:
    memory = MemoryStore(tmp_path / "memory.db", window_size=10, max_chars=100)
    for index in range(5):
        memory.append("s", {"role": "user", "content": f"{index}" * 40})
    recent = memory.recent("s")
    assert len(recent) < 5
    assert recent[-1]["content"].startswith("4")

