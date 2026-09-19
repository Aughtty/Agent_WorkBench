"""学校 OpenAI-compatible Chat Completions 服务适配器。"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any

from .config import LLMSettings
from .contracts import ModelTurn, ToolCall


class LLMRequestError(RuntimeError):
    """网络、鉴权、限额或服务端错误。"""


class LLMProtocolError(RuntimeError):
    """响应不是预期的 Chat Completions 格式。"""


class OpenAICompatibleClient:
    """只依赖 HTTP 协议，不绑定 OpenAI SDK。

    学校服务虽然使用自定义 URL，但请求样例采用 model + messages 的
    Chat Completions 格式。如果服务支持原生 Function Calling，同一个请求还可
    携带 tools 和 tool_choice；响应中的 tool_calls 会被转换为项目内部协议。
    """

    def __init__(self, settings: LLMSettings) -> None:
        self.settings = settings

    def complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> ModelTurn:
        payload: dict[str, Any] = {
            "model": self.settings.model,
            "messages": messages,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        response = self._post(payload)
        try:
            message = response["choices"][0]["message"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMProtocolError("响应缺少 choices[0].message") from exc

        parsed_calls: list[ToolCall] = []
        for index, raw_call in enumerate(message.get("tool_calls") or []):
            try:
                function = raw_call["function"]
                arguments = function.get("arguments", "{}")
                if isinstance(arguments, str):
                    arguments = json.loads(arguments)
                if not isinstance(arguments, dict):
                    raise TypeError("arguments 必须是 JSON object")
                parsed_calls.append(ToolCall(
                    name=function["name"],
                    arguments=arguments,
                    call_id=raw_call.get("id") or f"call-{index}",
                ))
            except (KeyError, TypeError, json.JSONDecodeError) as exc:
                raise LLMProtocolError(f"无法解析第 {index + 1} 个 tool_call") from exc

        return ModelTurn(
            content=message.get("content") or "",
            tool_calls=parsed_calls,
            usage=response.get("usage") or {},
            model=response.get("model") or self.settings.model,
        )

    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(
            self.settings.chat_url,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.api_key}",
            },
        )
        raw = ""
        for attempt in range(self.settings.max_retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self.settings.timeout_seconds) as response:
                    raw = response.read().decode("utf-8")
                break
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")[:1000]
                retryable = exc.code == 429 or 500 <= exc.code < 600
                if not retryable or attempt >= self.settings.max_retries:
                    raise LLMRequestError(f"LLM HTTP {exc.code}: {detail}") from exc
            except urllib.error.URLError as exc:
                if attempt >= self.settings.max_retries:
                    raise LLMRequestError(f"无法连接 LLM 服务：{exc.reason}") from exc
            time.sleep(0.5 * (2 ** attempt))

        try:
            decoded = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LLMProtocolError(f"LLM 返回的不是 JSON：{raw[:300]}") from exc
        if not isinstance(decoded, dict):
            raise LLMProtocolError("LLM JSON 响应顶层必须是 object")
        return decoded
