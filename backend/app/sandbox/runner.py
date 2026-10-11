from pathlib import Path
from typing import Any


def run_python(code: str, workdir: Path, timeout: float) -> dict[str, Any]:
    """Run code in an isolated subprocess and capture stdout, stderr, and plots."""
    raise NotImplementedError
