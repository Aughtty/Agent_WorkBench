import pytest

from workbench_agent.config import LLMSettings
from workbench_agent.llm_client import LLMProtocolError, OpenAICompatibleClient


class FakeClient(OpenAICompatibleClient):
    def __init__(self, response):
        super().__init__(LLMSettings("https://example.invalid/chat/completions", "secret", "test"))
        self.response = response
        self.last_payload = None

    def _post(self, payload):
        self.last_payload = payload
        return self.response


def test_client_parses_native_tool_call() -> None:
    client = FakeClient({"choices": [{"message": {
        "content": None,
        "tool_calls": [{
            "id": "call-123",
            "type": "function",
            "function": {"name": "search", "arguments": '{"query":"Agent"}'},
        }],
    }}]})
    turn = client.complete([{"role": "user", "content": "查询"}], [{"type": "function"}])
    assert turn.tool_calls[0].name == "search"
    assert turn.tool_calls[0].arguments == {"query": "Agent"}
    assert client.last_payload["tool_choice"] == "auto"


def test_client_parses_plain_answer() -> None:
    client = FakeClient({"choices": [{"message": {"content": "你好"}}]})
    turn = client.complete([{"role": "user", "content": "你好"}], [])
    assert turn.content == "你好"
    assert turn.tool_calls == []


def test_client_rejects_invalid_arguments_json() -> None:
    client = FakeClient({"choices": [{"message": {"tool_calls": [{
        "id": "bad", "function": {"name": "search", "arguments": "not-json"},
    }]}}]})
    with pytest.raises(LLMProtocolError):
        client.complete([], [{"type": "function"}])

