# run agent-written code in a throwaway dir with a hard timeout

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class RunResult:
    ok: bool
    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool = False


def _clean_env(work_dir: Path, extra: dict[str, str] | None = None) -> dict[str, str]:
    env = {
        "HOME": str(work_dir),
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "LANG": "C.UTF-8",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONNOUSERSITE": "1",
        "OMP_NUM_THREADS": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "NUMEXPR_NUM_THREADS": "1",
    }
    if extra:
        env.update(extra)
    return env


def run_tests(
    source: str,
    test_source: str,
    *,
    timeout_sec: float = 12.0,
) -> RunResult:
    work = Path(tempfile.mkdtemp(prefix="repairloop_"))
    (work / "solution.py").write_text(source, encoding="utf-8")
    (work / "tests.py").write_text(test_source, encoding="utf-8")
    (work / "run_tests.py").write_text(
        "import traceback\n"
        "import tests\n"
        "try:\n"
        "    tests.run()\n"
        "    print('ALL_TESTS_PASSED')\n"
        "except Exception:\n"
        "    traceback.print_exc()\n"
        "    raise SystemExit(1)\n",
        encoding="utf-8",
    )

    env = _clean_env(work, {"PYTHONPATH": str(work)})
    try:
        proc = subprocess.run(
            [sys.executable, "-s", str(work / "run_tests.py")],
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            cwd=str(work),
            env=env,
        )
        passed = proc.returncode == 0 and "ALL_TESTS_PASSED" in proc.stdout
        return RunResult(
            ok=passed,
            exit_code=proc.returncode,
            stdout=proc.stdout[-8000:],
            stderr=proc.stderr[-8000:],
        )
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout if isinstance(exc.stdout, str) else ""
        err = exc.stderr if isinstance(exc.stderr, str) else ""
        return RunResult(
            ok=False,
            exit_code=124,
            stdout=(out or "")[-8000:],
            stderr=((err or "") + f"\ntimeout after {timeout_sec}s")[-8000:],
            timed_out=True,
        )
