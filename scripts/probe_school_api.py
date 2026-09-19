"""探测学校模型是否支持原生 Tool Calling；不会打印 API Key。"""

from __future__ import annotations

import sys
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE_ROOT))

from workbench_agent.config import LLMSettings
from workbench_agent.llm_client import OpenAICompatibleClient


def main() -> None:
    client = OpenAICompatibleClient(LLMSettings.from_env())
    turn = client.complete(
        messages=[{"role": "user", "content": "请使用天气工具查询北京天气，不要直接回答。"}],
        tools=[{
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "查询指定城市天气",
                "parameters": {
                    "type": "object",
                    "properties": {"city": {"type": "string"}},
                    "required": ["city"],
                    "additionalProperties": False,
                },
            },
        }],
    )
    if turn.tool_calls:
        call = turn.tool_calls[0]
        print("PASS：服务支持原生 Tool Calling")
        print({"tool": call.name, "arguments": call.arguments, "call_id": call.call_id})
    else:
        print("FAIL：响应中没有 tool_calls")
        print({"content": turn.content})


if __name__ == "__main__":
    main()

