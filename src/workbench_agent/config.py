"""读取本地配置；不把密钥硬编码进代码或提交到 Git。"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def load_env_file(path: Path = Path(".env")) -> None:
    """加载简单 KEY=VALUE 格式；已有系统环境变量优先，不被文件覆盖。"""

    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@dataclass(frozen=True)
class LLMSettings:
    chat_url: str
    api_key: str
    model: str
    timeout_seconds: float = 60.0
    max_retries: int = 2

    @classmethod
    def from_env(cls) -> "LLMSettings":
        load_env_file()
        required = ["LLM_CHAT_URL", "LLM_API_KEY", "LLM_MODEL"]
        missing = [name for name in required if not os.getenv(name)]
        if missing:
            raise ValueError(f"缺少 LLM 配置：{', '.join(missing)}。请检查仓库根目录 .env")
        return cls(
            chat_url=os.environ["LLM_CHAT_URL"].strip(),
            api_key=os.environ["LLM_API_KEY"].strip(),
            model=os.environ["LLM_MODEL"].strip(),
            timeout_seconds=float(os.getenv("LLM_TIMEOUT_SECONDS", "60")),
            max_retries=int(os.getenv("LLM_MAX_RETRIES", "2")),
        )
