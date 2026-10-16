import os
import resource
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class RunResult:
    stdout: str
    stderr: str
    returncode: int | None
    timed_out: bool
    plots: list[str]  # filenames of PNGs this run created


MEMORY_LIMIT = 1024**3  # 1 GB, pandas + numpy reserve a lot of address space at import


def _limit_memory() -> None:
    """Cap the child's address space so runaway code gets a MemoryError."""
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT, MEMORY_LIMIT))


def _new_plots(workdir: Path, before: set[Path]) -> list[str]:
    """Return the PNG filenames that appeared in workdir since before."""
    return sorted(p.name for p in set(workdir.glob("*.png")) - before)  # glob order is random


def run_python(code: str, workdir: Path, timeout: float) -> RunResult:
    """Run code in an isolated subprocess and capture stdout, stderr, and plots."""
    before = set(workdir.glob("*.png"))  # plots from earlier steps don't count
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": os.environ.get("HOME", ""),
        "MPLBACKEND": "Agg",  # no screen in a subprocess, render straight to files
    }  # built from scratch so secrets never reach the child
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=workdir,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            preexec_fn=_limit_memory if sys.platform == "linux" else None,  # macOS rejects rlimit
        )
        return RunResult(
            stdout=result.stdout,
            stderr=result.stderr,
            returncode=result.returncode,
            timed_out=False,
            plots=_new_plots(workdir, before),
        )
    except subprocess.TimeoutExpired:
        return RunResult(
            stdout="",
            stderr="",
            returncode=None,
            timed_out=True,
            plots=_new_plots(workdir, before),  # plots saved before the timeout still count
        )
