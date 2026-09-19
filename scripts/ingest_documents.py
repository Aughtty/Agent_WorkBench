"""批量导入 knowledge 目录中的支持文件。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from workbench_agent.app import build_components


def main() -> None:
    parser = argparse.ArgumentParser(description="批量导入个人知识库")
    parser.add_argument("directory", nargs="?", default="knowledge")
    parser.add_argument("--data-dir", default="data")
    args = parser.parse_args()

    directory = Path(args.directory).resolve()
    service = build_components(Path(args.data_dir), online=False)
    files = [path for path in directory.rglob("*") if path.suffix.lower() in service.knowledge.loader.SUPPORTED_SUFFIXES]
    if not files:
        raise SystemExit(f"没有找到支持的文档：{directory}")
    for path in files:
        source = str(path.relative_to(directory)).replace("\\", "/")
        result = service.knowledge.ingest_file(path, source=source)
        print(f"PASS {source}: {result['chunks']} chunks")
    print(service.knowledge.stats())


if __name__ == "__main__":
    main()

