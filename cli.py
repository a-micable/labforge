#!/usr/bin/env python3
"""Run one task without the UI — useful for recording / quick checks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

from agent import llm, run_agent_loop

load_dotenv()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--task", default="rc_step_response")
    p.add_argument("--iters", type=int, default=4)
    args = p.parse_args()

    path = Path(__file__).resolve().parent / "tasks" / f"{args.task}.json"
    if not path.exists():
        print("unknown task:", args.task, file=sys.stderr)
        return 2

    task = json.loads(path.read_text(encoding="utf-8"))
    print("stack:", llm.describe_stack())

    def on_progress(evt: dict) -> None:
        print(evt.get("event"), "iter=", evt.get("iteration"), "ok=", evt.get("ok"))

    result = run_agent_loop(
        task_prompt=task["prompt"],
        public_tests_hint=task["public_tests_hint"],
        test_source=task["test_source"],
        max_iters=args.iters,
        on_progress=on_progress,
    )
    print("success=", result.success, "model=", result.model)
    if result.error:
        print(result.error, file=sys.stderr)
        return 1
    print("--- solution.py ---")
    print(result.final_code)
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
