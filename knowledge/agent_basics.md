# Agent 与 Tool Calling

Agent 是能够围绕用户目标选择行动、观察结果并继续决策的 LLM 应用。普通 ChatBot 通常只生成文本；固定 Workflow 的步骤主要由开发者预先定义；Agent 则让模型在受控工具集合内动态选择下一步。

Tool Calling 并不是模型直接执行 Python 函数。模型读取工具名称、描述和 JSON Schema，生成结构化的工具名与参数；应用程序校验参数、执行真实函数，再把 Tool Result 以 role=tool 的消息回传给模型。

一次工具调用通常至少需要两次模型请求：第一次决定调用什么工具，应用执行后，第二次模型读取 Observation 并回答或继续调用其他工具。call_id 用来关联工具请求和返回结果。

Agent 必须设置停止条件，例如最大步骤数。否则模型可能重复调用同一工具，造成死循环、延时和 Token 成本失控。

