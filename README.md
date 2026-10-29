# RepairLoop

Coding agent for lab-style STEM problems.

It calls **NVIDIA Nemotron** through **Nebius Token Factory**, writes into a workspace, runs a hidden grader, and keeps repairing until the tests pass (or the round budget is gone).

Built for the Nebius × NVIDIA Global AI Hackathon — **Coding & Agentic Engineering**.

I’ve spent a while authoring terminal / agent eval tasks in math + EE/physics. Most demos skip the grader. This one doesn’t.

## What you get

- tool-using agent (`write_file`, `read_file`, `run_python`, `run_tests`, optional `web_search` via Tavily)
- 8 graded STEM tasks (circuits, arrays, DSP, control, sensors, quaternions, modal freq)
- reference **oracles** that prove every grader is solvable without an LLM
- JSONL **transcripts** + rough token/cost meter
- Streamlit UI + CLI + Docker
- pytest covering schema, sandbox, and oracles

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
cp .env.example .env
# set NEBIUS_API_KEY (and optional TAVILY_API_KEY)
```

```bash
# UI
streamlit run app.py

# CLI
python -m repairloop.cli tasks
python -m repairloop.cli run rc_step_response
python -m repairloop.cli run beamforming_delay --iters 6

# prove graders locally (no API key)
python -m repairloop.eval --oracles-only
pytest -q
```

Token Factory key: https://tokenfactory.nebius.com/  
Hackathon credits form code often listed as `NEBIUS-DEVPOST-GLOBAL26` on Devpost.

## Layout

```
repairloop/          library (llm, tools, sandbox, session, eval)
tasks/               grader JSON (prompt + hidden tests)
oracles/             known-good solutions for offline checks
tests/               pytest
runs/                transcripts (gitignored)
app.py               streamlit
Dockerfile
SUBMIT.md            Devpost paste pack
notes.txt            build notes
```

Default model: `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`  
Override with `NEBIUS_MODEL`.

## How it maps to the rules

| Rule | Here |
|---|---|
| Runs on Nebius | live chat.completions → `api.tokenfactory.nebius.com` |
| NVIDIA open model | Nemotron Nano (Super/Ultra via env) |
| Coding & Agentic Engineering | agent writes, executes, grades, repairs |
| Optional Tavily | set `TAVILY_API_KEY` → `web_search` tool |

## Notes / limits

- sandbox is stdlib Python only (intentional — matches a lot of eval constraints)
- `damped_modes` and `snr_fft_tone` are the flaky ones on Nano; expect retries
- price estimates in the UI are approximate from a static table in `config.py`

## License

MIT — see LICENSE.
