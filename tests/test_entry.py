from pathlib import Path

import pytest
from espanol_encuentro.__main__ import main
from espanol_encuentro.constants import default_words_directory
from espanol_encuentro.entry import Entry, read_json_entries, write_json_entries


def dictionary_words() -> list[str]:
    directory = default_words_directory()
    return sorted(f.name[:-5] for f in directory.iterdir() if f.suffix == ".json")


@pytest.mark.parametrize("word", dictionary_words())
def test_serialization_roundtrip(word: str, tmp_path: Path) -> None:
    filename = default_words_directory() / f"{word}.json"
    entries = read_json_entries(filename)
    assert len(entries) >= 1, f"Expected at least one entry for word '{word}'"

    tmp_filename = tmp_path / filename.name
    write_json_entries(entries, tmp_filename)
    tmp_entries = read_json_entries(tmp_filename)
    assert tmp_entries == entries


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
    entries = read_json_entries(default_words_directory() / f"{word}.json")
    for entry in entries:
        command_line = [
            "--words-dir",
            str(tmp_path / "words"),
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

        main(command_line)

    new_file = tmp_path / "words" / f"{word}.json"
    new_entries = read_json_entries(new_file)
    assert_entries_equal(entries, new_entries)
