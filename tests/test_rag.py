from pathlib import Path

from workbench_agent.rag import DocumentLoader, HybridKnowledgeBase, SQLiteChunkStore, TextChunker


def test_chunker_preserves_source_and_overlap() -> None:
    text = "第一段介绍 Agent。\n\n" + "工具调用可以连接外部系统。" * 30
    chunks = TextChunker(chunk_size=120, overlap=20).split(text, source="notes.md")
    assert len(chunks) >= 2
    assert all(chunk.source == "notes.md" for chunk in chunks)
    assert chunks[0].chunk_id == "notes.md:0"


def test_document_loader_reads_markdown(tmp_path: Path) -> None:
    path = tmp_path / "note.md"
    path.write_text("# 标题\n\n正文", encoding="utf-8")
    assert "正文" in DocumentLoader().load(path)


def test_hybrid_knowledge_base_persists_and_cites(tmp_path: Path) -> None:
    database = tmp_path / "knowledge.db"
    knowledge = HybridKnowledgeBase(SQLiteChunkStore(database), TextChunker(chunk_size=120, overlap=20))
    knowledge.ingest_text("Agent 通过 Tool Calling 调用外部工具。", "agent.md")
    result = knowledge.search("外部工具怎么调用", top_k=1, mode="hybrid")
    assert result["matches"][0]["source"] == "agent.md"
    assert result["matches"][0]["citation"] == "[agent.md#chunk-0]"

    reloaded = HybridKnowledgeBase(SQLiteChunkStore(database))
    assert reloaded.stats()["chunks"] == 1


def test_replacing_same_source_does_not_duplicate_chunks(tmp_path: Path) -> None:
    knowledge = HybridKnowledgeBase(SQLiteChunkStore(tmp_path / "knowledge.db"), TextChunker(chunk_size=120, overlap=20))
    knowledge.ingest_text("第一次内容", "same.md")
    knowledge.ingest_text("第二次内容", "same.md")
    assert knowledge.stats()["chunks"] == 1
    assert knowledge.search("第二次", mode="bm25")["matches"][0]["source"] == "same.md"

