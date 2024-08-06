import subprocess
import sys
from pathlib import Path

import pytest


def run_command(command: list[str], use_example_script: bool, words_dir: Path | None) -> subprocess.CompletedProcess:
    command_prefix = (
        [sys.executable, Path(__file__).resolve().parent.parent / "example.py"]
        if use_example_script
        else [sys.executable, "-m", "espanol_encuentro"]
    )

    if words_dir:
        command_prefix += ["--words-dir", str(words_dir)]

    return subprocess.run(command_prefix + command, check=True, capture_output=True, text=True)


@pytest.mark.parametrize("use_example_script", [False, True])
def test_help(use_example_script: bool) -> None:
    run_command(["--help"], use_example_script, None)


@pytest.mark.parametrize("use_example_script", [False, True])
def test_end_to_end(use_example_script: bool, tmp_path: Path) -> None:
    words_dir = tmp_path / "words"

    run_command(
        [
            "add",
            "comida",
            "--part-of-speech",
            "noun_f",
            "--short-definition",
            "food",
        ],
        use_example_script,
        words_dir,
    )

    comida_yaml = words_dir / "comida.yaml"
    assert comida_yaml.is_file()

    lookup_output = run_command(
        [
            "lookup",
            "comida",
        ],
        use_example_script,
        words_dir,
    )
    assert "food" in lookup_output.stdout
    assert "noun_f" in lookup_output.stdout

    for starts_with in ("c", "d"):
        list_output = run_command(["list", "--starts-with", starts_with], use_example_script, words_dir)
        if starts_with == "c":
            assert "comida" in list_output.stdout
        else:
            assert "comida" not in list_output.stdout

    assert comida_yaml.is_file()
    run_command(["delete", "comida"], use_example_script, words_dir)
    assert not comida_yaml.exists()
