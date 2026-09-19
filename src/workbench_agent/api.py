"""FastAPI 服务层：对话、知识库管理、Memory 和健康检查。"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from .app import AppComponents, build_components
from .llm_client import LLMProtocolError, LLMRequestError


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    session_id: str = Field(default="default", min_length=1, max_length=100)


class ChatResponse(BaseModel):
    answer: str
    steps: int
    trace: list[dict[str, Any]]


class TextDocumentRequest(BaseModel):
    source: str = Field(min_length=1, max_length=300)
    text: str = Field(min_length=1, max_length=2_000_000)
    title: str = Field(default="", max_length=300)


def create_api(data_dir: Path = Path("data"), online: bool = True) -> FastAPI:
    app = FastAPI(
        title="个人信息工作台 Agent API",
        version="0.3.0",
        description="单 Agent 多工具、RAG、Memory 与可观测 Trace API",
    )
    components: AppComponents | None = None

    def get_components() -> AppComponents:
        nonlocal components
        if components is None:
            components = build_components(data_dir, online=online)
        return components

    @app.get("/health")
    def health() -> dict[str, Any]:
        service = get_components()
        return {"status": "ok", "online": online, "knowledge": service.knowledge.stats()}

    @app.post("/chat", response_model=ChatResponse)
    def chat(request: ChatRequest) -> ChatResponse:
        try:
            result = get_components().agent.run(request.message, request.session_id)
            return ChatResponse(answer=result.answer, steps=result.steps, trace=result.trace)
        except (LLMRequestError, LLMProtocolError) as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/documents/text")
    def add_text_document(request: TextDocumentRequest) -> dict[str, Any]:
        try:
            return get_components().knowledge.ingest_text(request.text, request.source, request.title)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/documents/upload")
    async def upload_document(file: UploadFile = File(...)) -> dict[str, Any]:
        suffix = Path(file.filename or "").suffix.lower()
        if suffix not in get_components().knowledge.loader.SUPPORTED_SUFFIXES:
            raise HTTPException(status_code=415, detail=f"不支持的文件类型：{suffix}")
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="文件不能超过 10 MB")
        with tempfile.TemporaryDirectory(prefix="workbench-upload-") as directory:
            path = Path(directory) / Path(file.filename or f"upload{suffix}").name
            path.write_bytes(content)
            try:
                return get_components().knowledge.ingest_file(path, source=Path(file.filename or path.name).name)
            except (ValueError, OSError) as exc:
                raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/documents")
    def list_documents() -> dict[str, Any]:
        return get_components().knowledge.stats()

    @app.delete("/memory/{session_id}")
    def clear_memory(session_id: str) -> dict[str, Any]:
        service = get_components()
        before = service.memory.count(session_id)
        service.memory.clear(session_id)
        return {"session_id": session_id, "deleted_messages": before}

    return app


app = create_api()

