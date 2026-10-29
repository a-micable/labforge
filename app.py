"""RepairLoop UI — local sandbox + Nemotron on Nebius Token Factory."""

from __future__ import annotations

import json
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from agent import llm, run_agent_loop

load_dotenv()

ROOT = Path(__file__).resolve().parent
TASKS = sorted((ROOT / "tasks").glob("*.json"))


def load_task(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


st.set_page_config(page_title="RepairLoop", layout="wide")

# keep the chrome quiet — this is a lab tool, not a landing page
st.markdown(
    """
    <style>
      .block-container { padding-top: 1.2rem; max-width: 1100px; }
      h1 { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 1.6rem; }
      .stCaption { opacity: 0.75; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("RepairLoop")
st.caption("write → run → test → repair · NVIDIA Nemotron · Nebius Token Factory")

stack = llm.describe_stack()
tasks = [load_task(p) for p in TASKS]
by_id = {t["id"]: t for t in tasks}

with st.sidebar:
    st.markdown("**inference**")
    st.code(
        f"{stack['base_url']}\n{stack['model']}",
        language="text",
    )
    if stack["api_key_configured"]:
        st.write("key: present")
    else:
        st.write("key: missing — copy `.env.example` → `.env`")

    max_iters = st.slider("max iterations", 1, 6, 4)
    st.markdown("---")
    st.markdown("track: Coding & Agentic Engineering")

picked = st.selectbox(
    "task",
    options=list(by_id.keys()),
    format_func=lambda i: f"{by_id[i]['title']}  [{by_id[i]['difficulty']}]",
)
task = by_id[picked]

left, right = st.columns([1.2, 1])
with left:
    st.markdown("#### prompt")
    st.text(task["prompt"])
with right:
    st.markdown("#### what the grader checks")
    st.text(task["public_tests_hint"])

go = st.button("run agent", type="primary")

trace = st.container()
out_code = st.empty()
banner = st.empty()

if go:
    if not os.environ.get("NEBIUS_API_KEY", "").strip():
        banner.error("NEBIUS_API_KEY not set")
        st.stop()

    chunks: list[str] = []

    def on_progress(evt: dict) -> None:
        kind = evt.get("event")
        if kind == "thinking":
            chunks.append(f"iter {evt['iteration']}: calling model…")
        elif kind == "code":
            chunks.append(f"iter {evt['iteration']}: got {len(evt.get('code') or '')} bytes")
            out_code.code(evt.get("code") or "", language="python")
        elif kind == "test":
            tag = "ok" if evt.get("ok") else "fail"
            chunks.append(
                f"iter {evt['iteration']}: tests {tag} (exit {evt.get('exit_code')})\n"
                f"stdout:\n{evt.get('stdout') or ''}\n"
                f"stderr:\n{evt.get('stderr') or ''}"
            )
        with trace:
            st.text("\n\n".join(chunks))

    with st.spinner("token factory…"):
        result = run_agent_loop(
            task_prompt=task["prompt"],
            public_tests_hint=task["public_tests_hint"],
            test_source=task["test_source"],
            max_iters=max_iters,
            on_progress=on_progress,
        )

    if result.error:
        banner.error(result.error)
    elif result.success:
        banner.success(f"passed on {result.model} after {len(result.steps)} iter(s)")
    else:
        banner.warning(f"still failing after {len(result.steps)} iter(s)")

    st.markdown("#### final solution.py")
    st.code(result.final_code or "# empty", language="python")
