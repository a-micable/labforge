# the whole product: ask model for code, grade it, ask again if it fails

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from . import llm, prompts
from .sandbox import RunResult, run_tests

ProgressCb = Callable[[dict[str, Any]], None]


@dataclass
class AgentStep:
    iteration: int
    code: str
    result: RunResult
    model_raw: str = ""


@dataclass
class AgentResult:
    success: bool
    final_code: str
    steps: list[AgentStep] = field(default_factory=list)
    model: str = ""
    error: str = ""


def run_agent_loop(
    *,
    task_prompt: str,
    public_tests_hint: str,
    test_source: str,
    max_iters: int = 4,
    on_progress: ProgressCb | None = None,
) -> AgentResult:
    model = llm.get_model()
    messages: list[dict[str, str]] = [
        {"role": "system", "content": prompts.SYSTEM_PROMPT},
        {
            "role": "user",
            "content": prompts.first_turn(task_prompt, public_tests_hint),
        },
    ]

    steps: list[AgentStep] = []
    last_code = ""

    try:
        for i in range(1, max_iters + 1):
            if on_progress:
                on_progress({"event": "thinking", "iteration": i, "model": model})

            raw = llm.chat(messages, temperature=0.2, max_tokens=4096)
            code = prompts.extract_python(raw)
            last_code = code

            if on_progress:
                on_progress({"event": "code", "iteration": i, "code": code})

            result = run_tests(code, test_source)
            steps.append(
                AgentStep(iteration=i, code=code, result=result, model_raw=raw)
            )

            if on_progress:
                on_progress(
                    {
                        "event": "test",
                        "iteration": i,
                        "ok": result.ok,
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                        "exit_code": result.exit_code,
                    }
                )

            if result.ok:
                return AgentResult(
                    success=True, final_code=code, steps=steps, model=model
                )

            # stick the failure back into the chat and try again
            messages.append({"role": "assistant", "content": raw})
            messages.append(
                {
                    "role": "user",
                    "content": prompts.repair_turn(
                        task_prompt,
                        code,
                        result.stdout,
                        result.stderr,
                        result.exit_code,
                    ),
                }
            )

        return AgentResult(
            success=False, final_code=last_code, steps=steps, model=model
        )
    except Exception as exc:  # surface to the UI / cli
        return AgentResult(
            success=False,
            final_code=last_code,
            steps=steps,
            model=model,
            error=str(exc),
        )
