from pathlib import Path
from typing import Any


def tool_schemas() -> list[dict[str, Any]]:
    """Return the tool definitions sent to Claude."""
    raise NotImplementedError


def dispatch(name: str, args: dict[str, Any], workdir: Path) -> str:
    """Execute a tool call and return its result as text for the model."""
    raise NotImplementedError
