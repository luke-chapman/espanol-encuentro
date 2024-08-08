from pathlib import Path
from shutil import copytree

import pytest
from espanol_encuentro.__main__ import main
from espanol_encuentro.constants import default_words_directory
from espanol_encuentro.entry import Entry, read_json_entries, write_json_entries


def dictionary_words() -> list[str]:
    directory = default_words_directory()
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
    filename = default_words_directory() / f"{word}.json"
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
    entries = read_json_entries(default_words_directory() / f"{word}.json")
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


def test_sanitise_repo_words(tmp_path: Path) -> None:
    words_dir = tmp_path / "words"
    copytree(default_words_directory(), words_dir)

    files = sorted(words_dir.iterdir())
    assert len(files) > 0

    command_line = [
        "sanitise",
        "--words-dir",
        str(words_dir),
    ]
    main(command_line)

    sanitised_files = sorted(words_dir.iterdir())
    assert files == sanitised_files


# This test adds four words one by one and uses the "sanitise" command
# to fill in the other direction of links in between them
#
# comida (food) ---- bebida (a drink)
#   |                  |
#   |                  |
# comer (to eat) --- beber (to drink)
#
def test_sanitise_example_words(tmp_path: Path) -> None:
    words_dir = tmp_path / "words"
    commands = (
        ["add", "comida", "-p", "noun_f", "-d", "food", "-r", "comer", "bebida"],
        ["add", "bebida", "-p", "noun_f", "-d", "drink"],
        ["add", "comer", "-p", "verb", "-d", string_for_command_line("to eat"), "-r", "beber"],
        ["add", "beber", "-p", "verb", "-d", string_for_command_line("to drink"), "-r", "bebida"],
        ["sanitise"],
    )

    for command in commands:
        main(command + ["--words-dir", str(words_dir)])

    json_files = sorted(words_dir.iterdir())
    entries = {jf.with_suffix("").name: read_json_entries(jf) for jf in json_files}
    assert entries["beber"][0].related_words == ["bebida", "comer"]
    assert entries["bebida"][0].related_words == ["beber", "comida"]
    assert entries["comer"][0].related_words == ["beber", "comida"]
    assert entries["comida"][0].related_words == ["bebida", "comer"]
