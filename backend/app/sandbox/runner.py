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


MEMORY_LIMIT = 1024**3  # 1 GB, pandas + numpy reserve a lot of address space at import


def _limit_memory() -> None:
    """Cap the child's address space so runaway code gets a MemoryError."""
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT, MEMORY_LIMIT))


def run_python(code: str, workdir: Path, timeout: float) -> RunResult:
    """Run code in an isolated subprocess and capture stdout, stderr, and plots."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=workdir,
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
        )
    except subprocess.TimeoutExpired:
        return RunResult(stdout="", stderr="", returncode=None, timed_out=True)
