# prompts for the repair loop — keep them short, models wander otherwise

SYSTEM_PROMPT = """You write Python solutions for small scientific / engineering tasks.

Constraints:
- return one complete module (solution.py)
- stdlib only — no numpy, no scipy, no network
- match the I/O the task asks for
- if you see a failed test run, fix the bug; don't rewrite the whole API
- no prose, no markdown unless you wrap code in fences
"""


def first_turn(task_prompt: str, public_tests_hint: str) -> str:
    return (
        f"# Task\n\n{task_prompt}\n\n"
        f"# Public checks\n\n{public_tests_hint}\n\n"
        "Write solution.py. Code only."
    )


def repair_turn(
    task_prompt: str,
    previous_code: str,
    stdout: str,
    stderr: str,
    exit_code: int,
) -> str:
    return (
        f"# Task\n\n{task_prompt}\n\n"
        f"# Previous solution.py\n\n```python\n{previous_code}\n```\n\n"
        f"# Test result (exit {exit_code})\n\n"
        f"stdout:\n```\n{stdout or '(empty)'}\n```\n\n"
        f"stderr:\n```\n{stderr or '(empty)'}\n```\n\n"
        "Fix it. Return the full solution.py source only."
    )


def extract_python(text: str) -> str:
    """Models love fences. Peel them off if present."""
    t = text.strip()
    if "```" not in t:
        return t
    chunks = t.split("```")
    for i, chunk in enumerate(chunks):
        if i % 2 == 0:
            continue
        body = chunk
        if body.startswith("python"):
            body = body[6:]
        elif body.startswith("py"):
            body = body[2:]
        return body.lstrip("\n").rstrip()
    return t
