# RepairLoop

STEM coding agent for the Nebius × NVIDIA hackathon  
**Track: Coding & Agentic Engineering**

Nemotron writes a `solution.py`, I run it against a hidden grader, failures go back into the model until tests pass or the iteration budget dies. That’s it.

Inference goes through **Nebius Token Factory** (`api.tokenfactory.nebius.com`) with an **NVIDIA Nemotron** model. The sandbox is local stdlib Python — no network, short timeout.

I built this because most “coding agent” demos never actually hit a real test harness. Coming from terminal-bench style task work, that felt backwards.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# put your Token Factory key in .env
```

Get a key: https://tokenfactory.nebius.com/ (API keys).  
Hackathon credits: Devpost / Builders Program / code `NEBIUS-DEVPOST-GLOBAL26`.

## Run

```bash
streamlit run app.py
```

or headless:

```bash
python cli.py --task rc_step_response
python cli.py --task beamforming_delay
python cli.py --task damped_modes   # flaky on nano, expected
```

## Layout

```
agent/llm.py       Token Factory client
agent/sandbox.py   run solution + tests
agent/loop.py      write / repair loop
agent/prompts.py   system + repair prompts
tasks/*.json       prompts + graders
app.py             streamlit ui
cli.py             no-ui runner
notes.txt          scratch notes from building this
SUBMIT.md          copy-paste for Devpost
```

Default model: `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`  
Override with `NEBIUS_MODEL` (Super/Ultra if you have credits).

## Hackathon compliance

- runtime call to Nebius Token Factory ✓  
- NVIDIA open model (Nemotron) ✓  
- agent that writes, runs, and tests code ✓  

## License

MIT
