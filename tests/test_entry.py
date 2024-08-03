from pathlib import Path

import pytest
from espanol_encuentro.constants import words_directory
from espanol_encuentro.entry import read_yaml_entries, write_yaml_entries


def __words() -> list[str]:
    directory = words_directory()
    return [f.name[:-5] for f in directory.iterdir() if f.suffix == ".yaml"]


@pytest.mark.parametrize("word", __words())
def test_serialization_roundtrip(word: str, tmp_path: Path) -> None:
    filename = words_directory() / f"{word}.yaml"
    entries = read_yaml_entries(filename)
    assert len(entries) >= 1, f"Expected at least one entry for word '{word}'"

    tmp_filename = tmp_path / filename.name
    write_yaml_entries(entries, tmp_filename)
    tmp_entries = read_yaml_entries(tmp_filename)
    assert tmp_entries == entries
