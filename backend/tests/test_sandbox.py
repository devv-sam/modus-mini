import sys
from pathlib import Path

import pytest

from app.sandbox.runner import run_python


def test_captures_stdout(tmp_path: Path) -> None:
    result = run_python("print('hi')", tmp_path, timeout=5)
    assert result.stdout == "hi\n"
    assert result.returncode == 0


def test_captures_stderr(tmp_path: Path) -> None:
    result = run_python("raise ValueError('boom')", tmp_path, timeout=5)
    assert "ValueError: boom" in result.stderr
    assert result.returncode == 1


def test_timeout_kills_process(tmp_path: Path) -> None:
    result = run_python("while True: pass", tmp_path, timeout=1)
    assert result.timed_out


def test_reads_csv_in_workdir(tmp_path: Path) -> None:
    (tmp_path / "data.csv").write_text("a,b\n1,2\n3,4\n")  # 2 rows, 2 columns, header not counted
    code = "import pandas as pd; print(pd.read_csv('data.csv').shape)"  # relative path, needs cwd
    result = run_python(code, tmp_path, timeout=5)
    assert result.returncode == 0
    assert result.stdout == "(2, 2)\n"


@pytest.mark.skipif(sys.platform != "linux", reason="rlimit not supported on macOS")
def test_memory_limit(tmp_path: Path) -> None:
    result = run_python("x = bytearray(2 * 1024**3)", tmp_path, timeout=5)  # 2 GB, over the cap
    assert "MemoryError" in result.stderr


@pytest.mark.skip(reason="plots not built yet")
def test_collects_saved_plots(tmp_path: Path) -> None:
    run_python("open('plot.png', 'wb').write(b'')", tmp_path, timeout=5)
