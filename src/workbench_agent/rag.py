"""完整的本地 RAG 检索层：文档解析、Chunk、持久化、向量化和混合检索。"""

from __future__ import annotations

import math
import re
import sqlite3
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


TOKEN_PATTERN = re.compile(r"[\u4e00-\u9fff]|[a-zA-Z0-9_]+")


def tokenize(text: str) -> list[str]:
    """中文按字、英文按词切分，作为可解释的 BM25 基线。"""

    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source: str
    text: str
    position: int
    title: str = ""


class DocumentLoader:
    """把 TXT、Markdown、PDF、DOCX 统一解析成纯文本。"""

    SUPPORTED_SUFFIXES = {".txt", ".md", ".pdf", ".docx"}

    def load(self, path: Path) -> str:
        path = path.resolve()
        suffix = path.suffix.lower()
        if suffix not in self.SUPPORTED_SUFFIXES:
            raise ValueError(f"不支持的文档类型：{suffix}")
        if suffix in {".txt", ".md"}:
            return path.read_text(encoding="utf-8")
        if suffix == ".pdf":
            from pypdf import PdfReader

            return "\n".join((page.extract_text() or "") for page in PdfReader(str(path)).pages)
        from docx import Document

        document = Document(str(path))
        return "\n".join(paragraph.text for paragraph in document.paragraphs)


class TextChunker:
    """按段落优先、字符长度兜底切块，并保留相邻块重叠。"""

    def __init__(self, chunk_size: int = 500, overlap: int = 80) -> None:
        if chunk_size < 100:
            raise ValueError("chunk_size 不能小于 100")
        if overlap < 0 or overlap >= chunk_size:
            raise ValueError("overlap 必须大于等于 0 且小于 chunk_size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str, source: str, title: str = "") -> list[Chunk]:
        normalized = re.sub(r"\r\n?", "\n", text).strip()
        if not normalized:
            return []

        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", normalized) if part.strip()]
        pieces: list[str] = []
        for paragraph in paragraphs:
            if len(paragraph) <= self.chunk_size:
                pieces.append(paragraph)
            else:
                step = self.chunk_size - self.overlap
                pieces.extend(paragraph[start:start + self.chunk_size] for start in range(0, len(paragraph), step))

        merged: list[str] = []
        current = ""
        for piece in pieces:
            candidate = f"{current}\n\n{piece}".strip() if current else piece
            if current and len(candidate) > self.chunk_size:
                merged.append(current)
                prefix = current[-self.overlap:] if self.overlap else ""
                current = f"{prefix}\n{piece}".strip()
                if len(current) > self.chunk_size:
                    # 超长段已经预切分；这里限制异常组合带来的长度膨胀。
                    current = current[-self.chunk_size:]
            else:
                current = candidate
        if current:
            merged.append(current)

        safe_source = re.sub(r"[^a-zA-Z0-9_.-]+", "-", source).strip("-") or "document"
        return [
            Chunk(chunk_id=f"{safe_source}:{index}", source=source, text=chunk, position=index, title=title)
            for index, chunk in enumerate(merged)
        ]


class SQLiteChunkStore:
    """持久化 Chunk；向量索引可由文本重建，避免数据库绑定模型版本。"""

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS chunks ("
                "chunk_id TEXT PRIMARY KEY, source TEXT NOT NULL, title TEXT NOT NULL, "
                "position INTEGER NOT NULL, text TEXT NOT NULL)"
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)

    def replace_source(self, source: str, chunks: Iterable[Chunk]) -> int:
        items = list(chunks)
        with self._connect() as conn:
            conn.execute("DELETE FROM chunks WHERE source = ?", (source,))
            conn.executemany(
                "INSERT INTO chunks(chunk_id, source, title, position, text) VALUES (?, ?, ?, ?, ?)",
                [(item.chunk_id, item.source, item.title, item.position, item.text) for item in items],
            )
        return len(items)

    def all(self) -> list[Chunk]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT chunk_id, source, text, position, title FROM chunks ORDER BY source, position"
            ).fetchall()
        return [Chunk(*row) for row in rows]

    def count(self) -> int:
        with self._connect() as conn:
            return int(conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0])

    def sources(self) -> list[str]:
        with self._connect() as conn:
            rows = conn.execute("SELECT DISTINCT source FROM chunks ORDER BY source").fetchall()
        return [row[0] for row in rows]


class BM25Retriever:
    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        self.doc_tokens = [tokenize(chunk.text) for chunk in chunks]
        self.avg_len = sum(map(len, self.doc_tokens)) / max(len(self.doc_tokens), 1)
        self.document_frequency: Counter[str] = Counter()
        for tokens in self.doc_tokens:
            self.document_frequency.update(set(tokens))

    def search(self, query: str, top_k: int) -> list[tuple[Chunk, float]]:
        query_tokens = tokenize(query)
        scores: list[tuple[float, int]] = []
        n_docs = len(self.chunks)
        for index, tokens in enumerate(self.doc_tokens):
            counts = Counter(tokens)
            score = 0.0
            for token in query_tokens:
                df = self.document_frequency.get(token, 0)
                idf = math.log(1 + (n_docs - df + 0.5) / (df + 0.5))
                tf = counts.get(token, 0)
                denominator = tf + 1.5 * (1 - 0.75 + 0.75 * len(tokens) / max(self.avg_len, 1))
                score += idf * (tf * 2.5 / denominator if denominator else 0)
            if score > 0:
                scores.append((score, index))
        scores.sort(reverse=True)
        return [(self.chunks[index], score) for score, index in scores[:top_k]]


