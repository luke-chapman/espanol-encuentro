from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field

PartOfSpeech = Literal["noun_f", "noun_m", "verb", "adjective"]


def _yaml_dump(item: Any) -> str:
    return yaml.safe_dump(item, sort_keys=False, allow_unicode=True)


class Entry(BaseModel):
    word: str
    part_of_speech: PartOfSpeech
    short_definition: str
    long_definition: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
    related_words: list[str] = Field(default_factory=list)

    def __str__(self) -> str:
        return _yaml_dump(self.model_dump(exclude_defaults=True))

    def __lt__(self, other):
        tuple_self = (self.word, self.part_of_speech, self.short_definition)
        tuple_other = (other.word, other.part_of_speech, other.short_definition)
        return tuple_self < tuple_other

    def format(self) -> "Entry":
        update = {"examples": sorted(self.examples), "related_words": sorted(self.related_words)}
        return self.model_copy(update=update)


def read_yaml_entries(filename: Path) -> list[Entry]:
    with filename.open() as f:
        model = yaml.safe_load(f)
    entries = [Entry.model_validate(m) for m in model]
    return entries


def write_yaml_entries(entries: list[Entry], filename: Path, verbose: bool = True) -> None:
    model = [e.model_dump(exclude_defaults=True) for e in entries]
    yaml_contents = _yaml_dump(model)
    filename.parent.mkdir(parents=True, exist_ok=True)
    filename.write_text(yaml_contents)
    if verbose:
        print(f"Wrote {len(entries)} entries to {filename}")


def get_entries(directory: Path, word: str) -> list[Entry]:
    filename = directory / f"{word}.yaml"
    return read_yaml_entries(filename) if filename.is_file() else []
