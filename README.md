# 个人信息工作台 Agent

面向个人学习与工作的单 Agent 多工具应用。用户用自然语言提出目标，模型通过原生 Function Calling 决定是否检索知识库、查找文件或管理待办，并根据工具结果继续执行，直到形成带来源的回答。

本项目重点不是堆叠框架，而是显式实现并验证：Agent 主循环、Tool Schema、RAG、Memory、API、Trace、异常处理、自动测试和评测。

## 已实现功能

- 学校 `tju-llm` 服务的原生 Tool Calling。
- 自定义“模型决策 → 工具执行 → Observation → 再决策”循环。
- 知识检索、文件查找、新增/列出/完成待办 5 个工具。
- TXT、Markdown、PDF、DOCX 文档解析。
- 段落优先、字符长度兜底的 Chunk 与 Overlap。
- BGE-small-zh-v1.5 中文神经 Embedding（FastEmbed/ONNX，CPU）。
- BM25、向量检索、加权 RRF Hybrid Search。
- SQLite Chunk、待办和短期会话 Memory。
- 来源引用，例如 `[rag.md#chunk-0]`。
- JSON Schema 参数校验、模型超时/429/5xx 重试、最大步骤保护。
- JSONL Trace：模型/工具耗时、参数、结果、模型名和 Token usage。
- FastAPI：健康检查、聊天、文本/文件入库、知识库状态、清空 Memory。
- Streamlit 演示界面。
- pytest、20 条检索评测、8 条真实 Agent 评测。

## 为什么需要 Agent

固定 Workflow 必须提前确定步骤，而用户目标可能需要不同工具组合：

```text
“查一下 Top-K 为什么不能越大越好，并记录一个调整 Top-K 的待办”
                              │
                              ▼
                       LLM 判断下一步
                    ┌─────────┴─────────┐
                    ▼                   ▼
          search_knowledge          add_todo
                    └─────────┬─────────┘
                              ▼
                    根据 Observation 汇总
```

模型只生成工具名和参数，Python 应用负责校验并执行函数。模型不能直接访问数据库或文件系统。

## 系统架构

```text
CLI / FastAPI / Streamlit
          │
          ▼
      Agent.run()
          │  messages + tools
          ▼
 学校 Chat Completions API
          │  tool_calls
          ▼
 ToolRegistry + JSON Schema
   ├── search_knowledge
   │     ├── DocumentLoader
   │     ├── TextChunker
   │     ├── BM25
   │     ├── BGE Embedding
   │     └── Weighted RRF
   ├── find_files（受限根目录）
   └── TodoStore（SQLite）
          │
          ▼ role=tool Observation
      再次请求模型
          │
          ├── Memory（SQLite，会话隔离与字符预算）
          └── Trace（JSONL）
```

## 技术栈与职责

| 技术 | 职责 |
|---|---|
| Python | Agent、工具、RAG 与服务端核心逻辑 |
| 学校 LLM API | 语言理解、工具选择和最终生成 |
| JSON Schema | 描述并校验 Tool 参数 |
| FastEmbed + BGE | CPU 中文神经 Embedding |
| scikit-learn | TF-IDF 向量基线和余弦相似度 |
| BM25 + RRF | 精确词法检索与混合排名 |
| SQLite | Chunk、Todo、会话消息持久化 |
| FastAPI | REST API 和错误边界 |
| Streamlit | 轻量演示 UI，不承载业务逻辑 |
| pytest | Agent、RAG、Memory、API 与 Tool 测试 |

Agent 核心没有使用 LangChain/LangGraph，因此可以直接解释 Tool Call、call_id、Observation、停止条件和失败回传。其他库只负责各自的基础设施。

## 项目目录

