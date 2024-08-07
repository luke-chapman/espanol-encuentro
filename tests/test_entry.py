from pathlib import Path

import pytest
from espanol_encuentro.constants import default_words_directory
from espanol_encuentro.entry import read_yaml_entries, write_yaml_entries

from tests import dictionary_words


@pytest.mark.parametrize("word", dictionary_words())
def test_serialization_roundtrip(word: str, tmp_path: Path) -> None:
    filename = default_words_directory() / f"{word}.yaml"
    entries = read_yaml_entries(filename)
    assert len(entries) >= 1, f"Expected at least one entry for word '{word}'"

    tmp_filename = tmp_path / filename.name
    write_yaml_entries(entries, tmp_filename)
    tmp_entries = read_yaml_entries(tmp_filename)
    assert tmp_entries == entries
