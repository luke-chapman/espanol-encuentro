from pathlib import Path

import pytest

from espanol_encuentro.__main__ import main
from espanol_encuentro.entry import Entry, read_json_entries, write_json_entries


def sample_words_directory() -> Path:
    return Path(__file__).resolve().parent / "example_words"


def dictionary_words() -> list[str]:
    directory = sample_words_directory()
    return sorted(f.name[:-5] for f in directory.iterdir() if f.suffix == ".json")


def assert_entries_equal(expected: list[Entry], actual: list[Entry]) -> None:
    assert len(expected) == len(actual)
    for this, that in zip(expected, actual, strict=False):
        if this != that:
            print(f"{this}")
            print(f"{that}")
            raise AssertionError("Entries are not equal - see earlier logging for details")


@pytest.mark.parametrize("word", dictionary_words())
def test_serialization_roundtrip(word: str, tmp_path: Path) -> None:
    filename = sample_words_directory() / f"{word}.json"
    entries = read_json_entries(filename)
    assert len(entries) >= 1, f"Expected at least one entry for word '{word}'"

    tmp_filename = tmp_path / filename.name
    write_json_entries(entries, tmp_filename)
    tmp_entries = read_json_entries(tmp_filename)
    assert_entries_equal(entries, tmp_entries)


def string_for_command_line(raw: str) -> str:
    return "'" + raw + "'" if " " in raw else raw


@pytest.mark.parametrize("word", dictionary_words())
def test_repopulate_entry(word: str, tmp_path: Path) -> None:
    entries = read_json_entries(sample_words_directory() / f"{word}.json")
    for entry in entries:
        command_line = [
            "add",
            entry.word,
            "--part-of-speech",
            entry.part_of_speech,
            "--definition",
            string_for_command_line(entry.definition),
            "--words-dir",
            str(tmp_path / "words"),
        ]

        if entry.examples:
            command_line.append("--examples")
            for item in entry.examples:
                command_line.append(string_for_command_line(item))

        if entry.related_words:
            command_line.append("--related-words")
            for item in entry.related_words:
                command_line.append(string_for_command_line(item))

        main(command_line)

    new_file = tmp_path / "words" / f"{word}.json"
    new_entries = read_json_entries(new_file)
    assert_entries_equal(entries, new_entries)