```text
personal-workbench-agent/
├─ main.py                       # CLI
├─ api_main.py                   # FastAPI 入口
├─ ui.py                         # Streamlit UI
├─ pyproject.toml                # 依赖声明
├─ src/workbench_agent/
│  ├─ agent.py                   # Agent 主循环
│  ├─ contracts.py               # ModelTurn / ToolCall 协议
│  ├─ llm_client.py              # 学校模型适配、重试和解析
│  ├─ tools.py                   # Tool Registry、Todo、文件搜索
│  ├─ rag.py                     # 解析、Chunk、Embedding、混合检索
│  ├─ memory.py                  # 会话隔离和上下文预算
│  ├─ api.py                     # FastAPI
│  ├─ prompts.py                 # 系统 Prompt
│  └─ app.py                     # 依赖组装
├─ knowledge/                    # 示例知识文档
├─ evals/                        # 固定评测数据
├─ scripts/                      # 入库、探测和评测脚本
├─ tests/                        # 自动测试
└─ docs/                         # 学习、验证、简历与面试文档
```

## 安装与配置

推荐 Python 3.11：

```powershell
cd D:\Code\work\personal-workbench-agent
python -m pip install -e ".[dev,ui]"
Copy-Item .env.example .env
```

在 `.env` 中填写：

```env
LLM_CHAT_URL=https://ai.tju.edu.cn/api/agent2026/你的专用端点/chat/completions
LLM_API_KEY=只保存在本机的Key
LLM_MODEL=tju-llm
LLM_TIMEOUT_SECONDS=60
LLM_MAX_RETRIES=2
EMBEDDING_BACKEND=fastembed
EMBEDDING_MODEL=BAAI/bge-small-zh-v1.5
```

`.env` 已被 `.gitignore` 排除。首次使用 BGE 会下载模型缓存，之后可离线生成 Embedding。

## 启动

真实 CLI：

```powershell
python main.py --online
```

FastAPI：

```powershell
python api_main.py
```

接口文档：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Streamlit：

```powershell
python -m streamlit run ui.py
```

浏览器打开 [http://127.0.0.1:8501](http://127.0.0.1:8501)。Windows 也可使用 `run.bat`、`run_api.bat`、`run_ui.bat`。

## 文档入库

批量导入 `knowledge/`：

```powershell
python scripts/ingest_documents.py knowledge
```

也可通过 API 或 Streamlit 上传 TXT、Markdown、PDF、DOCX。相同 `source` 再次导入时覆盖旧 Chunk，避免重复索引。

## API 示例

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health

$body = @{
  message = "根据知识库解释 Tool Calling，并附上来源"
  session_id = "demo-user"
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/chat `
  -Method Post `
  -ContentType "application/json; charset=utf-8" `
  -Body ([Text.Encoding]::UTF8.GetBytes($body))
```

## 测试与评测

```powershell
python -m pytest
python scripts/evaluate_retrieval.py
python scripts/evaluate_agent.py
```

2026-09-19 的实际结果：

- pytest：17 passed。
- 20 条检索集：加权 Hybrid Hit@3=1.0、MRR@3=0.9417。
- 8 条真实 Agent 案例：严格 Tool/回答/引用/效率检查 8/8。
- FastAPI `/health`、`/documents/text`、`/chat`：200。
- Streamlit `/_stcore/health`：200。

数据集只有 4 个主题文档、20 个问题，结果只能证明当前回归集，不代表开放领域准确率。

## 真实使用案例

1. 根据知识库解释 Tool Calling，并附来源。
2. 查找 RAG 的 Top-K 取舍并记录复习待办。
3. 列出未完成待办。
4. 根据 ID 完成待办。
5. 在受限工作目录查找指定文件。
6. 上传课程 PDF 后进行带引用问答。
7. 比较 Agent 与 Workflow。
8. 在多轮对话中追问上一轮主题。

## 当前局限

- SQLite 和进程内向量索引适合单机个人项目，不是大规模多用户 Vector Database。
- 新增文档后会重建向量矩阵，大语料需要迁移 Qdrant/Milvus/pgvector。
- BGE 适合中文检索，但当前没有 Reranker。
- Token usage 依赖学校网关是否返回 `usage`。
- Memory 是短期窗口，不是跨会话长期偏好系统。
- 没有权限体系、分布式部署和高并发，不得宣称生产级高可用。
- 当前评测集规模小，后续应加入真实个人文档和困难负样本。

## 延伸方向

优先增加真实文档评测和 Reranker；数据增长后迁移 Qdrant/pgvector。MCP、LangGraph、Docker可作为后续工程扩展。第一阶段不增加 Multi-Agent、GraphRAG、微调或 Kubernetes。

