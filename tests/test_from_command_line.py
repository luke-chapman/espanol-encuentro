import subprocess
import sys
from pathlib import Path
from typing import Literal, get_args

import pytest

Invocation = Literal["app", "script"]


def run_command(command: list[str], invocation: Invocation, words_dir: Path | None) -> subprocess.CompletedProcess:
    command_prefix = (
        [sys.executable, str(Path(__file__).resolve().parent.parent / "example.py")]
        if invocation == "script"
        else [sys.executable, "-m", "espanol_encuentro"]
    )

    if words_dir:
        command_prefix += ["--words-dir", str(words_dir)]

    return subprocess.run(command_prefix + command, check=True, capture_output=True, text=True)


@pytest.mark.parametrize("invocation", list(get_args(Invocation)))
def test_help(invocation: Invocation) -> None:
    output = run_command(["--help"], invocation, None)
    for mode in ("lookup", "add", "list", "delete"):
        assert mode in output.stdout


@pytest.mark.parametrize("invocation", list(get_args(Invocation)))
def test_one_word_end_to_end(invocation: Invocation, tmp_path: Path) -> None:
    words_dir = tmp_path / "words"

    run_command(
        [
            "add",
            "comida",
            "--part-of-speech",
            "noun_f",
            "--short-definition",
            "food",
            "--examples",
            "me gusta mucho la comida",
            "preferimos la comida italiana",
        ],
        invocation,
        words_dir,
    )

    comida_json = words_dir / "comida.json"
    assert comida_json.is_file()

    lookup_output = run_command(
        [
            "lookup",
            "comida",
        ],
        invocation,
        words_dir,
    )
    assert "food" in lookup_output.stdout
    assert "noun_f" in lookup_output.stdout
    assert "me gusta mucho la comida" in lookup_output.stdout
    assert "preferimos la comida italiana" in lookup_output.stdout

    for starts_with in ("c", "d"):
        list_output = run_command(["list", "--starts-with", starts_with], invocation, words_dir)
        if starts_with == "c":
            assert "comida" in list_output.stdout
        else:
            assert "comida" not in list_output.stdout

    assert comida_json.is_file()
    run_command(["delete", "comida"], invocation, words_dir)
    assert not comida_json.exists()
