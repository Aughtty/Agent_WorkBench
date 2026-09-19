"""使用固定问题集计算 Hit@K 和 MRR，并输出各检索模式的真实结果。"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from workbench_agent.rag import HybridKnowledgeBase, SQLiteChunkStore, TextChunker


def main() -> None:
    cases = json.loads((ROOT / "evals" / "retrieval_cases.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="workbench-eval-") as directory:
        for backend in ("tfidf", "fastembed"):
            knowledge = HybridKnowledgeBase(
                SQLiteChunkStore(Path(directory) / f"knowledge-{backend}.db"),
                TextChunker(),
                vector_backend=backend,
            )
            for path in sorted((ROOT / "knowledge").glob("*.md")):
                knowledge.ingest_file(path, source=path.name)

            for mode in ("bm25", "vector", "hybrid"):
                evaluate_mode(cases, knowledge, backend, mode)


def evaluate_mode(cases, knowledge, backend: str, mode: str) -> None:
    hits = 0
    reciprocal_rank = 0.0
    failures = []
    for case in cases:
        matches = knowledge.search(case["query"], top_k=3, mode=mode)["matches"]
        sources = [match["source"] for match in matches]
        if case["source"] in sources:
            hits += 1
            reciprocal_rank += 1.0 / (sources.index(case["source"]) + 1)
        else:
            failures.append({"query": case["query"], "expected": case["source"], "got": sources})
    total = len(cases)
    print(json.dumps({
        "backend": backend,
        "mode": mode,
        "cases": total,
        "hit_at_3": round(hits / total, 4),
        "mrr_at_3": round(reciprocal_rank / total, 4),
        "failures": failures,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
