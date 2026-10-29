from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .config import load_settings
from .session import run_session
from .tasks import list_tasks, load_task


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="repairloop",
        description="STEM coding agent on Nebius Token Factory / NVIDIA Nemotron",
    )
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="run agent on one task")
    run_p.add_argument("task")
    run_p.add_argument("--iters", type=int, default=None)

    sub.add_parser("tasks", help="list tasks")

    eval_p = sub.add_parser("eval", help="oracle check / agent suite")
    eval_p.add_argument("--oracles-only", action="store_true")
    eval_p.add_argument("--agent", action="store_true")
    eval_p.add_argument("--task", action="append", default=[])
    eval_p.add_argument("--iters", type=int, default=5)

    args = p.parse_args(argv)

    if args.cmd == "tasks":
        for t in list_tasks():
            print(f"{t.id:20} {t.difficulty:8} {t.title}")
        return 0

    if args.cmd == "eval":
        from .eval import main as eval_main

        argv2 = []
        if args.oracles_only:
            argv2.append("--oracles-only")
        if args.agent:
            argv2.append("--agent")
        for t in args.task:
            argv2.extend(["--task", t])
        argv2.extend(["--iters", str(args.iters)])
        return eval_main(argv2)

    if args.cmd == "run":
        settings = load_settings()
        print("model:", settings.model)
        print("tavily:", "on" if settings.has_tavily else "off")
        task = load_task(args.task)

        def on_progress(evt: dict) -> None:
            kind = evt.get("event")
            if kind == "tool":
                print(f"  tool {evt.get('name')} -> {str(evt.get('result'))[:120]}")
            elif kind == "thinking":
                print(f"iter {evt.get('iteration')} …")
            elif kind == "test":
                print("  test ok=" + str(evt.get("ok")))

        result = run_session(task, max_iters=args.iters, on_progress=on_progress)
        print(json.dumps({
            "success": result.success,
            "iters": result.iterations,
            "tokens": result.prompt_tokens + result.completion_tokens,
            "est_cost_usd": result.est_cost_usd,
            "transcript": result.transcript_path,
            "error": result.error,
        }, indent=2))
        if result.final_code:
            print("--- solution.py ---")
            print(result.final_code)
        return 0 if result.success and not result.error else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