class LocalVectorRetriever:
    """基于字符 n-gram TF-IDF 的本地向量检索。

    它是真实的向量化与余弦检索，但不是预训练神经网络语义模型。优点是无 GPU、
    无模型下载、中文稳定可复现；简历和面试必须准确称为“本地 TF-IDF 向量基线”。
    """

    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        self.vectorizer: TfidfVectorizer | None = None
        self.matrix: Any = None
        if chunks:
            self.vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), min_df=1, sublinear_tf=True)
            self.matrix = self.vectorizer.fit_transform([chunk.text for chunk in chunks])

    def search(self, query: str, top_k: int) -> list[tuple[Chunk, float]]:
        if not self.chunks or self.vectorizer is None:
            return []
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix)[0]
        indices = np.argsort(scores)[::-1]
        return [(self.chunks[int(index)], float(scores[index])) for index in indices[:top_k] if scores[index] > 0]


class FastEmbedRetriever:
    """使用中文 BGE ONNX 模型生成 512 维神经语义 Embedding。"""

    _models: dict[str, Any] = {}

    def __init__(self, chunks: list[Chunk], model_name: str = "BAAI/bge-small-zh-v1.5") -> None:
        from fastembed import TextEmbedding

        self.chunks = chunks
        self.model_name = model_name
        if model_name not in self._models:
            self._models[model_name] = TextEmbedding(model_name=model_name)
        self.model = self._models[model_name]
        self.matrix = np.vstack(list(self.model.embed([chunk.text for chunk in chunks]))) if chunks else None

    def search(self, query: str, top_k: int) -> list[tuple[Chunk, float]]:
        if not self.chunks or self.matrix is None:
            return []
        query_vector = np.vstack(list(self.model.embed([query])))
        scores = cosine_similarity(query_vector, self.matrix)[0]
        indices = np.argsort(scores)[::-1]
        return [(self.chunks[int(index)], float(scores[index])) for index in indices[:top_k]]


class HybridKnowledgeBase:
    """统一管理入库、BM25、向量检索和 Reciprocal Rank Fusion。"""

    def __init__(
        self,
        store: SQLiteChunkStore,
        chunker: TextChunker | None = None,
        vector_backend: str = "tfidf",
        embedding_model: str = "BAAI/bge-small-zh-v1.5",
    ) -> None:
        self.store = store
        self.chunker = chunker or TextChunker()
        self.loader = DocumentLoader()
        self.vector_backend = vector_backend
        self.embedding_model = embedding_model
        self._reload()

    def _reload(self) -> None:
        self.chunks = self.store.all()
        self.bm25 = BM25Retriever(self.chunks)
        if self.vector_backend == "fastembed":
            self.vector = FastEmbedRetriever(self.chunks, self.embedding_model)
        elif self.vector_backend == "tfidf":
            self.vector = LocalVectorRetriever(self.chunks)
        else:
            raise ValueError("vector_backend 必须是 tfidf 或 fastembed")

    def ingest_text(self, text: str, source: str, title: str = "") -> dict[str, Any]:
        chunks = self.chunker.split(text, source=source, title=title)
        if not chunks:
            raise ValueError("文档没有可入库的文本")
        count = self.store.replace_source(source, chunks)
        self._reload()
        return {"source": source, "chunks": count, "characters": len(text)}

    def ingest_file(self, path: Path, source: str | None = None) -> dict[str, Any]:
        text = self.loader.load(path)
        return self.ingest_text(text, source=source or path.name, title=path.stem)

    def search(self, query: str, top_k: int = 3, mode: str = "hybrid") -> dict[str, Any]:
        query = query.strip()
        if not query:
            raise ValueError("检索问题不能为空")
        top_k = max(1, min(int(top_k), 10))
        if mode not in {"bm25", "vector", "hybrid"}:
            raise ValueError("mode 必须是 bm25、vector 或 hybrid")

        if mode == "bm25":
            ranked = self.bm25.search(query, top_k)
        elif mode == "vector":
            ranked = self.vector.search(query, top_k)
        else:
            ranked = self._hybrid_search(query, top_k)

        matches = []
        for chunk, score in ranked:
            item = asdict(chunk)
            item["score"] = round(float(score), 6)
            item["citation"] = f"[{chunk.source}#chunk-{chunk.position}]"
            matches.append(item)
        return {"query": query, "matches": matches, "retrieval": mode, "total_chunks": len(self.chunks)}

    def _hybrid_search(self, query: str, top_k: int) -> list[tuple[Chunk, float]]:
        # RRF 融合不同量纲的 BM25 分数与余弦相似度，只依赖各自排名。
        candidates: dict[str, tuple[Chunk, float]] = {}
        fetch_k = min(max(top_k * 3, 10), max(len(self.chunks), 1))
        ranked_sources = (
            (1.4, self.bm25.search(query, fetch_k)),
            (1.0, self.vector.search(query, fetch_k)),
        )
        for weight, results in ranked_sources:
            for rank, (chunk, _) in enumerate(results, start=1):
                previous = candidates.get(chunk.chunk_id, (chunk, 0.0))[1]
                candidates[chunk.chunk_id] = (chunk, previous + weight / (60 + rank))
        return sorted(candidates.values(), key=lambda item: item[1], reverse=True)[:top_k]

    def stats(self) -> dict[str, Any]:
        return {
            "chunks": self.store.count(),
            "sources": self.store.sources(),
            "vector_backend": self.vector_backend,
            "embedding_model": self.embedding_model if self.vector_backend == "fastembed" else None,
        }
