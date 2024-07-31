from pathlib import Path

import yaml
from pydantic import BaseModel, Field
from typing import Any, Literal

PartOfSpeech = Literal["noun_f", "noun_m", "verb", "adjective", ""]


def _yaml_dump(item: Any) -> str:
    return yaml.safe_dump(item, sort_keys=False, allow_unicode=True)


class Entry(BaseModel):
    word: str
    part_of_speech: PartOfSpeech = ""
    short_definition: str = ""
    long_definition: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
    related_words: list[str] = Field(default_factory=list)

    def __str__(self) -> str:
        return _yaml_dump(self.model_dump(exclude_defaults=True))


def read_yaml_entries(filename: Path) -> list[Entry]:
    with filename.open() as f:
        model = yaml.safe_load(f)
    entries = [Entry.model_validate(m) for m in model]
    print(f"Read {len(entries)} entries from {filename}")
    return entries


def write_yaml_entries(entries: list[Entry], filename: Path) -> None:
    model = [e.model_dump(exclude_defaults=True) for e in entries]
    yaml_contents = _yaml_dump(model)
    filename.parent.mkdir(parents=True, exist_ok=True)
    filename.write_text(yaml_contents)
    print(f"Wrote {len(entries)} to {filename}")


def default_filename() -> Path:
    return Path(__file__).resolve().parent.parent.parent / "words.yaml"
