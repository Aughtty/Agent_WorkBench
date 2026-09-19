"""用于项目演示的轻量 Streamlit UI；业务逻辑仍在后端模块中。"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(SOURCE_ROOT))

import streamlit as st

from workbench_agent.app import build_components


st.set_page_config(page_title="个人信息工作台 Agent", page_icon="🧰", layout="wide")
st.title("个人信息工作台 Agent")
st.caption("真实 LLM Tool Calling · 混合检索 · SQLite Memory · Trace")


@st.cache_resource
def get_components():
    return build_components(Path("data"), online=True)


service = get_components()

with st.sidebar:
    st.subheader("知识库")
    upload = st.file_uploader("上传 TXT / Markdown / PDF / DOCX", type=["txt", "md", "pdf", "docx"])
    if upload and st.button("加入知识库", type="primary"):
        with tempfile.TemporaryDirectory(prefix="workbench-ui-") as directory:
            path = Path(directory) / upload.name
            path.write_bytes(upload.getvalue())
            result = service.knowledge.ingest_file(path, source=upload.name)
        st.success(f"已导入 {result['chunks']} 个 Chunk")
        st.cache_resource.clear()
    stats = service.knowledge.stats()
    st.metric("Chunk 数", stats["chunks"])
    st.write("来源：", stats["sources"])

session_id = st.text_input("Session ID", value="streamlit-demo")
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("例如：查知识库里的 Tool Calling，并记录一个复习待办"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Agent 正在决策和调用工具……"):
            result = service.agent.run(prompt, session_id=session_id)
        st.markdown(result.answer)
        with st.expander("查看 Agent Trace"):
            st.json(result.trace)
    st.session_state.messages.append({"role": "assistant", "content": result.answer})

