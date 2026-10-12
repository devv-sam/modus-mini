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


@pytest.mark.skip(reason="needs CSV fixture")
def test_reads_csv_in_workdir(tmp_path: Path) -> None:
    run_python("import pandas as pd; print(pd.read_csv('data.csv').shape)", tmp_path, timeout=5)


@pytest.mark.skip(reason="plots not built yet")
def test_collects_saved_plots(tmp_path: Path) -> None:
    run_python("open('plot.png', 'wb').write(b'')", tmp_path, timeout=5)
