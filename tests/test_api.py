from pathlib import Path

from fastapi.testclient import TestClient

from workbench_agent.api import create_api


def test_health_and_document_endpoints(tmp_path: Path) -> None:
    client = TestClient(create_api(tmp_path, online=False))
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    added = client.post("/documents/text", json={
        "source": "api-test.md",
        "text": "API 文档导入测试：Agent 可以使用工具。",
    })
    assert added.status_code == 200
    assert added.json()["chunks"] == 1
    assert "api-test.md" in client.get("/documents").json()["sources"]


def test_chat_and_memory_clear_endpoints(tmp_path: Path) -> None:
    client = TestClient(create_api(tmp_path, online=False))
    response = client.post("/chat", json={"message": "列出我的待办", "session_id": "api-session"})
    assert response.status_code == 200
    assert response.json()["steps"] >= 1
    cleared = client.delete("/memory/api-session")
    assert cleared.status_code == 200
    assert cleared.json()["deleted_messages"] == 2

