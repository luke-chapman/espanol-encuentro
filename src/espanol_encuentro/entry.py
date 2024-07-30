from pathlib import Path

import yaml
from pydantic import BaseModel, Field
from typing import Literal

PartOfSpeech = Literal["noun_f", "noun_m", "verb", "adjective"]


class Entry(BaseModel):
    word: str
    simple_definition: str
    part_of_speech: PartOfSpeech
    longer_definition: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
    related_words: list[str] = Field(default_factory=list)


def read_yaml_entries(filename: Path) -> list[Entry]:
    with filename.open() as f:
        contents = yaml.safe_load(f)
    return [Entry.model_validate(c) for c in contents]


def write_yaml_entries(entries: list[Entry], filename: Path) -> None:
    contents = [e.model_dump(exclude_defaults=True) for e in entries]
    filename.parent.mkdir(parents=True, exist_ok=True)
    with filename.open("w") as f:
        yaml.safe_dump(contents, f)
