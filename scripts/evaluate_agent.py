"""少量真实 LLM 端到端案例，评估 Tool 选择；会消耗学校服务额度。"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from workbench_agent.app import build_components


def main() -> None:
    cases = json.loads((ROOT / "evals" / "agent_cases.json").read_text(encoding="utf-8"))
    # Windows 上安全软件可能短暂占用刚关闭的 SQLite 文件；评测结果不应因临时目录
    # 清理失败而被误判，因此允许系统稍后回收该临时目录。
    with tempfile.TemporaryDirectory(prefix="workbench-agent-eval-", ignore_cleanup_errors=True) as directory:
        service = build_components(Path(directory), online=True)
        for path in sorted((ROOT / "knowledge").glob("*.md")):
            service.knowledge.ingest_file(path, source=path.name)
        passed = 0
        records = []
        for index, case in enumerate(cases):
            result = service.agent.run(case["prompt"], session_id=f"eval-{index}")
            actual = [item["tool"] for item in result.trace if item.get("type") == "tool_call"]
            expected = case["expected_tools"]
            tool_ok = set(actual) == set(expected)
            answer_ok = len(result.answer.strip()) >= 10
            if "search_knowledge" in expected:
                answer_ok = answer_ok and "[" in result.answer and "#chunk-" in result.answer
            max_tool_calls = max(1, len(expected) * 2)
            efficiency_ok = len(actual) <= max_tool_calls and result.steps <= max_tool_calls + 1
            ok = tool_ok and answer_ok and efficiency_ok
            passed += int(ok)
            records.append({
                "name": case["name"], "passed": ok, "expected": case["expected_tools"],
                "actual": actual, "tool_ok": tool_ok, "answer_ok": answer_ok, "efficiency_ok": efficiency_ok,
                "steps": result.steps,
            })
        output = {"passed": passed, "total": len(cases), "success_rate": round(passed / len(cases), 4), "cases": records}
        output_path = ROOT / "docs" / "agent评测结果.json"
        output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({key: output[key] for key in ("passed", "total", "success_rate")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
