# Devpost paste — RepairLoop

**Track:** Coding & Agentic Engineering  
**Deadline:** Oct 30, 2026 10:00 AM PT

## Project name
RepairLoop

## Tagline
A STEM coding agent that writes Python, runs hidden tests, and repairs with NVIDIA Nemotron on Nebius Token Factory.

## Built with
Nebius Token Factory, NVIDIA Nemotron, Python, Streamlit, Tavily (optional), Docker

## Description

### What it does
RepairLoop is a tool-using coding agent for lab-style STEM problems (circuits, arrays, DSP, control, sensors). It calls Nemotron on Nebius Token Factory, writes into a workspace, executes code, hits a hidden grader, and loops on failures.

This is closer to how terminal coding evals work than a chat “copilot” demo. There are eight graded tasks, reference oracles so every grader is proven solvable offline, JSONL transcripts, and a rough token/cost meter.

### How I built it
- `repairloop/session.py` — tool loop (write_file / run_python / run_tests / optional web_search)
- `repairloop/llm.py` — OpenAI-compatible Nebius client + usage meter
- `repairloop/sandbox.py` — per-run workspace with path guards + timeouts
- `tasks/*.json` — prompts + hidden unit tests
- `oracles/` — deterministic solutions; `python -m repairloop.eval --oracles-only`
- Streamlit UI (`app.py`), CLI, Docker, pytest

### Challenges
Getting models to stop narrating and actually call tools; stripping fences when they dump raw code; keeping the sandbox strict enough that “just import numpy” isn’t a fake win.

### What’s next
More physics/EE tasks from the same authoring pipeline, stricter sandboxing, and a small public leaderboard over the task suite.

## Nebius / NVIDIA usage
Runtime inference via Nebius Token Factory chat completions. Default model `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`. Optional Tavily `web_search` when `TAVILY_API_KEY` is set.

## Feedback
Token Factory’s OpenAI-compatible API made the agent thin. Nano is fast enough for multi-round repair; docs could highlight Nemotron model IDs on the quickstart. A hackathon preset (pinned model + agent rate-limit tips) would help.

## Video outline (~2 min)
1. Show README + blurred `.env` with Token Factory URL  
2. `pytest` / oracle check scrolling PASS  
3. Streamlit: run `rc_step_response` — tool calls — fail — repair — PASS  
4. Flash beamforming or thermistor task  
5. Point at public GitHub
