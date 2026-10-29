# Devpost paste pack — RepairLoop

**Track:** Coding & Agentic Engineering  
**Deadline:** Fri Oct 30, 2026 · 10:00 AM PT

---

## Project name
RepairLoop

## Tagline (short)
A STEM coding agent that writes Python, runs hidden tests, and repairs until it passes — on NVIDIA Nemotron via Nebius Token Factory.

## Elevator pitch / built with
Nebius Token Factory, NVIDIA Nemotron (Nano / optional Super), Python, Streamlit

## Full description (paste into Devpost)

### What it does
RepairLoop is a small coding agent aimed at lab-style STEM problems (circuits, arrays, signal fitting). You pick a task; the agent calls **NVIDIA Nemotron** on **Nebius Token Factory**, writes `solution.py`, runs a local sandbox + hidden unit tests, and if anything fails it sends stdout/stderr back to the model for another attempt.

That write → run → test → repair loop is the whole product. No chat UI pretending to be a “copilot” — just an agent that has to survive a grader the same way terminal coding benchmarks do.

### How I built it
- `agent/llm.py` — OpenAI-compatible client pointed at `https://api.tokenfactory.nebius.com/v1/`
- default model: `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B` (swap via `NEBIUS_MODEL`)
- `agent/sandbox.py` — subprocess runner with a stripped env and wall-clock timeout
- `agent/loop.py` — iteration budget, repair prompts, fence stripping
- three graded tasks under `tasks/` (RC τ fit, ULA steering delays, damped-cosine frequencies)
- Streamlit front-end in `app.py`, headless path in `cli.py`

### Why Nebius + Nemotron
Token Factory’s OpenAI-compatible API meant I could keep the agent thin. Nano is fast enough that multi-iteration repair is practical on demo credits; if a task needs heavier reasoning I can flip to Super/Ultra without changing code.

### What’s next
More tasks from the physics / EE set I’ve been authoring elsewhere, optional Tavily for pulling datasheet constraints into the prompt, and a stricter sandbox (seccomp / resource limits) if this grows past a hackathon demo.

### Built for
Nebius × NVIDIA Global AI Hackathon — Coding & Agentic Engineering track.

---

## How Nebius / NVIDIA were used (short field)
Runtime inference via Nebius Token Factory chat completions API. Model: NVIDIA Nemotron 3 Nano (`nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`). The agent loop depends on live Token Factory calls; the UI/sandbox stay local.

## Feedback on Token Factory / NVIDIA tools (required field)
Token Factory’s OpenAI-compatible endpoint made integration straightforward — drop in base_url + key and Nemotron just works. Nano is a good default for iterative repair loops; docs could surface the exact Nemotron model IDs more prominently on the quickstart. Would like a hackathon preset that pins a known-good Nemotron id + rate-limit tips for multi-turn agents.

---

## Video script (~2:00–2:30)

[0:00–0:15] Title card / talking head  
“RepairLoop — Coding & Agentic Engineering. Nemotron on Nebius Token Factory. Write, run, test, repair.”

[0:15–0:35] Show README + `.env` with Token Factory base URL (blur the key)  
“Only requirement for inference is a Token Factory key. Model id is Nemotron Nano.”

[0:35–0:55] Open Streamlit, select **RC circuit step-response fit**, hit Run  
Show sidebar: provider Nebius, model id visible.

[0:55–1:25] First iteration fails (or show stderr) then repair iteration  
Narrate: “It wrote solution.py, tests failed, stderr goes back to Nemotron…”

[1:25–1:50] Tests PASS — show final code briefly  
“Same loop I’d want in a terminal coding eval — the model doesn’t get to skip the grader.”

[1:50–2:15] Optional: switch task to beamforming delays, one clean pass  
Close: “Repo is public, MIT, setup in the README.”

Upload to YouTube → unlisted or public → paste URL on Devpost.

---

## Submission checklist
1. Create Token Factory key → `.env`
2. `streamlit run app.py` and record the video
3. Push this folder to a **public** GitHub/GitLab repo (LICENSE must show on the repo)
4. Demo URL: Streamlit Community Cloud **or** note “run locally — see README” + video (rules want a working demo URL if possible)
5. Enter on https://nebiusglobalaihackathon.devpost.com/ before **Oct 30 10:00 AM PT**
6. Select track **Coding & Agentic Engineering**
7. Paste feedback from above
