"""无需先安装项目即可启动 FastAPI。"""

from __future__ import annotations

import sys
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(SOURCE_ROOT))

import uvicorn


if __name__ == "__main__":
    uvicorn.run("workbench_agent.api:app", host="127.0.0.1", port=8000, reload=False)

