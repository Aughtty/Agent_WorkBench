# Agent / LLM 应用开发实习面试知识体系

> 面向北京地区 Agent、AI 应用开发、大模型应用开发实习。目标不是背 500 个答案，而是在最多 15 天内建立“识别考点 → 解释原理 → 联系代码 → 应对追问”的能力。

## 0. 使用说明

### 0.1 完成标准

一个知识点只有同时满足以下条件，才能标为“可以应对追问”：

1. 不看答案，用一句话解释它是什么；
2. 说明它为什么出现、解决什么问题；
3. 说出核心流程或原理；
4. 与相似技术作比较；
5. 指出它在 Agent_WorkBench 中的位置，或说明项目为何没用；
6. 接住至少 1～2 层追问；
7. 能给出一个失败场景和排查方向。

学习状态统一使用：

```text
[ ] 未学习  [ ] 已看过  [ ] 已理解  [ ] 可以独立回答  [ ] 可以应对追问
```

“之前教学已涉及”只表示接触过，不代表已掌握。

### 0.2 时间分配原则

- P0：约 65% 时间。必须能独立回答并联系项目；
- P1：约 25% 时间。能回答主体并接一层追问；
- P2：约 8% 时间。知道原理、场景和取舍；
- P3：约 2% 时间。知道它是什么，JD 明确要求再深入。

每天建议：55% 新知识、20% 闭卷复述、15% 项目映射、10% 模拟追问。学习不是“读完”，必须开口回答。

### 0.3 优先级依据

