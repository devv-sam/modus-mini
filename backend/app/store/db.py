import sqlite3
from pathlib import Path


def connect(path: Path) -> sqlite3.Connection:
    """Open the database and create the schema if missing."""
    raise NotImplementedError
