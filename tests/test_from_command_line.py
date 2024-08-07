import subprocess
import sys
from pathlib import Path

import pytest
from espanol_encuentro.constants import default_words_directory
from espanol_encuentro.entry import Entry, read_yaml_entries

from tests import dictionary_words


def run_command(command: list[str], use_example_script: bool, words_dir: Path | None) -> subprocess.CompletedProcess:
    command_prefix = (
        [sys.executable, str(Path(__file__).resolve().parent.parent / "example.py")]
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
def test_one_word_end_to_end(use_example_script: bool, tmp_path: Path) -> None:
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
    assert "me gusta mucho la comida" in lookup_output.stdout
    assert "preferimos la comida italiana" in lookup_output.stdout

    for starts_with in ("c", "d"):
        list_output = run_command(["list", "--starts-with", starts_with], use_example_script, words_dir)
        if starts_with == "c":
            assert "comida" in list_output.stdout
        else:
            assert "comida" not in list_output.stdout

    assert comida_yaml.is_file()
    run_command(["delete", "comida"], use_example_script, words_dir)
    assert not comida_yaml.exists()


def string_for_command_line(raw: str) -> str:
    return "'" + raw + "'" if " " in raw else raw


def assert_entries_equal(expected: list[Entry], actual: list[Entry]) -> None:
    assert len(expected) == len(actual)
    for this, that in zip(expected, actual, strict=False):
        assert this.word == that.word
        assert this.part_of_speech == that.part_of_speech
        assert this.short_definition == that.short_definition
        assert this.long_definition == that.long_definition
        assert this.examples == that.examples
        assert this.related_words == that.related_words


@pytest.mark.parametrize("word", dictionary_words())
def test_repopulate_entry(word: str, tmp_path: Path) -> None:
    entries = read_yaml_entries(default_words_directory() / f"{word}.yaml")
    for entry in entries:
        command_line = [
            "add",
            entry.word,
            "--part-of-speech",
            entry.part_of_speech,
            "--short-definition",
            string_for_command_line(entry.short_definition),
        ]

        if entry.long_definition:
            command_line.append("--long-definition")
            for item in entry.long_definition:
                command_line.append(string_for_command_line(item))

        if entry.examples:
            command_line.append("--examples")
            for item in entry.examples:
                command_line.append(string_for_command_line(item))

        if entry.related_words:
            command_line.append("--related-words")
            for item in entry.related_words:
                command_line.append(string_for_command_line(item))

        run_command(command_line, False, tmp_path / "words")

    new_file = tmp_path / "words" / f"{word}.yaml"
    new_entries = read_yaml_entries(new_file)
    assert_entries_equal(entries, new_entries)
