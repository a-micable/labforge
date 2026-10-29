"""RepairLoop — Streamlit front-end for the Nebius/NVIDIA hackathon demo."""

from __future__ import annotations

from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from repairloop import __version__
from repairloop.config import load_settings
from repairloop.session import run_session
from repairloop.tasks import list_tasks

st.set_page_config(page_title="RepairLoop", layout="wide")

st.markdown(
    """
    <style>
      .block-container { max-width: 1120px; padding-top: 1rem; }
      h1 { font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
           letter-spacing: -0.02em; font-size: 1.55rem; margin-bottom: 0.2rem; }
      div[data-testid="stCaption"] { opacity: 0.7; }
    </style>
    """,
    unsafe_allow_html=True,
)

settings = load_settings()
tasks = list_tasks()
by_id = {t.id: t for t in tasks}

st.title("RepairLoop")
st.caption(
    f"v{__version__} · write / run / test / repair · "
    "NVIDIA Nemotron on Nebius Token Factory"
)

with st.sidebar:
    st.markdown("**stack**")
    st.text(f"model\n{settings.model}")
    st.text(f"base\n{settings.base_url}")
    st.write("nebius key:", "yes" if settings.has_nebius else "NO")
    st.write("tavily:", "yes" if settings.has_tavily else "no")
    max_iters = st.slider("max tool rounds", 1, 8, settings.max_iters)
    st.markdown("---")
    st.markdown(
        "Coding & Agentic Engineering  \n"
        "tools: write_file · run_python · run_tests"
        + (" · web_search" if settings.has_tavily else "")
    )

picked = st.selectbox(
    "task",
    options=[t.id for t in tasks],
    format_func=lambda i: f"{by_id[i].title}  ·  {by_id[i].difficulty}",
)
task = by_id[picked]

c1, c2 = st.columns([1.25, 1])
with c1:
    st.markdown("#### prompt")
    st.text(task.prompt)
with c2:
    st.markdown("#### grader checks")
    st.text(task.public_tests_hint)
    if task.tags:
        st.write("tags:", ", ".join(task.tags))

go = st.button("run agent", type="primary")

log = st.empty()
code_panel = st.empty()
status = st.empty()
metrics = st.empty()

if go:
    if not settings.has_nebius:
        status.error("Set NEBIUS_API_KEY in .env first")
        st.stop()

    lines: list[str] = []

    def on_progress(evt: dict) -> None:
        kind = evt.get("event")
        if kind == "thinking":
            lines.append(f"round {evt['iteration']}: model call")
        elif kind == "tool":
            lines.append(f"  {evt.get('name')}: {str(evt.get('result'))[:240]}")
            if evt.get("name") == "write_file":
                # reload code view lazily at end
                pass
            if evt.get("ok") is True:
                lines.append("  grader PASS")
            elif evt.get("ok") is False:
                lines.append("  grader FAIL")
        elif kind == "test":
            lines.append("  grader " + ("PASS" if evt.get("ok") else "FAIL"))
        log.text("\n".join(lines))

    with st.spinner("token factory…"):
        result = run_session(task, max_iters=max_iters, on_progress=on_progress)

    if result.error:
        status.error(result.error)
    elif result.success:
        status.success(f"passed in {result.iterations} round(s)")
    else:
        status.warning("still failing — see transcript")

    metrics.write(
        {
            "model": result.model,
            "prompt_tokens": result.prompt_tokens,
            "completion_tokens": result.completion_tokens,
            "est_cost_usd": round(result.est_cost_usd, 6),
            "transcript": result.transcript_path,
        }
    )
    code_panel.code(result.final_code or "# (no solution.py yet)", language="python")

st.markdown("---")
runs = Path("runs")
if runs.exists():
    recent = sorted(runs.glob("*.jsonl"), reverse=True)[:8]
    if recent:
        st.markdown("#### recent transcripts")
        for p in recent:
            st.text(str(p))
