"""项目的一键入口。

默认进入交互模式；--demo 会运行一个不需要 API Key 的可重复演示。
离线演示用于验证 Agent 主循环和 Tool 协议，不冒充真实 LLM。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# 允许用户刚克隆仓库、尚未执行 `pip install -e .` 时直接运行。
# 安装后 Python 会自行找到包；这行只为一键启动提供可靠兜底。
SOURCE_ROOT = Path(__file__).resolve().parent / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from workbench_agent.app import build_offline_app, build_online_app


def main() -> None:
    parser = argparse.ArgumentParser(description="个人信息工作台 Agent")
    parser.add_argument("--demo", action="store_true", help="运行离线可重复演示")
    parser.add_argument("--online", action="store_true", help="使用 .env 中配置的真实 LLM")
    parser.add_argument("--data-dir", default="data", help="数据库目录")
    args = parser.parse_args()

    if args.demo and args.online:
        parser.error("--demo 和 --online 不能同时使用")
    agent = build_online_app(Path(args.data_dir)) if args.online else build_offline_app(Path(args.data_dir))
    if args.demo:
        questions = [
            "帮我查知识库里的 Agent Memory，并记录一个复习待办",
            "列出我的待办",
        ]
        for question in questions:
            print(f"\n用户：{question}")
            result = agent.run(question, session_id="demo")
            print(f"助手：{result.answer}")
        return

    print("个人信息工作台 Agent（输入 exit 退出）")
    while True:
        question = input("\n你：").strip()
        if question.lower() in {"exit", "quit"}:
            break
        result = agent.run(question, session_id="cli")
        print(f"助手：{result.answer}")


if __name__ == "__main__":
    main()
