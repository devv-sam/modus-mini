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


def run_python(code: str, workdir: Path, timeout: float) -> RunResult:
    """Run code in an isolated subprocess and capture stdout, stderr, and plots."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return RunResult(
            stdout=result.stdout,
            stderr=result.stderr,
            returncode=result.returncode,
            timed_out=False,
        )
    except subprocess.TimeoutExpired:
        return RunResult(stdout="", stderr="", returncode=None, timed_out=True)
