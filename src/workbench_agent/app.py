"""组装应用依赖，入口文件不需要知道各模块的创建细节。"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from .agent import Agent
from .config import LLMSettings
from .llm_client import OpenAICompatibleClient
from .memory import MemoryStore
from .offline_model import OfflineDemoModel
from .tools import create_registry
from .rag import HybridKnowledgeBase, SQLiteChunkStore, TextChunker


DEFAULT_DOCUMENTS = [
    {
        "source": "knowledge/agent-memory.md",
        "text": "Agent Memory 用于保存任务相关信息。短期记忆通常保存最近对话，长期记忆可保存用户偏好或历史事实。",
    },
    {
        "source": "knowledge/tool-calling.md",
        "text": "Tool Calling 是模型根据工具描述和 JSON Schema 生成结构化调用参数，再由应用执行工具并把结果回传给模型。",
    },
    {
        "source": "knowledge/rag.md",
        "text": "RAG 是检索增强生成：先检索外部知识，再把相关上下文交给大模型生成回答，并应保留来源。",
    },
]


@dataclass
class AppComponents:
    agent: Agent
    knowledge: HybridKnowledgeBase
    memory: MemoryStore


def build_components(data_dir: Path, online: bool) -> AppComponents:
    data_dir.mkdir(parents=True, exist_ok=True)
    vector_backend = os.getenv("EMBEDDING_BACKEND", "fastembed" if online else "tfidf")
    knowledge = HybridKnowledgeBase(
        SQLiteChunkStore(data_dir / "knowledge.db"),
        TextChunker(chunk_size=500, overlap=80),
        vector_backend=vector_backend,
        embedding_model=os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5"),
    )
    if knowledge.store.count() == 0:
        for document in DEFAULT_DOCUMENTS:
            knowledge.ingest_text(document["text"], document["source"])
    registry = create_registry(data_dir / "workbench.db", Path("workspace"), knowledge=knowledge)
    memory = MemoryStore(data_dir / "workbench.db")
    model = OpenAICompatibleClient(LLMSettings.from_env()) if online else OfflineDemoModel()
    agent = Agent(
        model=model,
        registry=registry,
        memory=memory,
        log_path=Path("logs") / "agent.jsonl",
    )
    return AppComponents(agent=agent, knowledge=knowledge, memory=memory)


def build_offline_app(data_dir: Path) -> Agent:
    return build_components(data_dir, online=False).agent


def build_online_app(data_dir: Path) -> Agent:
    """使用 `.env` 中的学校 LLM 服务组装真实 Agent。"""

    return build_components(data_dir, online=True).agent
