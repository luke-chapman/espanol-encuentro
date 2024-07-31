from pathlib import Path

import yaml
from pydantic import BaseModel, Field
from typing import Literal

PartOfSpeech = Literal["noun_f", "noun_m", "verb", "adjective", ""]


class Entry(BaseModel):
    word: str
    part_of_speech: PartOfSpeech = ""
    short_definition: str = ""
    long_definition: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
    related_words: list[str] = Field(default_factory=list)

    def __str__(self) -> str:
        return yaml.safe_dump(self.model_dump(exclude_defaults=True), sort_keys=False)


def read_yaml_entries(filename: Path) -> list[Entry]:
    with filename.open() as f:
        contents = yaml.safe_load(f)
    entries = [Entry.model_validate(c) for c in contents]
    print(f"Read {len(entries)} entries from {filename}")
    return entries


def write_yaml_entries(entries: list[Entry], filename: Path) -> None:
    contents = [e.model_dump(exclude_defaults=True) for e in entries]
    filename.parent.mkdir(parents=True, exist_ok=True)
    with filename.open("w") as f:
        yaml.safe_dump(contents, f, sort_keys=False)
    print(f"Wrote {len(entries)} to {filename}")


def default_filename() -> Path:
    return Path(__file__).resolve().parent.parent.parent / "data" / "words.yaml"