2026 年可检索 JD 抽样显示：Python、RAG、Agent、Tool Calling、Prompt、向量检索、API/后端、评测与工程落地反复出现；LangChain/LangGraph、部署和推理优化多为高频追问或加分项。参考样本包括：[国家大学生就业服务平台大模型算法实习](https://www.ncss.cn/student/jobs/KFbad5y2NBH8Z5f3yhqoKe/detail.html)、[阿里巴巴大模型应用开发实习](https://www.jdwatch.work/jobs/j1ohuw8wq)、[西门子北京 LLM 应用开发实习](https://cn.linkedin.com/jobs/view/ai%E5%BC%80%E5%8F%91%E5%AE%9E%E4%B9%A0%E7%94%9F%EF%BC%88llm%E5%BA%94%E7%94%A8%E6%96%B9%E5%90%91-pipeline%EF%BC%89-at-siemens-4325064652)、[大模型 Agent 知识库实习](https://offerdao.ai/j/agent_ota7vfintj6rvp)。岗位样本会随时间变化，本手册据此做优先级推断，不把单个 JD 当统一标准。

---

# 1. 整体知识地图

```text
Agent / LLM 应用开发实习
│
├── 编程与工程底座
│   ├── Python：对象、函数、异常、迭代器、装饰器、并发/异步
│   ├── HTTP / REST / JSON / API
│   ├── Git / Linux / 测试 / 日志
│   └── 数据结构、数据库、缓存
│
├── AI 与 LLM 原理
│   ├── ML/DL/NLP 基础
│   ├── Transformer / Attention / QKV / Mask
│   ├── Token / Embedding / Context Window
│   ├── Pretraining / SFT / Alignment / LoRA
│   └── 推理：Sampling / KV Cache / Quantization
│
├── LLM 应用
│   ├── Prompt / System Prompt / Structured Output
│   ├── LLM API / Streaming / Retry / Rate Limit
│   └── Context Engineering / Safety
│
├── RAG
│   ├── Loader / Cleaning / Chunk / Metadata
│   ├── Sparse + Dense Retrieval
│   ├── Vector DB / Top-K / Similarity
│   ├── Hybrid / Reranker / Query Rewrite
│   └── Generation / Citation / Evaluation
│
├── Agent
│   ├── Tool Calling / Schema / Observation
│   ├── Planning / ReAct / Reflection
│   ├── Memory / State / Context
│   ├── Agent vs Workflow / Human-in-the-loop
│   └── Evaluation / Trace / Permission / Cost
│
├── Framework
│   ├── LangChain：组件与快速集成
│   └── LangGraph：State、Node、Edge、Checkpoint
│
└── 面试输出
    ├── 定义 / 原理 / 为什么 / 对比
    ├── 代码 / 项目 / Debug
    ├── 场景 / 系统设计 / 开放题
    └── Agent_WorkBench 真实代码答辩
```

---

# 2. P0 / P1 / P2 / P3 总览

| 优先级 | 知识 | 总建议投入 | 掌握目标 |
|---|---|---:|---|
| P0 | Agent Loop、Tool Calling、Agent vs Workflow、ReAct | 4 h | 独立回答、画流程、结合项目、接 Debug 追问 |
| P0 | RAG、Chunk、Embedding、检索、Top-K、Hybrid | 4 h | 讲完整链路、参数取舍、排查质量问题 |
| P0 | Transformer、Attention、LLM/Token/Context | 3 h | 讲清主干原理，不追数学证明 |
| P0 | Python 高频基础与代码设计 | 3 h | 能解释项目中的类型、装饰器、异常、上下文管理 |
| P0 | Prompt、结构化输出、LLM API | 2 h | 能设计、约束、解析并处理失败 |
| P0 | Agent_WorkBench 项目答辩 | 每天 30 min | 3 分钟介绍与连续追问不脱离真实代码 |
| P0 | HTTP/REST/JSON、Git/Linux 基本操作 | 2 h | 能完成开发并回答高频基础题 |
| P1 | Memory、Planning、Evaluation、Trace、安全 | 3 h | 能做方案取舍和排查 |
| P1 | LangChain / LangGraph | 2 h | 懂抽象、适用场景；明确项目未使用它们 |
| P1 | FastAPI、async、数据库、SQLite/索引/事务 | 3 h | 能解释项目实现与扩展风险 |
| P1 | ML/DL/NLP 基础、训练 vs 推理、SFT/LoRA/RLHF | 3 h | 回答主干，不陷训练细节 |
| P1 | 数据结构算法基础 | 每天 30 min | 常见复杂度、Hash、栈队列、Top-K |
| P2 | Reranker、Query Rewrite、MCP、多 Agent | 2 h | 知道为什么用、代价与边界 |
| P2 | Docker、Redis、消息队列、部署、监控 | 2 h | 能给生产化方案 |
| P2 | vLLM、KV Cache、量化、批处理 | 1.5 h | 能解释推理优化直觉 |
| P3 | 分布式训练、DeepSpeed/Megatron、RL 算法细节 | 按 JD | 知道作用即可 |
| P3 | OS 内核、网络协议细枝末节、复杂算法竞赛题 | 按 JD | 不作为半月主线 |

---

# 3. 识别面试官到底在考什么

| 类型 | 常见开头 | 实际考察 | 回答结构 |
|---|---|---|---|
| A 定义题 | “什么是 RAG？” | 能否准确建立边界 | 一句话 + 目标 + 核心流程 |
| B 原理题 | “Attention 怎么算？” | 是否理解内部机制 | 输入 → 步骤 → 输出 → 作用 |
| C 为什么题 | “为何除以 √dk？” | 能否解释设计动机 | 原问题 → 后果 → 机制 → 取舍 |
| D 对比题 | “RAG 和微调区别？” | 是否会选型 | 目标、数据更新、成本、场景、组合 |
| E 项目题 | “你项目怎样做 RAG？” | 是否真正做过 | 真实调用链 + 参数 + 结果 + 局限 |
| F 代码题 | “这个装饰器做什么？” | 编码基本功 | 语法机制 + 项目作用 + 替代写法 |
| G Debug 题 | “Agent 重复调用怎么办？” | 分层定位能力 | 现象 → 指标/Trace → 根因层 → 修复/验证 |
| H 系统设计 | “设计企业知识 Agent” | 架构与取舍 | 需求 → 数据流 → 模块 → 非功能 → 评测 |
| I 开放题 | “Agent 最大问题？” | 判断力和边界意识 | 观点 + 证据 + 反例 + 工程措施 |

识别技巧：题目换说法，先判断它属于哪类，再调用对应回答结构，不要搜索脑中的“标准题原句”。

---

# 4. Python 与代码能力

## 4.1 Python 对象、可变性、拷贝与参数传递

**优先级：P0｜时间：40 分钟｜目标：独立回答并看懂项目状态变化｜【必须理解】**

学习状态：[ ] 未学习 [ ] 已看过 [ ] 已理解 [ ] 可以独立回答 [ ] 可以应对追问

### 一句话理解与例子

Python 变量保存对象引用；函数调用传递的是对象引用的赋值。修改可变对象内容会影响共享引用，重新绑定局部变量不会改变外部变量。

```python
def add_message(messages):
    messages.append({"role": "tool"})   # 修改原 list

def replace(messages):
    messages = []                        # 只重绑局部名字
```

### 为什么需要理解

Agent 的 `messages` 和 `trace` 在循环中原地追加。如果误以为每次都会自动复制，就会看不懂状态如何跨 step 积累；若多个请求共享同一个 list，还可能产生串话。

### 项目对应

【与你的 Agent_WorkBench 项目直接相关】`agent.py::Agent.run()` 每次调用新建局部 `messages/trace`，随后 `append()`；因此同一次 run 内共享状态，不同 run 不共享局部 list。Memory 则通过 SQLite 跨 run 持久化。

### 面试官可能怎么问

- 定义/代码：Python 参数是值传递还是引用传递？
- 对比：浅拷贝和深拷贝区别？
- 项目：你的 messages 会不会被不同用户共享？
- Debug：为什么修改嵌套 dict 后原对象也变了？

### 面试时怎么回答

**20 秒：** Python 采用对象引用传递或 call by sharing。形参和实参先指向同一对象；修改 list/dict 内容对外可见，给形参重新赋值不影响外部绑定。

**1 分钟：** 补充不可变对象、`copy.copy` 只复制外层、`copy.deepcopy` 递归复制，并说明深拷贝成本和不可复制资源。

**深入：** 联系 Agent 并发：不要把请求级可变状态放成全局变量；持久状态用 session key 隔离。

**易错：** 只回答“引用传递”不够严谨；Python 不是 C++ 意义的传引用。

## 4.2 迭代器、生成器、装饰器、上下文管理器

**优先级：P0｜时间：60 分钟｜目标：读懂代码、解释设计与替代实现｜【必须理解】**

### 一句话与例子

- Iterable：能产生迭代器；Iterator：实现 `__next__()`，记录遍历状态；
- Generator：用 `yield` 惰性地产生值；
- Decorator：接收函数/类并返回包装后对象；
- Context Manager：定义进入/退出资源边界，确保异常时也清理。

```python
@contextmanager
def connect():
    conn = sqlite3.connect("a.db")
    try:
        with conn:
            yield conn
    finally:
        conn.close()
```

### 技术发展的逻辑

手工 open/close 容易在异常分支泄漏资源；上下文管理器把“申请—使用—释放”封装为结构。手写注册/包装重复，装饰器把横切逻辑声明式附加在定义上。大数据一次构造 list 浪费内存，生成器按需产生。

### 项目对应

- `memory.py`、`tools.py`、`rag.py` 的 `_connect()` 使用 `@contextmanager`；
- `api.py` 的 `@app.get/@app.post` 是装饰器，把函数注册为路由；
- `ui.py` 的 `@st.cache_resource` 缓存重型组件；
- 项目工具没有使用 LangChain 的 `@tool`，而是显式 `Tool(...) + registry.register()`。

### 面试官可能怎么问

- `@contextmanager` 做了什么？为什么还需要 finally？
- 装饰器底层是什么？不用 `@` 能否实现？
- `@app.post` 为什么能让 FastAPI 发现函数？
- 生成器为什么省内存？有哪些限制？
- 项目为什么没用 `@tool`？

### 回答版本

**20 秒：** 装饰器本质是 `func = decorator(func)`；上下文管理器封装资源生命周期；生成器用 `yield` 保存执行状态并惰性返回。

**1 分钟：** 用项目连接管理说明：进入时创建连接，`yield` 给业务代码，离开时提交/回滚并在 finally close，即使抛异常也释放句柄。

**深入追问：** `with sqlite3.connect()` 主要管理事务，不一定及时关闭句柄；项目曾因此在 Windows 清理临时 DB 失败，后来显式 close。

## 4.3 面向对象、dataclass、Protocol 与依赖注入

**优先级：P0｜时间：45 分钟｜目标：结合架构回答｜【之前教学已涉及，需面试化复习】**

### 一句话与出现原因

OOP 将数据与行为组织为对象；`dataclass` 减少数据载体样板；`Protocol` 以“具备哪些方法”定义接口；依赖注入让对象从外部接收依赖而非内部写死，从而可替换、可测试。

### 项目例子与调用关系

```text
app.py::build_components()
→ 创建 OpenAICompatibleClient / ToolRegistry / MemoryStore
→ Agent(model=..., registry=..., memory=...)

contracts.py::ModelClient Protocol
├── OpenAICompatibleClient
├── OfflineDemoModel
└── tests::ScriptedModel
```

`ToolCall/ModelTurn/AgentResult/Chunk` 是数据契约；`frozen=True` 表达不可变意图。Agent 只依赖 `ModelClient.complete()`，不解析厂商 JSON。

### 面试问法与回答

- 为什么 tools/model 要传入而不是在 Agent 内创建？
- Protocol 和抽象基类区别？
- dataclass 解决什么问题？
- 新增模型供应商改哪里？

**30 秒：** 我用依赖注入把模型、工具注册表和 Memory 交给 Agent，Agent 面向 `ModelClient` 协议编程。真实、离线和测试模型都可替换，主循环不变。

**深入：** Protocol 支持结构化子类型，不强制继承；代价是运行时约束弱，仍需测试和类型检查。

## 4.4 异常、重试、日志与测试

**优先级：P0｜时间：45 分钟｜目标：应对工程追问｜【必须理解】**

### 核心体系

```text
可恢复工具错误 → {ok:false,error} → Observation → 模型决定下一步
LLM 网络/协议错误 → LLMRequestError / LLMProtocolError → API 502
非法用户输入 → ValueError → API 400
测试 → Fake 外部边界，真实执行本地控制流
日志 → Trace 记录 step/tool/arguments/result/latency/usage
```

重试只用于可能短暂恢复的错误，如 429、5xx、网络波动；认证失败或参数错误盲目重试只会放大问题。指数退避降低惊群，可再加入 jitter。

### 面试问法

- 什么时候重试？幂等性为什么重要？
- 为什么不能 `except Exception: pass`？
- 单元测试如何避免调用真实 LLM？
- 日志和 Trace 应记录什么，什么不能记录？

**回答主线：** 分类错误 → 决定恢复责任 → 结构化记录 → 验证。敏感 Key、个人数据和完整私有文档不能直接落日志。

## 4.5 Python 并发：线程、进程、async/await

**优先级：P1｜时间：60 分钟｜目标：回答 I/O 场景和项目局限｜【必须理解主干】**

### 一句话

- Thread：共享进程内存，适合阻塞 I/O；CPython GIL 限制纯 Python CPU 并行；
- Process：独立内存，可利用多核，启动和通信更重；
- Async：单线程协作式并发，任务在 `await` I/O 时让出执行权，适合大量网络等待。

### 项目对应

`api.py::upload_document()` 是 `async def`，因为 `UploadFile.read()` 可 await；`chat()` 是普通 `def`，而当前 `urllib` LLM 客户端和 SQLite 都是同步阻塞。FastAPI 会区别处理同步和异步路径。官方建议根据依赖是否可 await 选择 `def/async def`，不要把阻塞调用直接塞进事件循环：[FastAPI 并发说明](https://fastapi.tiangolo.com/async/)。

### 面试问法

- async 等于多线程吗？
- `async def` 中调用阻塞 HTTP 有什么问题？
- 什么时候用进程池？
- 项目怎样支持多个并发 LLM 请求？

**30 秒：** async 不是自动并行，而是在 I/O 等待点协作切换。若内部仍用同步 urllib 或 CPU-heavy embedding，直接 async 不会变快，甚至阻塞事件循环，应使用异步客户端、线程池或任务队列。

---

# 5. 计算机基础：只学高收益部分

## 5.1 数据结构与算法

**优先级：P1｜时间：每天 30 分钟｜目标：复杂度 + 常见题，不追竞赛难题｜【建议理解】**

必会：array/list、linked list、stack、queue、hash map/set、heap、tree/graph BFS/DFS、sort、binary search、Top-K。

项目映射：

- `ToolRegistry._tools` 用 dict：平均 O(1) 按 name 查工具；
- RRF 用 dict 按 chunk_id 聚合两路结果；
- `np.argsort` 排相似度；大规模 Top-K 可用 heap/专用 ANN，没必要全排序；
- Agent/Workflow 图常用节点与边；BFS/DFS 可用于检查可达性或循环。

高频问法：list 与 tuple；dict 原理和冲突；set 去重；Top-K 怎么做；排序复杂度；BFS vs DFS；递归风险。

回答不要只背 O(n)：说明 n 是什么、空间复杂度、数据规模和是否需要保持顺序。

## 5.2 HTTP / REST / JSON / API

**优先级：P0｜时间：60 分钟｜目标：独立回答并结合 LLM API｜【必须理解】**

### 一句话与例子

HTTP 是请求—响应应用层协议；REST 是以资源和标准动词组织接口的设计风格；JSON 是常见数据表示；API 是系统之间约定的调用契约。

```text
POST /chat
Headers: Content-Type, Authorization
Body: {message, session_id}
→ 200 {answer, steps, trace}
```

### 为什么出现

不同语言/进程/机器需要稳定边界，不能直接调用彼此内存中的函数。HTTP + JSON 提供通用传输，OpenAPI/Schema 提供可读契约。

### 必会状态码

- 200 成功；201 创建；204 成功无 body；
- 400 请求非法；401 未认证；403 无权限；404 不存在；409 冲突；
- 413 过大；415 媒体类型不支持；429 限流；
- 500 服务内部错误；502 上游服务失败；503 暂不可用；504 上游超时。

### 项目对应

`api.py` 的 `/chat`、`/documents/*`、`/memory/{session_id}`；`llm_client._post()` 是下游 HTTP 客户端。Tool Calling 的 JSON Schema 是“模型—应用”内部契约，REST 是“外部客户端—服务”契约，两者层级不同。

### 问法与回答

- GET 与 POST 区别，GET 能否有 body？
- PUT vs PATCH？幂等是什么意思？
- 401 vs 403，502 vs 500？
- Authorization Key 应放哪里？
- 超时、重试、限流如何处理？

**30 秒：** 我的 API 用 Pydantic 校验 HTTP JSON，再调用统一业务层；LLM 上游失败映射 502，非法输入映射 400。对 429/5xx 和网络波动做有限重试，但写操作重试前要考虑幂等性。

## 5.3 数据库：SQL、索引、事务与 SQLite

**优先级：P1｜时间：60 分钟｜目标：结合 Store 回答｜【必须理解主干】**

关系数据库把结构化数据放入表；索引用额外空间加速查找；事务强调 ACID；参数化 SQL 防注入。

项目中：

- `messages` 表按 session_id 查询，但当前未建复合索引；数据增大后可建 `(session_id,id)`；
- `chunks.chunk_id` 是主键，source 更新先 DELETE 再 INSERT，事务保证原子性；
- `todos.id` 自增主键；
- SQL 参数使用 `?` 占位，不拼接用户值；
- SQLite 适合单机 MVP，不适合高并发多实例共享写入。

面试问法：什么是事务/ACID？索引为何快、代价是什么？主键/唯一索引区别？SQL 注入？SQLite 与 PostgreSQL？为何显式 close？

**1 分钟回答：** 先说数据模型，再说查询模式决定索引，事务保护多步更新，参数化防注入；最后说明项目规模扩大后迁移 PostgreSQL/连接池，并把向量检索交给 pgvector/Milvus。

## 5.4 Git、Linux、操作系统与网络

**优先级：P0 基础操作 + P1 原理｜时间：90 分钟｜目标：能开发和排错｜【可以背诵命令，必须理解危险操作】**

### Git 必会

工作区 → 暂存区 → 本地 commit → remote。能解释 branch、merge、rebase、conflict、HEAD、`.gitignore`；会用 `status/diff/add/commit/log/branch/pull/push`。不要把 API Key 提交；删除当前文件不等于从历史中删除秘密，泄漏后应立即轮换。

### Linux 必会

`pwd/ls/cd/cp/mv/rm/mkdir`、`cat/less/head/tail`、`rg/grep/find`、`ps/top/kill`、`curl`、`chmod`、环境变量、管道和重定向、端口排查。知道进程与线程、文件描述符、SIGTERM vs SIGKILL。

### 网络必会

DNS → TCP/TLS → HTTP；IP 定位主机，端口定位进程。TCP 可靠有序，UDP 无连接低开销。HTTPS 是 HTTP over TLS，提供加密、完整性和身份验证。无需在半个月里背 TCP 状态机所有细节。

### 高频问法

- `git merge` vs `rebase`；Key 已提交怎么办？
- 进程和线程区别；什么是上下文切换？
- TCP vs UDP；三次握手为什么不是两次？
- 域名访问服务经过什么过程？
- Linux 服务占用端口/日志持续输出怎么查？

### 项目结合

公开仓库使用 Git；`.env` 在 `.gitignore`；API 监听 `127.0.0.1:8000`；调用学校服务需要 DNS/TLS/HTTP；JSONL 日志可用 `tail` 持续查看。

---

# 6. ML / DL / NLP 基础

## 6.1 机器学习主干

**优先级：P1｜时间：60 分钟｜目标：回答基础而不展开证明｜【建议理解】**

### 一句话与出现逻辑

机器学习不是手写所有规则，而是从数据中学习参数，使模型对未见数据也能完成预测。训练集拟合参数，验证集选模型/超参，测试集只做最终无偏估计。

必须理解：监督/无监督/自监督；分类/回归；loss；gradient descent；learning rate；epoch/batch；过拟合/欠拟合；regularization；precision/recall/F1。

### 例子

垃圾邮件分类：文本和标签训练 → 最小化交叉熵 → 验证集调超参 → 测试集评估。若正例稀少，只看 accuracy 会掩盖漏检，应看 precision/recall/F1。

### 面试问法

- 过拟合怎样判断和缓解？
- Precision 与 Recall 如何取舍？
- 训练/验证/测试为何分开？
- 梯度下降、学习率和 batch size 的影响？

**回答主线：** 定义 → 观测现象 → 原因 → 数据/正则/早停/模型复杂度等措施 → 用验证集确认。

## 6.2 深度学习与 NLP 主干

**优先级：P1｜时间：60 分钟｜目标：给 Transformer 铺路｜【必须理解主干】**

神经网络通过多层可微变换学习表示；前向计算预测，loss 衡量差异，反向传播用链式法则求梯度，优化器更新参数。激活函数引入非线性；残差连接改善深层网络训练；LayerNorm 稳定特征尺度。

NLP 的历史逻辑：手工特征/词袋缺上下文 → Word2Vec 等静态词向量“一词一向量” → RNN 按序处理但难并行、长依赖困难 → Attention 动态聚合上下文 → Transformer 并行处理序列并扩展到大规模预训练。

高频问法：反向传播是什么？ReLU 为什么常用？BatchNorm vs LayerNorm？Word2Vec 与上下文 Embedding？RNN/LSTM 的问题？

半月边界：理解直觉和作用；不投入时间手推复杂梯度。

---

# 7. Transformer 与 Attention

## 7.1 Transformer 总体结构

**优先级：P0｜时间：2～3 小时（含 Attention）｜目标：可画图、讲原理、接常见追问｜【必须理解】**

学习状态：[ ] 未学习 [ ] 已看过 [ ] 已理解 [ ] 可以独立回答 [ ] 可以应对追问

### 一句话理解

Transformer 用 Attention 让每个 token 动态读取其他 token 的信息，再通过前馈网络逐位置变换；残差、归一化和位置表示使深层训练与序列顺序成为可能。

### 具体例子

“小明把书给小红，因为她要复习。”处理“她”时，模型可给“小红”较高注意力，而不是只能依赖固定窗口或按顺序压缩到一个隐藏状态。

### 为什么出现

```text
RNN/LSTM 按时间步串行
→ 训练难并行，长距离信息传递路径长
→ Attention 可直接连接任意位置
→ Transformer 去掉 recurrence，以 Attention 为核心
→ 更易并行、扩展数据和参数规模
```

原始 Transformer 论文提出基于 Attention、无需 recurrence/convolution 的架构，并强调并行训练优势：[Attention Is All You Need](https://arxiv.org/abs/1706.03762)。

### 知识体系位置

```text
Deep Learning
└── Sequence Model
    └── Transformer
        ├── Token Embedding + Position
        ├── Multi-Head Attention
        ├── Feed-Forward Network
        ├── Residual + LayerNorm
        └── Encoder / Decoder / Mask
```

### 面试时怎么回答

**20 秒：** Transformer 是基于 Attention 的序列模型。每层通过多头注意力聚合上下文，再经过前馈网络，并用残差、LayerNorm 和位置编码稳定训练、保留顺序。

**1 分钟：** 补充 Encoder 双向 self-attention；Decoder 使用 causal mask，只看当前位置之前 token；相比 RNN 更易并行和建模长依赖，但标准 Attention 随序列长度约 O(n²)。

**深入：** 说明 QKV、scaled dot-product、multi-head、mask、FFN、残差和推理 KV cache；不要声称 Attention “无限长”或完全解决长上下文。

### 面试官可能怎么问

- 定义：介绍 Transformer；
- 原理：一层内部经过什么？
- 为什么：为何比 RNN 更适合大模型？
- 对比：Encoder/Decoder、BERT/GPT 区别？
- 性能：长上下文瓶颈是什么？
- 项目：你只调用 API，为什么还要懂 Transformer？

项目回答：虽然 Agent_WorkBench 不训练模型，但 Token 预算、上下文构造、生成随机性、KV cache/延迟和模型能力边界都来自底层模型特性，应用选型和排错需要这些知识。

## 7.2 Scaled Dot-Product Attention 与 QKV

**优先级：P0｜时间：60 分钟｜目标：解释公式每一项｜【必须理解】**

```text
Attention(Q,K,V) = softmax(QKᵀ / √dk) V
```

- Q（Query）：当前位置想找什么；
- K（Key）：每个位置可用什么来被匹配；
- V（Value）：真正被加权汇总的信息；
- QKᵀ：匹配分数；
- softmax：转为归一化权重；
- 权重乘 V：得到上下文表示。

例子：搜索系统中 query 像 Q，文档索引特征像 K，文档内容像 V。只是直觉类比，不等同于数据库检索实现。

### 为什么除以 √dk

维度变大时点积方差增大，softmax 更容易饱和，梯度变小。缩放让数值分布更稳定。回答“防止梯度爆炸”过于粗糙，应说 softmax 饱和和训练稳定性。

### Multi-Head 为什么需要

把表示投影到多个子空间，各 head 可学习不同关系，再拼接投影。它提升表达多样性，但不保证每个 head 都有可解释语义。

### Self vs Cross Attention

- Self-Attention：Q/K/V 来自同一序列；
- Cross-Attention：Q 来自一条序列，K/V 来自另一条表示，典型是 Encoder-Decoder；
- GPT 类 Decoder-only 主要使用 masked self-attention，并非经典 encoder-decoder cross-attention。

## 7.3 Position、Mask、Encoder 与 Decoder

**优先级：P0｜时间：45 分钟｜目标：接结构追问｜【必须理解】**

Attention 本身对排列不敏感，需要位置编码/位置嵌入表达顺序。Causal mask 屏蔽未来 token，保证自回归训练和生成不偷看答案。Padding mask 忽略补齐位置。

- Encoder-only（如 BERT）：双向上下文，适合理解/分类/抽取；
- Decoder-only（如 GPT）：因果预测下一个 token，适合生成并可通过提示统一多任务；
- Encoder-Decoder（如 T5）：输入编码后由 Decoder 条件生成，适合 seq2seq。

### 高频题卡

| 问题 | 核心回答 | 易错点 / 追问 |
|---|---|---|
| 为什么比 RNN 易并行？ | 训练时所有位置的 QKV 可矩阵并行 | 自回归推理仍逐 token |
| Attention 复杂度？ | 标准 full attention 时间/内存约随 n² 增长 | 还要考虑 hidden/head/batch |
| QKV 从哪来？ | 输入表示分别乘可学习投影矩阵 | 不是三个原始句子 |
| 为何多头？ | 多子空间并行建模不同关系 | 不是简单重复同一 head |
| GPT 为何 Decoder-only？ | 因果 LM 与生成任务统一、规模扩展简单 | 不代表 Encoder 无价值 |
| LayerNorm 作用？ | 稳定特征尺度和优化 | 不等同 BatchNorm |

### Transformer 追问树

```text
Transformer
├── 为什么替代 RNN？→ 并行、长依赖、扩展性
├── Attention
│   ├── Q/K/V 从哪来？
│   ├── 为什么 √dk？
│   ├── Multi-Head？
│   └── O(n²) 怎么办？
├── 顺序 → Positional Encoding / RoPE
├── Mask → causal / padding
├── 结构 → Encoder / Decoder / Encoder-Decoder
└── 推理 → autoregressive / KV cache / sampling
```

---

# 8. LLM 基础：Token、训练、推理与能力边界

## 8.1 Token、Tokenization 与 Context Window

**优先级：P0｜时间：45 分钟｜目标：结合成本和 Memory 回答｜【必须理解】**

### 一句话与例子

Token 是 tokenizer 切分文本后的离散 ID，不一定等于一个字或单词。Context window 是单次请求中输入与输出可处理 token 的总范围。

“Agent_WorkBench”可能被切为多个子词；不同模型 tokenizer 不同，同一文本 token 数不同。因此不能用“字符数=token 数”精确估算。

### 为什么需要 Tokenization

模型只能处理有限词表中的整数 ID。按词词表巨大且 OOV，按字符序列过长；BPE/Unigram 等子词方法在词表大小与序列长度间折中。

### 项目对应

`MemoryStore.recent()` 当前用 JSON 字符数近似 token budget，简单但不精确。改进是在发送前使用目标模型 tokenizer 计算 system/history/tools/query/output reserve，并做摘要或检索式 Memory。

### 面试问法与回答

- Token 和词有什么区别？中文一个字一个 token 吗？
- 上下文超限怎么办？
- Context 越长越好吗？
- 为什么工具 Schema 也消耗 token？

**30 秒：** Token 是模型词表单位，context 包括 system、历史、工具 schema、检索上下文和输出。超限要裁剪、摘要、检索相关历史、减少工具描述并预留输出预算；长上下文还增加成本和延迟，也可能稀释注意力。

## 8.2 Pretraining、SFT、RLHF/DPO、LoRA

**优先级：P1｜时间：75 分钟｜目标：能比较，不深挖训练工程｜【建议理解】**

```text
Pretraining：海量数据自监督预测 token → 获得通用语言/知识能力
SFT：高质量指令-回答监督训练 → 学会遵循任务格式
Preference Alignment：人类/AI 偏好数据 → 更符合偏好与安全目标
LoRA：冻结大部分权重，只训练低秩增量 → 降低微调成本
```

RLHF 通常包含偏好数据、奖励模型和强化优化；DPO 直接在偏好对上优化相对偏好，流程更简单。面试中不要把所有对齐都称为 RLHF。

### Fine-tuning vs RAG

| 维度 | Fine-tuning | RAG |
|---|---|---|
| 主要改变 | 模型参数/行为 | 推理时上下文 |
| 适合 | 风格、格式、领域行为、特定能力 | 新鲜/私有/可引用事实 |
| 更新 | 需再训练/适配 | 更新索引即可 |
| 可追溯 | 较弱 | 可提供来源 |
| 成本 | 训练与维护较高 | 检索与上下文成本 |
| 可组合 | 可以 | 可以；常见组合是微调行为 + RAG 知识 |

### 面试问法

- 预训练与微调区别？
- SFT 与 RLHF/DPO 各解决什么？
- LoRA 为什么省参数？
- 公司知识为什么优先 RAG 而不是微调？

## 8.3 推理、Sampling、Temperature 与幻觉

**优先级：P0｜时间：45 分钟｜目标：解释生成和稳定性｜【必须理解】**

LLM 推理通常自回归：根据已有 token 计算下一个 token 概率，选择后继续。Temperature 调整 logits 分布锐度；top-k 只在概率最高 k 个采样；top-p 选择累计概率达到阈值的最小集合。

低 temperature 通常更稳定，不等于事实正确；temperature=0 也可能因服务实现、并行或模型更新出现差异。幻觉来自模型目标是生成高概率文本而非查询事实数据库，也可能由错误上下文、模糊提示或检索失败触发。

减幻觉是分层工程：需要事实就检索/调用工具；限制只基于证据回答；引用；结构化输出与校验；不确定时拒答；评测和人工兜底。RAG 只能提供证据，不能保证模型正确使用证据。

## 8.4 Embedding vs Token vs Hidden State

**优先级：P0｜时间：30 分钟｜目标：避免概念混淆｜【必须理解】**

| 概念 | 是什么 | 典型用途 |
|---|---|---|
| Token | 离散文本单位/ID | 模型输入输出与计费 |
| Token Embedding | token ID 查表得到的向量 | Transformer 初始表示 |
| Hidden State | 每层结合上下文后的 token 表示 | 模型内部计算 |
| Sentence/Document Embedding | 整段文本的固定维向量 | 语义检索、聚类、相似度 |

同一个词在输入 embedding 层可能相同，但不同上下文后的 hidden state 不同。RAG 的 BGE embedding 是专门用于文本相似度的段落向量，不是简单拿生成模型某个 token 的输入向量。

### LLM 追问树

```text
LLM
├── 输入 → tokenizer / token / context window
├── 模型 → Transformer Decoder / causal mask
├── 训练 → pretrain / SFT / preference alignment / LoRA
├── 推理 → autoregressive / temperature / top-k / top-p
├── 性能 → KV cache / batching / quantization
└── 局限 → hallucination / stale knowledge / prompt injection / cost
```

---

# 9. Prompt、结构化输出与 LLM API

## 9.1 Prompt / System Prompt / Context Engineering

**优先级：P0｜时间：60 分钟｜目标：设计、解释、调试｜【必须理解】**

学习状态：[ ] 未学习 [ ] 已看过 [ ] 已理解 [ ] 可以独立回答 [ ] 可以应对追问

### 一句话和例子

Prompt 是发给模型的指令与上下文；System Prompt 定义高优先级角色和规则；Context Engineering 更广，关注在正确时机向模型提供正确的指令、历史、工具、检索证据和状态。

```text
System：需要外部事实必须调用工具；引用来源；不得虚构成功
History：用户上一轮目标
Tool schemas：当前允许的能力
Retrieved context：知识证据
User：本轮问题
```

### 为什么出现

预训练模型是通用概率模型，不知道当前任务、输出格式、权限和业务数据。Prompt 在不改参数的情况下提供任务约束；但复杂应用仅靠提示不可靠，因此还需要 Schema、校验、权限和代码工作流。

### 项目对应

【与你的 Agent_WorkBench 直接相关】`prompts.py::SYSTEM_PROMPT` 管理行为规则；`Agent.run()` 将其置于 messages 首位；`registry.schemas()` 和 Memory/RAG 共同构成完整上下文。Prompt 负责“建议如何做”，Registry 白名单与 max_steps 负责硬边界。

### 面试官可能怎么问

- Prompt Engineering 是什么？System/User Prompt 区别？
- Zero-shot、Few-shot、CoT 各是什么？
- 为什么 Prompt 有效但不可靠？
- 如何减少 Prompt Injection？
- 项目 Prompt 如何迭代？怎样评测而不是凭感觉？

### 面试回答

**20 秒：** Prompt Engineering 是通过指令、示例、上下文和输出约束，让通用模型稳定完成特定任务；System Prompt 放全局规则，但不能当安全机制。

**1 分钟：** 好 Prompt 应明确角色、目标、输入边界、工具使用、输出格式、失败行为并提供必要例子；用固定 case 回归。涉及外部动作时再用 Schema 校验、权限和确定性代码兜底。

**深入：** 说明注入防御：把外部内容视为数据、分隔信任域、工具最小权限、敏感操作确认、输出验证、不可只写“忽略恶意指令”。

## 9.2 Structured Output / JSON Schema / Function Calling

**优先级：P0｜时间：45 分钟｜目标：区分生成约束和执行安全｜【必须理解】**

结构化输出让模型按约定字段生成机器可处理数据；JSON Schema 描述类型、必填、枚举、范围；Function Calling 通常让模型返回函数名和参数，由应用执行。

项目中同一 Schema 两次发挥作用：先随 LLM 请求指导生成，再由 `Draft202012Validator` 在执行前校验。即使供应商声称严格 JSON，也不应跳过应用校验。

**Function Calling vs Tool Calling：** 业界常混用。Function Calling 强调结构化函数调用协议；Tool Calling 是更广概念，可包括函数、检索、API、代码执行等。项目里的五个 tool 最终都是 Python callable。

### 面试问法

- JSON mode 与 Function Calling 区别？
- Schema 中 default 会自动填入吗？
- 模型返回不存在的 tool 怎么办？
- arguments 为什么还要校验？
- call_id 有什么作用？

## 9.3 LLM API 工程

**优先级：P0｜时间：45 分钟｜目标：调用、重试、成本、安全｜【必须理解】**

必须会：messages roles、model、tools/tool_choice、timeout、rate limit、usage、streaming、重试、错误解析、Key 管理。

项目 `llm_client.py` 使用 OpenAI-compatible Chat Completions：内部 dict → JSON bytes → Authorization header → response JSON → ModelTurn。429/5xx 和网络错误有限重试；坏 JSON 是协议错误。

流式输出可降低首 token 延迟，但工具调用参数可能分 chunk 到达，需要增量拼接；项目当前非流式。成本粗略由输入/输出 token 和模型单价决定；优化顺序通常是减少无关上下文/重复调用、缓存、选择合适模型，再谈复杂架构。

---

# 10. Embedding 与 Vector Database

## 10.1 Embedding

**优先级：P0｜时间：60 分钟｜目标：解释模型、相似度和选型｜【之前教学已涉及】**

### 一句话和例子

Embedding 把文本映射为固定维向量，使语义相近文本在向量空间更接近。例如“报销交通费标准”和“差旅交通如何报销”关键词不完全相同，但向量可能接近。

### 为什么出现

关键词检索依赖字面重合，难处理同义改写；预训练表示把语义压缩到向量，便于相似度搜索。它不是事实判断器，领域、语言和训练目标不匹配时也会召回错误。

### 工作流程

```text
documents → embedding model → vectors
query → 同一个 embedding model → query vector
→ cosine/dot/L2 → nearest neighbors
```

文档和 query 必须用兼容模型/版本/归一化方式；换模型通常要重建索引。

### 项目对应

`rag.py::FastEmbedRetriever` 用 BGE-small-zh-v1.5 生成 512 维向量，`cosine_similarity` 排序；`LocalVectorRetriever` 是字符 n-gram TF-IDF 基线。模型类缓存避免重复加载，但向量矩阵每次入库全量重建。

### 面试官可能怎么问

- Embedding 是什么，与 token embedding 区别？
- 模型怎样选：语言、领域、维度、速度、许可证、benchmark？
- cosine/dot/L2 区别？向量是否需归一化？
- 中文检索有什么注意？
- 换 embedding 模型为什么重建索引？

### 回答版本

**20 秒：** 文本 Embedding 是用于语义比较的固定维向量；query 和文档用同一模型编码，再按相似度召回。

**1 分钟：** 加上选型维度和离线评测；不能只看公开榜，要用业务 query/source 计算 Recall/Hit/MRR、延迟和成本。

**深入：** Bi-Encoder 预先编码文档、检索快；Cross-Encoder 联合读取 query-document，精度高但不能全库逐一计算，适合 rerank 小候选集。

## 10.2 Vector Database

**优先级：P0/P1｜时间：45 分钟｜目标：会与普通数据库比较和选型｜【必须理解】**

### 一句话

向量数据库存储向量和元数据，并通过 ANN 索引在大规模数据中近似查找最近邻，同时提供过滤、更新、持久化和服务能力。

### 为什么出现

小数据可在内存对所有向量做精确相似度；百万级时全扫描成本高，于是使用 HNSW、IVF 等近似索引，以少量召回损失换速度和规模。

### Vector DB vs 普通数据库

| 维度 | 向量数据库 | 关系数据库 |
|---|---|---|
| 核心查询 | 相似度 Top-K | 精确条件/Join/事务 |
| 索引 | HNSW/IVF 等 ANN | B-tree/hash 等 |
| 数据 | vector + metadata | 结构化行列 |
| 强项 | 语义近邻 | 一致性、事务、复杂查询 |
| 可同时用 | 可以；pgvector 在 PostgreSQL 内结合两者 | 可以作为元数据/业务库 |

### 项目对应

项目没有独立向量数据库：Chunk 放 SQLite，BGE 矩阵驻内存并精确排序。面试必须诚实。小规模简单可复现；规模扩大可迁移 pgvector/Milvus/Weaviate，考虑索引参数、过滤、更新一致性、备份和多租户。

### 面试问法

- FAISS 是数据库吗？（更准确是相似度搜索库，缺少完整 DB 服务能力。）
- HNSW/IVF 是什么，参数怎样影响 recall/latency/memory？
- 向量库如何做 metadata filter？
- 为什么项目没用 Milvus？什么时候该换？

---

# 11. RAG：从文档到可引用答案

## 11.1 RAG 完整知识卡

**优先级：P0｜时间：3～4 小时｜目标：独立画链路、解释参数、排查问题｜【之前教学已涉及，需面试化复习】**

学习状态：[ ] 未学习 [ ] 已看过 [ ] 已理解 [ ] 可以独立回答 [ ] 可以应对追问

### 一句话理解

RAG 在生成前从外部知识库找相关证据，把证据连同问题交给 LLM，使回答能使用新鲜、私有且可追溯的信息。

### 具体例子

```text
“公司的报销标准是什么？”
→ query 处理/Embedding
→ 从制度库召回相关 Chunk
→ 可选 Rerank
→ Prompt 放入证据和问题
→ LLM 基于证据回答并引用来源
```

### 为什么出现

```text
纯 LLM：知识截止、无公司私有数据、容易编造、难给来源
→ 直接塞全部文档：上下文超限、成本高、噪声大
→ RAG：只取与当前问题相关的小部分证据
```

RAG 降低但不消灭幻觉：错误召回、缺失证据、Prompt 冲突、模型忽略证据都可能失败。

### 知识体系位置

```text
RAG
├── Offline ingestion
│   ├── Load / OCR / Clean / Deduplicate
│   ├── Chunk / Metadata
│   └── Embedding / Index
└── Online query
    ├── Query rewrite / route
    ├── Sparse + Dense retrieve
    ├── Filter / Hybrid / Rerank
    ├── Context assemble
    ├── Generate / Citation
    └── Evaluate / Feedback
```

### 项目完整映射

【与你的 Agent_WorkBench 直接相关】

```text
rag.py::DocumentLoader.load()
→ TextChunker.split()
→ SQLiteChunkStore.replace_source()
→ HybridKnowledgeBase._reload()
→ BM25Retriever + FastEmbedRetriever

tools.py::create_registry()
→ handler=knowledge.search
→ Agent.run() 执行 search_knowledge
→ role=tool Observation
→ LLM 生成带 citation 答案
```

为什么这样实现：段落优先加 overlap 降低边界损失；SQLite 保存可重建 Chunk；BM25 与 BGE 互补；RRF 避免直接相加不同量纲分数；citation 由应用确定生成。

替代方案：递归/语义/标题感知 Chunk；pgvector/Milvus；learned sparse；Cross-Encoder rerank；multi-query/hyde/query rewrite；parent-child retrieval；GraphRAG。

### 面试官可能怎么问

**直接：** 什么是 RAG？介绍完整流程。

**原理：** 为什么减少幻觉？Embedding/Chunk/Retriever 各作用？

**为什么：** 为什么不把全部文档放 Prompt？为什么不用微调？

**对比：** Sparse vs Dense；Bi-Encoder vs Cross-Encoder；RAG vs Fine-tuning。

**项目：** Chunk size/overlap 为什么这样设？Top-K 为何 3？为什么用 BGE？为什么 Hybrid 权重 1.4/1.0？

**Debug：** 检索不到、召回正确但回答错、文档越来越大分别怎么办？

**系统设计：** 设计企业内部知识问答 Agent。

### 面试回答版本

**20 秒：** RAG 是检索增强生成：先从外部知识库检索相关 Chunk，再把证据交给 LLM 回答并引用来源，适合新鲜、私有、需可追溯的知识。

**1 分钟：** 文档先解析、清洗、切块、向量化和索引；查询时可改写，使用关键词/向量混合召回，必要时 rerank，组装上下文后生成和引用；效果要分别评估检索和答案。

**深入：** 加上 chunk/top-k 取舍、hybrid/rerank、权限过滤、索引更新、context budget、拒答、离线/在线指标与项目真实结果。

## 11.2 Chunk / Top-K / Overlap

**优先级：P0｜时间：45 分钟｜【必须理解取舍】**

- Chunk 太小：语义不完整、上下文碎片化；
- 太大：向量主题混合、噪声和 token 成本高；
- Overlap：缓解边界切断，但引入重复和索引成本；
- Top-K 太小：漏召回；太大：噪声、成本、lost-in-the-middle；
- 参数必须用业务数据评测，不能说“行业统一 500/5”。

项目用 500 字符、80 overlap、默认 top_k=3；它是小知识库可解释起点，不是普适最优。20 条检索集用于回归。

## 11.3 Sparse / Dense / Hybrid / Reranker

**优先级：P0/P1｜时间：60 分钟｜【必须理解】**

- Sparse（BM25）：精确词项、专有名词强，可解释；
- Dense（Embedding）：语义改写强，受模型领域匹配影响；
- Hybrid：合并两者候选；RRF 用排名融合，避免分数尺度问题；
- Reranker：联合读取 query 与候选文档精排，质量高但更慢，通常只排初召回几十条。

## 11.4 RAG Evaluation

**优先级：P1｜时间：45 分钟｜【必须理解分层】**

```text
检索层：Recall@K / Hit@K / MRR / nDCG
生成层：faithfulness / answer relevance / correctness / citation accuracy
系统层：latency / cost / failure rate / user task success
```

先看“证据是否召回”，再看“模型是否正确使用”。否则最终答错时无法判断是检索还是生成问题。

### RAG 追问树

```text
RAG
├── 为什么需要？→ 私有/新鲜/引用 vs 幻觉
├── Ingestion
│   ├── 解析/OCR/清洗
│   ├── Chunk size/overlap/metadata
│   └── Embedding/index/update
├── Retrieval
│   ├── BM25 vs Dense
│   ├── Top-K / similarity / filter
│   ├── Hybrid / RRF
│   └── Reranker / query rewrite
├── Generation
│   ├── context placement/token budget
│   ├── citation/refusal
│   └── prompt injection
└── Evaluation
    ├── retrieval metrics
    ├── answer faithfulness
    └── latency/cost
```

### 高频题模板

| 问题 | 核心考点 | 一句话答案 | 易错点 |
|---|---|---|---|
| RAG 为何减幻觉？ | grounding | 提供可验证证据并约束基于证据回答 | 不能说完全消除 |
| Chunk size 怎么定？ | trade-off + eval | 按文档结构、问题粒度、模型限制用数据调 | 不背固定数值 |
| Top-K 怎么定？ | recall/noise/cost | 用 Recall@K 与答案指标联合选 | 越大不越好 |
| 为什么 Hybrid？ | sparse+dense 互补 | 专名和语义改写兼顾 | 要说明融合方式 |
| 召回对但答案错？ | generation layer | 查上下文排序、Prompt、冲突、模型遵循和引用 | 不要继续盲调向量库 |

---

# 12. Agent、Tool Calling、Memory 与 Workflow

## 12.1 Agent 核心知识卡

**优先级：P0｜时间：2～3 小时｜目标：画 Loop、解释边界、结合项目连续追问｜【必须理解】**

学习状态：[ ] 未学习 [ ] 已看过 [ ] 已理解 [ ] 可以独立回答 [ ] 可以应对追问

### 一句话理解

LLM Agent 是由模型根据目标和当前状态选择下一步行动，应用执行工具并把结果作为 Observation 返回，循环直到完成或触发停止条件的系统。

### 具体例子

```text
“查 Tool Calling 的定义并创建复习待办”
→ LLM 选择 search_knowledge
→ 应用检索并回传结果
→ LLM 选择 add_todo
→ 应用写数据库并回传结果
→ LLM 汇总答案
```

### 为什么出现

普通 Chatbot 只生成文本；固定 Workflow 的步骤预先确定。当任务需要根据中间结果动态选择不同工具和步骤时，引入 Agent。Agent 不是“更高级就一定更好”，它增加随机性、延迟、成本和安全风险。

### 知识体系位置

```text
Agent Runtime
├── Model / Prompt
├── State / Context
├── Planning / Policy
├── Tools / Environment
├── Observation
├── Memory
├── Stop / Guardrail
└── Trace / Evaluation
```

### Agent_WorkBench 对应代码

【与你的项目直接相关】

```text
agent.py::Agent.run()
├── memory.recent() + current user → messages
├── model.complete(messages, registry.schemas()) → ModelTurn
├── no tool_calls → final answer
└── tool_calls
    ├── ToolRegistry.execute()
    ├── tool_result_message() → Observation
    └── 回到 model.complete()
```

项目没有独立 `Planner` 类：planning 是模型每轮返回 `ModelTurn`。没有 LangGraph：循环是显式 Python `for`。这种实现便于解释协议和控制流，但复杂分支、持久 checkpoint、人审中断会更难维护。

### 面试官可能怎么问

- 定义：什么是 Agent？和 Chatbot 区别？
- 原理：Agent Loop 怎么运行？状态是什么？
- 为什么：什么时候需要 Agent，什么时候不用？
- 对比：Agent vs Workflow；单 Agent vs Multi-Agent；ReAct vs Tool Calling。
- 项目：主循环代码在哪？规划在哪里？如何停止？
- Debug：重复工具、错误参数、工具失败怎么办？
- 系统：如何给多个 API 的 Agent 做权限控制？

### 面试回答

**20 秒：** Agent 是“模型决策 + 工具执行 + Observation 回传”的闭环，能根据中间结果动态选择下一步；固定步骤更适合 Workflow。

**1 分钟：** 说明目标进入 messages，模型读取 tool schemas 返回结构化调用，应用白名单校验执行并用 call_id 回传结果，循环到无 tool_calls 或达到上限；Memory、Trace 和 guardrail 分别处理上下文、可观测性与安全。

**深入：** 加上 deterministic shell + probabilistic policy 的观点：外层控制流、权限、校验、停止由代码确定，路径选择由模型决定；讨论可靠性、成本和可评估性。

## 12.2 Agent vs Chatbot vs Workflow

**优先级：P0｜时间：30 分钟｜【必须理解】**

| 维度 | Chatbot | Workflow | Agent |
|---|---|---|---|
| 核心 | 对话生成 | 预定义节点/分支 | 模型动态选动作 |
| 路径 | 通常单次/多轮文本 | 开发者确定 | 运行时不完全确定 |
| 工具 | 可无 | 节点固定调用 | 模型选择调用 |
| 可靠性 | 取决于生成 | 较可控 | 需强 guardrail/eval |
| 适合 | 闲聊、问答 | 审批、ETL、稳定业务流程 | 开放任务、步骤依结果变化 |

可以组合：Workflow 的某个节点是 Agent，Agent 外层由 Workflow 控制审批和预算。面试官问这个是看你会不会“为了 Agent 而 Agent”。

## 12.3 Tool / Function Calling

**优先级：P0｜时间：75 分钟｜目标：讲清协议、代码和安全｜【之前教学已涉及】**

### 一句话与出现原因

Tool Calling 让模型产生“调用哪个能力、传什么参数”的结构化意图；应用验证并执行。纯自然语言解析脆弱，模型也不能直接可信地操作真实系统，因此需要 Schema 和受控执行器。

### 完整协议

```text
Tool(name, description, JSON Schema, handler)
→ schemas 发送给 LLM
→ ToolCall(name, arguments, call_id)
→ Registry 白名单查找 + Schema 二次校验
→ handler(**arguments)
→ {ok,data/error}
→ role=tool + tool_call_id
→ LLM 再决策
```

### 项目关键位置

- `tools.py::Tool.schema()`：模型看到的契约；
- `ToolRegistry._tools`：工具白名单 dict；
- `ToolRegistry.execute()`：校验与异常包装；
- `create_registry()`：五个工具绑定实际 handler；
- `contracts.py::ToolCall`：内部数据结构；
- `agent.py::run()`：执行与 Observation；
- `llm_client.py::complete()`：解析供应商 tool_calls。

### 面试问法

- 工具描述怎样影响选择？Schema 为什么还要应用校验？
- call_id 为什么必要？一轮多个工具怎样对应？
- 工具失败应抛异常还是返回 Observation？
- 如何避免模型调用危险工具？
- `@tool` 装饰器做什么？不用能否实现？

**30 秒：** 模型只提出调用，不直接执行。应用用 Registry 白名单和 JSON Schema 校验参数，再调用 handler，把结果以相同 call_id 回传。危险工具还需权限、最小作用域、确认、审计和幂等设计。

### Tool Calling 追问树

```text
Tool Calling
├── Schema → name/description/properties/required/enum
├── Selection → model/tool_choice/router
├── Execution → registry/validation/handler
├── Correlation → call_id / multiple calls
├── Failure → unknown/invalid/timeout/retry/idempotency
└── Security → allowlist/permission/confirmation/audit/sandbox
```

## 12.4 ReAct、Planning、Reflection

**优先级：P0/P1｜时间：60 分钟｜目标：准确映射、不夸大｜【必须理解】**

### ReAct

ReAct 将推理与行动交替：Reason/Action → Observation → 再 Reason。现代 API 未必暴露 Thought；不要要求模型输出隐含思维链。项目实现的是 Action/Observation 闭环，不记录显式 Thought。

### Planning

- Reactive：每步根据当前状态选下一动作；简单灵活，可能短视；
- Plan-and-Execute：先生成计划再执行/修订；适合复杂任务，但计划可能过时；
- Deterministic router：规则/分类器决定路径；稳定、可测，开放性较低。

项目使用 reactive planning：`model.complete()` 每轮动态选择，没有显式计划对象。

### Reflection

模型审查结果并修正，可改善部分错误，也增加 token/延迟且可能“越反思越偏”。需要触发条件、次数上限和外部验证，不能无限 self-critique。

### 高频问法

- ReAct 与普通 Tool Calling 区别？
- Planning 在你的代码哪里？
- CoT 与 Agent planning 一样吗？
- Reflection 是否一定有效？
- 怎样避免 plan 失效或无限重规划？

## 12.5 Memory / State / Context

**优先级：P0/P1｜时间：60 分钟｜目标：设计多轮和长期记忆｜【必须理解】**

### 一句话

State 是当前运行事实的总集合；Context 是本轮实际送给模型的信息；Memory 是跨步骤或跨会话保存、选择和更新信息的机制。

### Memory 类型

- Working/short-term：当前任务 messages、工具结果；
- Conversation memory：最近多轮对话；
- Semantic long-term：用户偏好、事实，按相关性检索；
- Episodic：历史任务及结果；
- Procedural：规则、技能和操作方法。

### 项目对应

`MemoryStore` 只保存 user/final assistant 到 SQLite，按 session 隔离、最近 N 条和字符预算取回；本次工具 Observation 只在局部 messages；Trace 单独存日志。它不是完整长期 Memory。

### Memory vs RAG

Memory 来源于交互和状态，强调写入/更新/遗忘/身份；RAG 来源于外部知识文档，强调检索证据。两者都可能用向量检索，可以组合，但语义和生命周期不同。

### 面试问法

- 多轮对话怎么实现？上下文超限怎么办？
- 为什么不能把全部历史直接拼接？
- 长期记忆怎样写入、冲突更新和删除？
- session 隔离怎么做？
- Memory 中的 Prompt Injection 怎么防？

### 回答版本

**20 秒：** Memory 不是无限聊天记录，而是决定保存什么、何时检索、怎样更新和遗忘的状态管理策略。

**1 分钟：** 短期使用窗口/摘要，长期事实结构化或向量检索；按用户/会话隔离，做 token 预算、权限、过期和删除；关键状态优先结构化，不完全依赖模型摘要。

### Memory 追问树

```text
Memory
├── 作用 → continuity / personalization / task state
├── 类型 → working / conversation / semantic / episodic
├── 写入 → what/when/validation
├── 读取 → window/summary/retrieval
├── 更新 → conflict/TTL/delete
├── 隔离 → session/user/tenant
└── 风险 → privacy/injection/stale memory/token cost
```

## 12.6 Workflow、State Machine 与 Human-in-the-loop

**优先级：P1｜时间：45 分钟｜目标：会设计可靠 Agent 外壳｜【建议理解】**

Workflow 用节点、边、条件和状态表达确定或半确定流程；状态机明确状态转移；Human-in-the-loop 在高风险/低置信操作前暂停，由人审查后继续。

适合人审：付款、删除、发送外部消息、权限变更、高影响结论。确认必须绑定具体操作与参数，防止确认后被替换（TOCTOU）。

项目当前没有 checkpoint/human approval；所有工具低风险且受本地范围限制。新增 delete/send/pay 工具必须补授权机制。

### Agent 追问树

```text
Agent
├── Agent vs Workflow/Chatbot
├── Loop → model/action/observation/stop
├── Tool Calling → schema/registry/error/security
├── Planning → reactive/plan-execute/router
├── Memory → state/context/long-term
├── Reliability → max steps/dedup/timeout/fallback
├── Evaluation → task/tool/trajectory/latency/cost
└── Production → trace/permission/human approval/concurrency
```

---

# 13. LangChain 与 LangGraph

## 13.1 LangChain

**优先级：P1｜时间：60 分钟｜目标：理解抽象，不背版本 API｜【建议理解】**

### 一句话和位置

LangChain 是 LLM 应用组件与集成框架，提供模型、Prompt、Retriever、Tool、Agent、中间件等统一抽象，适合快速连接生态组件。

为什么出现：不同模型/向量库/loader API 各异，手工胶水多；统一接口提高组合速度。局限是抽象层可能隐藏请求、增加调试复杂度，并随版本变化。

### 项目关系

Agent_WorkBench 没用 LangChain。我们手写了相当于 Model Adapter、Tool Registry、Agent Loop、Retriever 的最小实现，目的是掌握底层协议。面试时可以说未来需要大量第三方集成时考虑引入，而不是声称项目“用了 LangChain”。

### 面试问法

- LangChain 解决什么问题？
- Chain、Tool、Retriever、Agent 区别？
- 为什么项目没用？手写优缺点？
- 框架升级或抽象泄漏怎么办？

## 13.2 LangGraph

**优先级：P1｜时间：75 分钟｜目标：讲清 State/Node/Edge/Checkpoint 和选型｜【建议理解】**

### 一句话

LangGraph 用图和共享 State 表达有循环、分支、持久化和人工中断的 Agent/Workflow；Node 读取并更新状态，Edge 决定下一节点，Checkpoint 支持恢复。

### 为什么出现

简单 while-loop 在复杂分支、并行、重试、持久恢复、人工审批时难维护。显式图让状态转移可见并支持 durable execution。LangChain 官方学习材料也将深度定制 Agent 指向 LangGraph primitives：[LangChain/LangGraph 学习文档](https://docs.langchain.com/oss/python/learn)。

### 核心概念

```text
State：节点共享的类型化数据
Node：处理状态并返回更新
Edge：固定转移
Conditional Edge：根据状态路由
Checkpoint：按 thread 保存执行状态
Interrupt：暂停等待人或外部事件
Reducer：并行/多次更新同一字段时如何合并
```

### 项目怎样迁移

```text
START → load_memory → call_model
call_model ─无 tool calls→ save_answer → END
call_model ─有 calls→ execute_tools → call_model
```

当前 `messages/trace/step` 会进入 Graph State；`max_steps` 可通过 remaining steps；SQLite Memory 与 LangGraph checkpoint 需区分：checkpoint 是执行恢复，业务 Memory 是给模型的历史/知识。

### LangChain vs LangGraph

| 维度 | LangChain | LangGraph |
|---|---|---|
| 重点 | 组件、集成、快速构建 | 有状态编排、循环、恢复、人审 |
| 控制流 | 较高层 Agent/Chain | 显式 Node/Edge |
| 适合 | 简单应用、生态连接 | 复杂长流程、可靠执行 |
| 关系 | 可组合 | LangChain Agent 可建立在 LangGraph primitives 上 |

### 面试官可能怎么问

- 你为什么选/没选 LangGraph？
- State、Node、Edge、conditional edge 各是什么？
- checkpoint 和 Memory 区别？
- 怎样实现 Tool Loop、人审和恢复？
- LangGraph 相比手写 while loop 的价值和成本？

### 回答版本

**20 秒：** LangGraph 是有状态图编排框架，用 Node/Edge/State 表达 Agent 循环，并支持 checkpoint 和人工中断。

**1 分钟：** 项目目前逻辑简单，手写 loop 更透明；如果加入复杂分支、长任务恢复、并行工具或审批，再迁移 LangGraph。这样是按复杂度选型，不是框架越多越好。

### LangGraph 追问树

```text
LangGraph
├── 为什么图？→ complex branching/cycle/durable execution
├── State → schema/reducer/thread
├── Node → model/tool/router/human
├── Edge → normal/conditional
├── Persistence → checkpoint/resume
├── Human-in-loop → interrupt/approve/edit
└── 对比 → hand-written loop/LangChain workflow
```

## 13.3 MCP 与 Multi-Agent

**优先级：P2｜时间：45 分钟｜目标：知道边界，不作为主线｜【了解并能简答】**

MCP 是连接模型应用与外部 tools/resources/prompts 的标准化协议思路，降低每个客户端单独集成的成本；它不替代 Agent planning、权限治理或业务逻辑。

Multi-Agent 用多个角色/Agent 协作，适合明确分工、上下文隔离、并行或独立权限域；代价是协调、成本、延迟、错误传播和评测更复杂。能用单 Agent + Tools/Workflow 解决时不要先上 Multi-Agent。

---

# 14. FastAPI、后端、部署与推理基础

## 14.1 FastAPI / Pydantic / REST

**优先级：P1｜时间：60 分钟｜目标：结合接口代码回答｜【必须理解主干】**

FastAPI 用类型标注和 Pydantic 做请求/响应校验并生成 OpenAPI；路由装饰器将函数注册到 method/path。项目 `api.py::create_api()` 延迟构建 `AppComponents`，`ChatRequest/Response` 定义边界，异常映射 400/502。

```text
HTTP JSON → Pydantic Model → AgentResult → Response Model → JSON
```

面试问法：为什么选 FastAPI？Pydantic 做什么？依赖注入？同步/异步路由？怎样测试？怎样部署多 worker？

**30 秒：** FastAPI 适合 Python AI 服务，类型契约、自动校验/OpenAPI 和 async 生态好。项目用它封装聊天、文档和 Memory API，但核心 Agent 不依赖 FastAPI，所以 CLI/UI 可复用。

## 14.2 Cache、并发、队列、部署

**优先级：P2｜时间：60 分钟｜目标：系统设计可展开｜【建议理解】**

生产化常见组件：

- Redis：缓存、rate limit、短状态；不是所有 Memory 都应放 Redis；
- Queue：长文档入库、批量 embedding、长 Agent task 异步化；
- Docker：封装运行环境；K8s：编排、扩缩容、健康检查；
- Load balancer：分发请求；服务保持无状态或将状态外置；
- Observability：logs/metrics/traces，关联 request/session/trace ID；
- Circuit breaker/fallback：上游失败快速降级，避免雪崩。

项目当前单进程、SQLite、本地向量矩阵，不适合多实例共享写。扩展顺序：外置 PostgreSQL/向量库 → async LLM client/连接池 → 文档任务队列 → 缓存与限流 → metrics/tracing → 容器化与水平扩展。

## 14.3 LLM 推理与部署

**优先级：P2｜时间：60 分钟｜目标：会解释延迟和成本｜【了解原理】**

- TTFT：首 token 延迟，受排队、prefill、网络影响；
- TPOT：后续 token 间延迟，受 decode 吞吐影响；
- KV Cache：缓存历史 token 的 K/V，避免每次从头重算；占显存且随上下文/并发增长；
- Batching/continuous batching：合并请求提高吞吐，可能影响延迟；
- Quantization：低位权重/激活降低显存和提高吞吐，可能损质量；
- vLLM：面向高吞吐 LLM serving 的系统，了解 PagedAttention/continuous batching 的目标即可；
- Streaming：改善感知延迟，不一定降低总计算。

P3：Tensor Parallel、Pipeline Parallel、DeepSpeed/Megatron 细节，除非 JD 明确偏训练/Infra。

---

# 15. Agent Evaluation、安全与可观测性

## 15.1 Evaluation

**优先级：P1｜时间：75 分钟｜目标：能设计分层评测｜【必须理解】**

### 为什么出现

Agent 输出非确定且路径动态，“能 demo”不能说明可靠。只评最终答案也无法定位模型、检索还是工具问题。因此需要数据集、明确标准、分层指标和回归。

### 指标体系

```text
组件：检索 Hit/MRR、Tool 参数有效率、API error/latency
轨迹：期望工具、顺序、重复调用、步数、越权行为
结果：task success、correctness、faithfulness、citation
系统：P50/P95 latency、token/cost、availability
安全：prompt injection、权限、敏感信息、危险动作
```

项目 `evaluate_retrieval.py` 测 20 条 source 标签；`evaluate_agent.py` 检查工具集合、citation、步数和回答。真实模型曾 8/8，也曾 7/8，说明要报告重复分布而非最好一次。

### 面试问法

- Agent 怎样评估？LLM-as-judge 可靠吗？
- 离线评测和在线 A/B 区别？
- 如何构造 case？
- 非确定性怎样回归？

**1 分钟回答：** 先按失败层拆指标；建立真实业务和边界/对抗 case；固定模型参数和版本多次运行；确定性规则优先，LLM judge 做补充并校准人工一致性；上线再看任务成功、延迟、成本和用户反馈。

## 15.2 Security / Permission

**优先级：P1｜时间：45 分钟｜目标：能回答 Tool 风险｜【必须理解】**

威胁：Prompt injection、间接注入、数据泄漏、工具越权、路径穿越、SQL 注入、SSRF、任意代码执行、secret 日志泄漏、跨租户 Memory/RAG 泄漏。

防御不是一句 System Prompt：

1. 工具 allowlist 与最小权限；
2. 参数 Schema + 业务校验；
3. 用户/租户身份和资源级授权；
4. 高风险动作 human approval；
5. 文件/path/domain sandbox；
6. 输出/日志脱敏、secret manager；
7. 操作审计、限额、超时、幂等；
8. 对抗评测与 incident response。

项目已有 Registry allowlist、Schema、FileFinder 固定根、上传大小/后缀/文件名清洗、`.env` 忽略；缺少完整用户认证、租户授权、MIME 校验、日志脱敏和人审。

## 15.3 Trace / Logs / Metrics

**优先级：P1｜时间：30 分钟｜目标：Debug 有证据｜【必须理解】**

- Log：离散事件；
- Metric：可聚合数值时间序列；
- Trace：一次请求跨组件的因果链/span；
- Agent trajectory：模型步骤、工具与 Observation。

项目 JSONL 更接近应用级 trajectory log，不是完整分布式 trace。生产环境应有 request ID、模型/Prompt 版本、token、每步 latency、错误类型，同时脱敏。

---

# 16. Debug / 排错方法与高频题

## 16.1 通用分层法

```text
先复现并固定输入
→ 看入口/配置
→ 看 messages/tools payload
→ 看原始/解析后的 ModelTurn
→ 看 Tool Schema/arguments
→ 看 handler/数据库/外部 API
→ 看 Observation/call_id
→ 看下一轮和停止条件
→ 用测试/评测验证修复，防回归
```

不要一看到“回答错”就改 Prompt；先定位是哪一层证据错误。

## 16.2 高频 Debug 题

### Agent 一直重复调用工具

**考察：** 状态、停止、观测和可靠性。

**分析：** Trace 看是否同 name+arguments；工具结果是否清晰且 call_id 正确；Prompt 是否要求完成后总结；模型是否没看懂失败；是否缺状态标记。

**方案：** max_steps 硬上限；调用 signature 去重；相同失败不重试；返回明确结构；Prompt 约束；必要时状态机/规则路由。项目已有 max_steps 和 Prompt，尚无 signature 去重。

### Tool Calling 失败

区分未知工具、Schema 无效、handler 业务错误、网络超时、非幂等重试风险。可恢复错误作为 Observation；系统性错误告警/熔断；危险写操作需 idempotency key。

### RAG 检索不到正确文档

检查文档是否解析/入库、metadata/权限过滤、query 与语言、chunk 边界、embedding 模型、BM25/Dense 各自结果、Top-K、索引版本。再尝试 query rewrite、hybrid、rerank，不先盲目换大模型。

### 召回正确但回答错误

检查 context 是否真的进入 Prompt、排序/截断、冲突文档、instruction hierarchy、引用/拒答规则和模型能力。问题位于 generation，不要只调 Retriever。

### 上下文超限

为 system/tools/history/RAG/output 分预算；去除重复 schema；历史窗口/摘要/检索；Chunk/rerank；分阶段任务；不要无脑截掉最近用户问题。

### API 超时/429/5xx

设置分层 timeout；仅对可恢复且幂等操作指数退避+jitter；尊重 Retry-After；限流、队列、降级模型、缓存；Trace 区分排队/网络/model/tool latency。

### 响应太慢/成本过高

先度量每步。减少 Agent steps/重复调用和上下文；并行独立工具；缓存 embedding/检索/稳定回答；模型路由；streaming 改善感知；批处理入库；不要在未测量前优化。

### 多轮串话/数据泄漏

检查 session/user/tenant key、共享可变对象、缓存 key、数据库查询过滤和向量 metadata filter。项目按 session 隔离 Memory，但无租户认证。

---

# 17. 高频场景题：考点 → 分析 → 方案 → 取舍

## 17.1 什么时候用 Agent，什么时候 Workflow

**考察：** 是否理性选型。

先问路径能否预先枚举、错误代价、审计需求、任务开放性。确定审批/ETL 用 Workflow；开放研究/动态 API 组合用 Agent；高风险场景常用 Workflow 外壳 + Agent 节点 + 人审。

替代：规则 router、分类器、有限状态机。Agent 灵活但成本和不可预测性高。

## 17.2 设计可访问多个 API 的 Agent

**考察：** Tool 抽象、安全、可靠性。

统一 Tool schema/registry；认证凭据由服务端管理；每工具 timeout/retry/rate limit；读写权限分级；高风险确认；结果标准化；并行只用于独立调用；Trace 和预算；失败降级。不要把任意 URL 或 secret 交给模型。

## 17.3 如何设计 Agent Memory

**考察：** State 与长期记忆。

区分任务状态、最近对话、长期事实、历史事件；定义写入触发、读取检索、冲突更新、TTL/删除、用户可见性；结构化关键事实，向量检索长文本；隔离租户；评估是否真正提升任务成功。

## 17.4 如何评估 Agent 是否好用

**考察：** 从 Demo 到产品。

以业务 task success 为主；组件/轨迹/结果/系统/安全分层；真实 case + edge/adversarial；重复运行；线上反馈和人工抽检。单看 BLEU 或“感觉回答不错”不够。

## 17.5 如何设计公司内部知识问答 Agent

**考察：** 端到端系统设计。

```text
数据源/ACL → 解析/OCR/清洗 → Chunk/metadata/version
→ embedding + sparse/dense index
→ query auth/rewrite/filter → hybrid retrieve → rerank
→ evidence prompt → answer/citation/refusal
→ feedback/eval/trace/monitor
```

权限必须在检索前过滤，不是生成后删除。文档更新需要增量索引和版本；敏感问答要审计。若只做问答无需 Agent；需要查多个系统/执行操作时再加 Agent Tool。

## 17.6 如何降低幻觉

**考察：** 是否知道不存在单一开关。

明确任务和输出、RAG/Tools grounding、引用/拒答、结构化校验、冲突检测、模型选择、低随机性、事实 checker/人审、评测。区分“模型无知识”和“证据有但没遵循”。

## 17.7 如何提高速度和降低成本

**考察：** 度量与取舍。

先拆 TTFT、LLM steps、tool、retrieval。优先减少不必要步骤/上下文；小模型路由；缓存；并行独立 I/O；异步；批量 embedding；合适 Top-K/rerank 候选；超时/降级。缓存需考虑用户隔离和知识版本。

## 17.8 如何做 Tool 权限控制

**考察：** 安全不是 Prompt。

身份 → tool-level scope → resource-level authorization → 参数约束 → dry-run/approval → idempotency → audit。模型只能提出意图，服务端根据当前用户决定是否执行。

---

# 18. 系统设计答题模板

## 18.1 六步法

1. 澄清需求：用户、任务、规模、实时性、是否执行写操作；
2. 定义成功：正确性、延迟、成本、可用性、安全；
3. 画在线主链和离线数据链；
4. 逐模块选型并说明替代方案；
5. 讨论故障、权限、观测、扩展；
6. 给 MVP 与下一阶段，不一开始堆所有组件。

## 18.2 常见设计题清单

- 企业知识问答/RAG Agent；
- 客服 Agent：知识问答 + 工单/退款工具；
- 研究 Agent：搜索、抓取、引用、长任务 checkpoint；
- SQL Agent：Schema 获取、只读权限、查询校验、行数限制；
- 多 API 助理：工具路由、并行、授权、幂等；
- 文档处理平台：上传、异步解析、索引、状态通知；
- 高并发 LLM 网关：认证、限流、路由、缓存、重试、观测。

每题都要回答：为什么需要 Agent？不用 Agent 的更简单方案是什么？最大风险在哪里？怎样评测？

---

# 19. Agent_WorkBench 项目面试题（独立专项）

> 原则：只说真实实现。项目没有 LangChain/LangGraph、独立向量数据库、多 Agent、流式输出、用户认证或生产部署，不得编造。

## 19.1 3 个介绍版本

### 20 秒

我实现了一个个人信息工作台 Agent，用学校 OpenAI-compatible 模型动态调用知识检索、文件搜索和待办工具。核心是手写 Tool Calling 主循环，配有 SQLite Memory、BM25+BGE 混合 RAG、FastAPI/Streamlit、Trace、测试和评测。

### 1 分钟

项目解决个人知识、文件和待办分散的问题。入口最终调用 `Agent.run()`；模型收到 messages 和五个 Tool schemas，返回 ToolCall 后由 Registry 白名单和 JSON Schema 校验，再执行真实 handler，将 Observation 回传模型直到最终回答。RAG 支持文档解析、段落优先 Chunk、BM25、BGE 与 weighted RRF，并生成 citation。工程上有 Memory 隔离、超时重试、max_steps、JSONL Trace、17 项测试和两类评测。

### 3 分钟

按“问题 → 架构 → 一条真实请求 → 难点 → 证据 → 局限/优化”展开。必须提真实最新结果：17 tests；检索固定集六组 Hit@3=1.0；真实 Agent 因模型非确定出现过 8/8 和 7/8。不要只报最好结果。

## 19.2 项目整体题

### Q1. 项目解决什么问题？为什么做？

个人知识、文件和待办需要不同接口，普通聊天只能给文本；Agent 可根据目标动态组合检索和写操作。项目同时用于掌握不被框架隐藏的 Tool 协议与 Agent Loop。

### Q2. 程序从哪里启动？

CLI `main.py`、API `api_main.py → api.py`、UI `ui.py`；都经 `app.py::build_components()` 取得同一个核心对象，最终调用 `Agent.run()`。

### Q3. 你的主要工作是什么？

应回答实际仓库全链：架构与主循环、模型适配、Tool/Schema、RAG/Memory/API/UI、测试评测和 Debug。若被问团队分工，明确这是个人项目，不虚构协作。

### Q4. 最大技术难点？

建议选两个讲深：一是正确维护 assistant tool request 与 call_id 对应的 Observation，使多轮协议闭环；二是用实际评测选择 Hybrid 权重而非主观认定 BGE 必然更好。

### Q5. 项目为什么不是固定 Workflow？

用户任务可能只查知识、只列待办或连续调用多工具，路径取决于输入和中间结果；但外层最大步数、校验和权限仍是确定流程。

## 19.3 技术选型题

### Q6. 为什么不用 LangChain/LangGraph？

当前控制流简单，手写 loop 更透明，便于解释 Schema/call_id/Observation 和测试。复杂分支、checkpoint、人审、并行工具增加后再考虑 LangGraph。这不是否定框架，而是按复杂度选型。

### Q7. “为什么用 LangGraph？”该怎么答？

应纠正前提：“这个项目没有使用 LangGraph。”随后说明若迁移会把 messages/trace/step 作为 State，把 call_model/execute_tools 作为节点，用 conditional edge 循环，用 checkpoint 支持恢复。

### Q8. 为什么不用 OpenAI SDK？

学校服务是 OpenAI-compatible 自定义 endpoint，标准库 urllib 足以展示完整 HTTP 协议并减少依赖。生产中可换支持连接池、async、streaming 的成熟客户端；ModelClient 契约让主循环不变。

### Q9. 为什么使用 BGE-small-zh？

中文场景、CPU ONNX 可运行、依赖比 PyTorch 方案轻。不是凭 benchmark 定论，仍用业务固定集比较 BM25/Vector/Hybrid。

### Q10. 为什么用 SQLite？

单机 MVP 零服务依赖、事务和持久化足够。高并发/多实例应迁移 PostgreSQL；向量规模扩大再引入 pgvector/Milvus。

### Q11. 为什么选择 FastAPI？

Python AI 生态、类型/Pydantic 校验、自动 OpenAPI、测试方便；核心业务与框架解耦。项目不依赖它才能运行 Agent。

## 19.4 Agent / Tool 实现题

### Q12. Agent Loop 在哪里？

`agent.py::Agent.run()`：构造 messages → `model.complete()` → 无 ToolCall 返回；有则 `registry.execute()` → append role=tool → 再循环。

### Q13. Planning 在哪里？

没有独立 Planner。模型在每次 `complete()` 根据 messages/tools 选择下一动作，是 reactive planning。

### Q14. Tool 怎样注册？

`tools.py::create_registry()` 构造 `Tool(name, description, parameters, handler)` 并 `registry.register()`；内部 dict 用 name 分发。

### Q15. 参数怎样保证合法？

Schema 先指导模型生成，应用侧 `Draft202012Validator` 再校验；handler 自身继续做业务校验，如 query 非空、top_k 限制。

### Q16. 工具失败怎么办？

未知工具、Schema 错、handler 异常统一为 `{ok:false,error}` Observation，模型可修正或说明。LLM 传输/协议错误则抛分类异常，由 API 映射 502。

### Q17. 怎样避免无限循环？

Prompt 减少重复 + `max_steps=6` 硬停止。当前未实现相同调用 signature 去重，这是明确优化项。

### Q18. call_id 有什么用？

将每个 role=tool 结果对应到模型发出的具体 ToolCall；一轮多个工具时尤其必要。

## 19.5 RAG / Memory 实现题

### Q19. RAG 完整调用链？

`DocumentLoader → TextChunker → SQLiteChunkStore → _reload(BM25+BGE) → HybridKnowledgeBase.search → Tool handler → Observation → final answer`。

### Q20. Chunk 参数为什么 500/80？

段落优先、字符兜底的小库起点；500 平衡语义完整和检索粒度，80 缓解边界。不是普适最优，应通过 query/source 评测调整。

### Q21. 为什么 Hybrid 权重 1.4/1.0？

初版等权 BGE Hybrid 在固定集漏掉一个问题；数据偏术语型，BM25 强。提高 BM25 权重后 Hit@3 恢复 1.0；承认样本仅 20 条，需扩大集验证过拟合。

### Q22. 项目用了什么向量数据库？

没有独立 Vector DB。Chunk 在 SQLite，向量矩阵在内存精确计算。小规模可复现；大规模需 ANN/外置服务。

### Q23. Citation 怎样实现？

检索层用 source 和 position 生成 `[source#chunk-N]`；Prompt 要求模型保留。当前无最终 citation validator，可增加证据覆盖校验。

### Q24. Memory 怎样实现？

`MemoryStore` 用 SQLite 按 session 保存 user 和最终 assistant；取最近 window_size 条再按字符预算保留最新消息。工具中间消息不跨 run 持久化。

### Q25. Memory 与 Trace 区别？

Memory 给下一轮模型提供对话；Trace 给开发者记录执行轨迹。Trace 含工具参数/耗时/结果，不应直接全部塞入上下文。

## 19.6 Debug / 质量题

### Q26. 遇到过什么真实 Bug？

SQLite 上下文管理器提交事务但句柄未及时关闭，Windows 清理评测临时 DB 报 WinError 32。为三类 Store 统一 `_connect()`，finally close；测试和六组检索评测回归通过。

### Q27. 怎样测试模型不确定系统？

用 `ScriptedModel/FakeClient` 固定外部决策，真实运行 Agent 控制流；组件测试验证 Store/RAG/API；真实在线 case 评行为分布。

### Q28. 为什么 Agent 评测不是稳定满分？

模型可能重复搜索，严格规则将超过工具次数视为失败。诚实报告 7/8 与曾有 8/8，并计划 signature 去重、固定参数和多次统计。

## 19.7 优化 / 扩展题

### Q29. 用户增加 100 倍怎么办？

外置 PostgreSQL/向量库和对象存储；服务无状态化；异步 LLM client、连接池、限流/队列；文档异步入库；缓存按 tenant/version 隔离；多实例与集中 trace/metrics；压测后扩容。

### Q30. 下一步最值得优化什么？

优先：重复调用去重、精确 token budget、citation validator、异步/streaming、权限认证、增量向量索引、更大评测集。不要先堆 Multi-Agent。

---

# 20. 最易混淆概念对照表

| 对比 | 本质区别 | 能否同时用 | 面试官在考什么 |
|---|---|---|---|
| Agent vs Workflow | 动态选路径 vs 预定义路径 | 可以嵌套 | 是否理性选型 |
| Agent vs Chatbot | 行动闭环 vs 主要生成文本 | 可以 | 是否理解工具与状态 |
| RAG vs Fine-tuning | 推理时注入知识 vs 改参数/行为 | 可以 | 知识更新与成本 |
| Embedding vs Token | 连续向量 vs 离散 ID | 必然关联但不同 | 基础概念边界 |
| Embedding vs Hidden State | 检索段落向量 vs 模型层内上下文化表示 | 可从 hidden pooling 产生 | 表示学习理解 |
| Vector DB vs SQL DB | 近邻相似度 vs 精确关系查询 | pgvector 可结合 | 数据和查询模式 |
| Function vs Tool Calling | 函数协议偏窄，Tool 概念更广 | 常混用 | 协议和执行边界 |
| Prompt vs System Prompt | 所有输入指令/上下文 vs 高优先级全局规则 | System 是 Prompt 一部分 | 角色和信任层级 |
| Memory vs RAG | 交互状态/历史 vs 外部知识证据 | 可以 | 生命周期与写入策略 |
| LangChain vs LangGraph | 组件集成 vs 有状态图编排 | 可以 | 框架选型 |
| Encoder vs Decoder | 双向理解表示 vs 因果生成 | Encoder-Decoder 组合 | 模型结构 |
| Self vs Cross Attention | QKV 同源 vs Q 与 KV 异源 | 可以 | Attention 来源 |
| 训练 vs 推理 | 更新参数 vs 固定参数生成 | 先训练后推理 | 性能与数据流 |
| Pretrain vs Fine-tune | 通用自监督 vs 下游适配 | 顺序组合 | 数据与目标 |
| SFT vs RLHF/DPO | 监督模仿 vs 偏好对齐 | 通常组合 | 对齐流程 |
| LoRA vs Full FT | 低秩增量 vs 更新全部参数 | 二选一/阶段组合 | 资源与能力取舍 |
| ReAct vs Tool Calling | 循环范式 vs 一次结构化动作机制 | ReAct 常使用 Tool Calling | 层级关系 |
| State vs Context vs Memory | 所有运行事实 vs 本轮模型输入 vs 跨时保存/检索 | 相互关联 | Agent 状态管理 |
| Logs vs Metrics vs Traces | 事件 vs 聚合数值 vs 因果链 | 应同时用 | 可观测性 |

---

# 21. P2 / P3 了解清单：学不深但不能没听过

## P2（每项 15～30 分钟）

- Query Rewrite / Multi-query / HyDE：改善 query 表达，代价是额外模型调用和可能漂移；
- Reranker：Cross-Encoder 精排候选，质量换延迟；
- Parent-child / Multi-vector retrieval：小块检索、大块返回；
- GraphRAG：利用实体关系和图结构，适合关系密集问题，构建成本高；
- MCP：标准化暴露 tool/resource/prompt，不负责自动规划；
- Multi-Agent：角色分工与上下文隔离，协调成本高；
- Redis/Queue/Docker/K8s：生产工程能力；
- vLLM/KV Cache/Quantization：推理吞吐、显存和质量取舍；
- LoRA/DPO：了解目的和适用场景。

## P3（JD 明确要求再学）

- PPO/DQN 公式与强化学习推导；
- Megatron/DeepSpeed/FSDP 分布式训练细节；
- CUDA kernel、Tensor/Pipeline Parallel 深水区；
- OS 内核调度、虚拟内存页表细节；
- TCP 拥塞控制算法细节；
- 红黑树证明、复杂动态规划和竞赛难题；
- 多模态/VLM 训练细节。

---

# 22. 必会 50 题索引

> 用法：先遮住“回答锚点”，每题 30～60 秒口述。答不上再回对应章节，不背整段。

| # | 高频问题 | 回答必须出现的锚点 | 频率 |
|---:|---|---|:---:|
| 1 | Transformer 为什么适合大模型？ | Attention、并行、扩展；推理仍自回归 | ★★★★★ |
| 2 | Attention 怎样计算？ | QKᵀ/√dk → softmax → V | ★★★★★ |
| 3 | Q/K/V 是什么？ | 查询、匹配键、被聚合值；均为投影 | ★★★★★ |
| 4 | 为什么除以 √dk？ | 点积方差、softmax 饱和、梯度稳定 | ★★★★★ |
| 5 | Multi-Head 作用？ | 多子空间关系、拼接投影 | ★★★★ |
| 6 | 为什么需要位置编码？ | Attention 本身排列不敏感 | ★★★★ |
| 7 | Encoder 和 Decoder 区别？ | 双向理解 vs causal 生成 | ★★★★★ |
| 8 | GPT 为什么 Decoder-only？ | next-token 目标、生成统一、扩展 | ★★★★ |
| 9 | Token 是什么？ | tokenizer 离散单位，不等于字/词 | ★★★★★ |
| 10 | Context window 包含什么？ | system/history/tools/RAG/user/output | ★★★★★ |
| 11 | Temperature/top-k/top-p？ | 概率分布与采样集合 | ★★★★ |
| 12 | Pretrain/SFT/RLHF(DPO)？ | 通用能力/指令遵循/偏好对齐 | ★★★★ |
| 13 | LoRA 为什么省资源？ | 冻结基座、低秩增量 | ★★★ |
| 14 | 什么是幻觉，如何降低？ | 概率生成；grounding/validation/refusal/eval | ★★★★★ |
| 15 | Prompt 和 System Prompt？ | 总上下文 vs 高优先级规则；非安全边界 | ★★★★★ |
| 16 | Structured Output 有何价值？ | 机器可解析、Schema、仍需校验 | ★★★★★ |
| 17 | Function Calling 流程？ | schema → call → validate/execute → observation | ★★★★★ |
| 18 | 什么是 Embedding？ | 固定维语义向量、相似度 | ★★★★★ |
| 19 | Embedding 怎么选？ | 语言/领域/速度/维度/许可/业务评测 | ★★★★ |
| 20 | cosine、dot、L2 区别？ | 方向、模长、距离；归一化关系 | ★★★★ |
| 21 | 什么是向量数据库？ | vector+metadata+ANN+更新/过滤 | ★★★★★ |
| 22 | Vector DB vs SQL？ | 相似近邻 vs 精确关系/事务，可组合 | ★★★★★ |
| 23 | 什么是 RAG？ | retrieve evidence → generate/cite | ★★★★★ |
| 24 | RAG 完整流程？ | ingestion + online retrieval/generation/eval | ★★★★★ |
| 25 | RAG vs Fine-tuning？ | 知识注入 vs 参数行为，更新/引用/成本 | ★★★★★ |
| 26 | Chunk size/overlap 怎么定？ | 完整性/粒度/重复/token，用评测定 | ★★★★★ |
| 27 | Top-K 越大越好吗？ | recall vs noise/cost/lost-in-middle | ★★★★★ |
| 28 | BM25 vs Dense？ | 精确词项 vs 语义改写 | ★★★★★ |
| 29 | 为什么 Hybrid/RRF？ | 互补；排名融合解决分数量纲 | ★★★★ |
| 30 | Reranker 做什么？ | 小候选 joint scoring，质量换延迟 | ★★★★ |
| 31 | RAG 如何评估？ | retrieval/answer/system 分层 | ★★★★★ |
| 32 | 什么是 Agent？ | model decision + tool + observation loop | ★★★★★ |
| 33 | Agent vs Workflow？ | 动态路径 vs 预定义路径，组合 | ★★★★★ |
| 34 | ReAct 是什么？ | reason/action/observation 循环 | ★★★★★ |
| 35 | Planning 有哪些方式？ | reactive/plan-execute/router | ★★★★ |
| 36 | Memory 是什么？ | 保存/检索/更新/遗忘策略，不是全历史 | ★★★★★ |
| 37 | Memory vs RAG？ | 交互状态 vs 外部知识 | ★★★★★ |
| 38 | 怎样避免 Agent 无限循环？ | max steps/dedup/state/prompt/eval | ★★★★★ |
| 39 | Tool 权限如何做？ | allowlist/authz/validation/approval/audit | ★★★★★ |
| 40 | Agent 怎样评测？ | component/trajectory/outcome/system/safety | ★★★★★ |
| 41 | LangChain 做什么？ | 组件与集成；抽象代价 | ★★★★ |
| 42 | LangGraph 做什么？ | State/Node/Edge/checkpoint/interrupt | ★★★★★ |
| 43 | LangChain vs LangGraph？ | 组件集成 vs 状态图编排 | ★★★★ |
| 44 | async 与线程/进程？ | 协作 I/O / shared-memory / CPU parallel | ★★★★ |
| 45 | FastAPI 为什么适合 AI 服务？ | type/Pydantic/OpenAPI/async/Python ecosystem | ★★★★ |
| 46 | HTTP 429/5xx 怎么处理？ | timeout/limited retry/backoff/jitter/idempotency | ★★★★ |
| 47 | 依赖注入为何有用？ | 解耦、替换、测试 | ★★★★ |
| 48 | Python 装饰器是什么？ | `f=decorator(f)`，注册/包装 | ★★★★ |
| 49 | Git secret 提交后怎么办？ | 立即轮换，清历史仅是后续治理 | ★★★★ |
| 50 | 介绍 Agent_WorkBench | 问题/架构/请求/难点/指标/局限 | ★★★★★ |

---

# 23. 面试前 1 天速查

## 23.1 P0 核心链

```text
Transformer：QKV → scaled attention → multi-head → mask/position → decoder generation
RAG：load → chunk → embed/index → retrieve → rerank → context → answer/citation → eval
Agent：messages/state → model decision → ToolCall → validate/execute → Observation → loop/stop
工程：HTTP/API → timeout/retry → trace/eval → auth/permission → cost/latency
项目：entry → build_components → Agent.run → model/registry/memory/RAG → result
```

## 23.2 极高频 ★★★★★

- Transformer/Attention/QKV/√dk；
- Token/context/幻觉；
- Embedding、Vector DB；
- RAG 完整流程、Chunk、Top-K、Hybrid、评测；
- Agent Loop、Agent vs Workflow、Tool Calling、Memory；
- 项目 1 分钟介绍、真实调用链、难点、Bug、优化；
- Python 对象/装饰器/异常/依赖注入；
- HTTP 状态码、重试、API Key；
- 无限循环、检索失败、上下文超限、权限控制。

## 23.3 高频 ★★★★

- LangChain/LangGraph；
- FastAPI、async；
- SFT/LoRA/RLHF/DPO；
- Reranker、query rewrite；
- Git/Linux/SQL/索引/事务；
- Evaluation、Trace、安全。

## 23.4 项目必会 30 题

复习第 19 章。至少闭卷回答：Q2 主链、Q6 框架选型、Q12 Loop、Q13 Planning、Q14 Tool、Q17 停止、Q19 RAG、Q21 权重、Q22 Vector DB、Q24 Memory、Q26 Bug、Q30 优化。

## 23.5 最后检查的易错话术

- 不说“RAG 消除幻觉”，说“提供 grounding，仍需生成层约束与评测”；
- 不说“项目用了 LangGraph/向量数据库”，项目没有；
- 不说“temperature=0 完全确定”；
- 不说“Prompt 能保证安全”；
- 不说“Embedding 就是 token”；
- 不说“Top-K 越大越好”；
- 不说“测试全过所以真实模型一定可靠”；
- 不把字符预算说成精确 token 预算；
- 不把 8/8 当稳定结果，说明非确定回归；
- 不编造并发、部署、多租户和人审能力。

## 23.6 面试当场答题模板

```text
定义题：一句话边界 → 目标 → 三步流程
原理题：输入 → 关键变换 → 输出 → 为什么有效
对比题：目标 → 数据/控制流 → 成本 → 场景 → 能否组合
项目题：文件/函数 → 数据流 → 参数理由 → 结果 → 局限
Debug：复现 → Trace/指标 → 分层定位 → 修复 → 回归
设计题：需求/指标 → 数据流 → 模块 → 安全/故障 → 评测/扩展
```

---

# 附录 A：15 天完整版冲刺计划

> 每天 1～3 小时。若只有 1 小时，完成 P0 和口述；2 小时再做项目映射；3 小时增加代码阅读/模拟。每天至少 20 分钟复习旧题、20 分钟闭卷回答。

| Day | 新知识（约 55%） | 项目/代码（约 20%） | 回答与复习（约 25%） | 当天验收 |
|---:|---|---|---|---|
| 1 | P0 Agent、Loop、Agent vs Workflow、ReAct | `Agent.run()` 全链 | 回答 32–40 题中前 5 题 | 画 Agent Loop，1 分钟讲清 |
| 2 | P0 Tool Calling、Schema、错误、安全 | `Tool/Registry/create_registry` | 模拟 Tool 连续追问 | 从 schema 讲到 Observation |
| 3 | P0 RAG 总流程、Chunk、Top-K | Loader/Chunker/ingest | 复习 Day1–2；RAG 20 秒/1 分钟 | 画离线+在线两条链 |
| 4 | P0 Embedding、Vector DB、BM25/Dense/Hybrid | 三个 Retriever + RRF | 回答 18–31 中核心题 | 解释为何不是向量越强越好 |
| 5 | P0 Transformer 总体、QKV、Attention | 联系 token/context，不要求训练代码 | 闭卷画 Transformer；第一轮追问 | 解释公式和 √dk |
| 6 | P0 LLM、Token、Context、Sampling、幻觉 | Memory 字符预算局限 | 复习 Transformer/RAG | 接住两层 LLM 追问 |
| 7 | P0 Python 对象/OOP/Protocol/装饰器/contextmanager | `contracts.py` 和三个 `_connect()` | 15 道 Python 口述 | 用真实 Bug 解释上下文管理 |
| 8 | P0 HTTP/API/Prompt/Structured Output | `llm_client.py`、`api.py` | **第一次技术模拟** 30–40 分钟 | 找出 5 个回答漏洞 |
| 9 | P1 Memory/State/Context、Planning/Workflow | `MemoryStore` 和 messages | 修复第一次模拟错题 | 区分四种状态 |
| 10 | P1 LangChain/LangGraph | 将当前 loop 画成 Graph | 框架选型追问 | 不编造项目使用框架 |
| 11 | P1 FastAPI/async/DB/Git/Linux | API route/SQLite/Git 安全 | **项目专项模拟** | 项目 30 题至少答 20 |
| 12 | P1 Evaluation/Trace/Security | tests/evaluate/Trace | Debug 题 6 道 | 分层定位，不先改 Prompt |
| 13 | 系统设计、场景题、生产化 P2 | 企业知识 Agent 架构 | **Agent+RAG 深挖模拟** | 15 分钟系统设计完整 |
| 14 | ML/DL/NLP、SFT/LoRA/RLHF、推理基础 | 说明项目不训练模型 | **完整模拟面试** 45 分钟 | 技术+项目+场景连贯 |
| 15 | 不学大块新内容 | 检查仓库/README/演示 | 错题复盘 + 50 题 + 1 天速查 | 连续 60 分钟无资料模拟 |

每天操作循环：

```text
20 min 昨日闭卷复述
→ 40–90 min 新知识
→ 20–40 min 对应项目代码
→ 20–30 min 面试问答/追问
→ 5 min 记录“答不上来的具体点”
```

---

# 附录 B：10 天压缩版

| Day | 必学内容 | 项目结合 | 模拟/验收 |
|---:|---|---|---|
| 1 | Agent + Tool Calling + ReAct | `Agent.run/ToolRegistry` | 画完整 Loop |
| 2 | RAG + Chunk + Top-K | 入库/检索链 | 10 道 RAG 问题 |
| 3 | Embedding + Vector DB + Hybrid/Rerank | BGE/BM25/RRF | Debug 两个检索 case |
| 4 | Transformer + Attention/QKV/Mask | token/context 联系 | 画结构并口述 |
| 5 | LLM/Prompt/结构化输出/API | `llm_client.py` | 30 分钟技术模拟 |
| 6 | Python 高频 + HTTP + DB + async | contextmanager/API/SQLite | 15 道基础题 |
| 7 | Memory/Planning/Workflow/LangGraph | 当前 loop 迁移图 | 框架选型追问 |
| 8 | Evaluation/Security/Debug/场景 | tests/evals/真实 Bug | 项目专项模拟 |
| 9 | ML/DL 轻量补齐 + 系统设计 | 项目扩展 100 倍 | Agent+RAG 深挖模拟 |
| 10 | 50 题、项目 30 题、错题 | 演示与真实指标 | 45–60 分钟完整模拟 |

压缩原则：不单独学习 P2；训练/部署只保留一句话和场景；算法每天 20 分钟。

---

# 附录 C：7 天极限版

| Day | 2～3 小时任务 | 必须产出 |
|---:|---|---|
| 1 | Agent Loop + Tool Calling + 项目主链 | 1 分钟项目介绍；手画 messages 变化 |
| 2 | RAG + Chunk + Embedding + Vector DB + Hybrid | RAG 1 分钟回答；5 个 Debug 分支 |
| 3 | Transformer + Attention + Token/Context/幻觉 | 解释 QKV/√dk/Decoder |
| 4 | Python 高频 + HTTP/API + Prompt/Schema | 回答装饰器、Protocol、async、状态码、重试 |
| 5 | Memory/Planning/Workflow/LangGraph + Evaluation | 说明项目没用 LangGraph；画迁移图 |
| 6 | 项目 30 题 + 场景/系统设计 | 40 分钟项目深挖模拟 |
| 7 | 50 题速查 + 错题 + 完整模拟 | 两次 30 分钟无资料回答 |

7 天必须主动放弃：分布式训练、RL 算法公式、K8s 细节、GraphRAG 深入、多 Agent 框架横向评测、复杂算法题。每天只做 1～2 道最常见算法保持手感。

---

# 附录 D：时间不够时砍什么

## 必须保留

1. Agent / Tool Calling / Agent vs Workflow / 无限循环；
2. RAG / Chunk / Embedding / Vector DB / Hybrid / Debug；
3. Transformer / Attention / Token / Context / 幻觉；
4. Python 项目相关基础、HTTP/API、Prompt/Schema；
5. Agent_WorkBench 介绍、主链、难点、Bug、指标、局限；
6. 至少一次完整模拟。

## 时间不足先压缩

- ML/DL 只保留训练、loss、过拟合、反向传播直觉；
- LangChain/LangGraph 只保留核心抽象和选型；
- 数据结构只保留复杂度、Hash、栈队列、Top-K；
- 数据库只保留索引、事务、SQL 注入、SQLite 局限；
- 部署只保留缓存/队列/容器/扩缩容的作用。

## 最后放弃

P3 全部；P2 中 Multi-Agent、GraphRAG、K8s、推理框架细节；冷门模型参数和论文年份；低收益命令背诵。

原则：宁可把 Agent/RAG/项目讲透，也不要每项只会一句定义。

---

# 附录 E：学习完成度检查标准

## 单知识点

```text
[ ] 能用 20 秒说定义和目标
[ ] 能举一个直观例子
[ ] 能解释为什么出现
[ ] 能画核心流程
[ ] 能与最相似技术对比
[ ] 能联系项目文件/函数或说明项目没用
[ ] 能回答一个 Debug/场景问题
[ ] 能接 1～2 层追问
```

达到前 4 项：已理解；达到前 6 项：可以独立回答；全部达到：可以应对追问。

## 项目

```text
[ ] 20 秒、1 分钟、3 分钟介绍都能控制时间
[ ] 能画入口 → 组装 → Agent → Model/Tool → Result
[ ] 能解释 Agent.run() 每个阶段的数据类型
[ ] 能解释 RAG 入库/检索链和参数取舍
[ ] 能展示一个真实 Bug 的症状、根因、修复、回归
[ ] 能准确说出没实现的功能
[ ] 能回答“100 倍用户”和“下一步优化”
```

## 模拟面试评分（每项 0～2）

| 维度 | 0 | 1 | 2 |
|---|---|---|---|
| 准确性 | 明显错误 | 主体对，有模糊 | 边界准确 |
| 结构 | 零散 | 有顺序 | 先结论后展开 |
| 原理 | 只背定义 | 能说流程 | 能解释原因与取舍 |
| 项目 | 无法定位 | 能说文件 | 能讲数据和证据 |
| 追问 | 一问就断 | 接一层 | 接两层并承认边界 |
| 工程判断 | 只堆技术 | 有方案 | 能比较成本/风险 |

总分 9/12 可进入面试；低于 9 优先复盘 P0 和项目，不扩展 P2/P3。

---

# 附录 F：长期增补模板

以后遇到新 JD、新问题或一次真实面试，按下面模板追加，而不是只抄答案：

```text
知识点 / 问题：
来源岗位 / 面试日期：
优先级与预计时间：
面试官原始问法：
问题类型（A-I）：
一句话理解：
为什么出现：
核心流程：
容易混淆概念：
20 秒回答：
1 分钟回答：
继续追问：
Agent_WorkBench 对应代码或“项目未使用”：
当时答错/卡住的原因：
下次回答：
学习状态：
```

最后提醒：面试八股的价值不是让回答听起来像教材，而是让你在陌生问法下迅速定位概念、给出边界、解释取舍，并用真实项目代码和验证证据落地。
