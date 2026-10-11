from pathlib import Path

import pytest

from app.sandbox.runner import run_python

pytestmark = pytest.mark.xfail(raises=NotImplementedError, strict=True)


def test_captures_stdout(tmp_path: Path) -> None:
    run_python("print('hi')", tmp_path, timeout=5)


def test_captures_stderr(tmp_path: Path) -> None:
    run_python("raise ValueError('boom')", tmp_path, timeout=5)


def test_timeout_kills_process(tmp_path: Path) -> None:
    run_python("while True: pass", tmp_path, timeout=1)


def test_reads_csv_in_workdir(tmp_path: Path) -> None:
    run_python("import pandas as pd; print(pd.read_csv('data.csv').shape)", tmp_path, timeout=5)


def test_collects_saved_plots(tmp_path: Path) -> None:
    run_python("open('plot.png', 'wb').write(b'')", tmp_path, timeout=5)
