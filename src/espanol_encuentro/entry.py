import json
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field

PartOfSpeech = Literal["noun_f", "noun_m", "verb", "adjective"]


def _json_dump(item: Any) -> str:
    return json.dumps(item, indent=2, ensure_ascii=False)


class Entry(BaseModel):
    word: str
    part_of_speech: PartOfSpeech
    definition: str
    examples: list[str] = Field(default_factory=list)
    related_words: list[str] = Field(default_factory=list)

    def __str__(self) -> str:
        return _json_dump(self.model_dump(exclude_defaults=True))

    def __lt__(self, other):
        tuple_self = (self.word, self.part_of_speech, self.definition)
        tuple_other = (other.word, other.part_of_speech, other.definition)
        return tuple_self < tuple_other

    @staticmethod
    def __strip_quotes(raw: str) -> str:
        return raw.strip("\"'")

    def format(self) -> "Entry":
        return Entry(
            word=self.word,
            part_of_speech=self.part_of_speech,
            definition=self.definition.strip("\"'"),
            examples=sorted(s.strip("\"'") for s in self.examples),
            related_words=sorted(s.strip("\"'") for s in self.related_words),
        )


def read_json_entries(filename: Path) -> list[Entry]:
    with filename.open(encoding="utf-16") as f:
        model = json.load(f)
    return [Entry.model_validate(m) for m in model]


def write_json_entries(entries: list[Entry], filename: Path, verbose: bool = True) -> None:
    model = [e.model_dump(exclude_defaults=True) for e in entries]
    json_contents = _json_dump(model)
    filename.parent.mkdir(parents=True, exist_ok=True)
    filename.write_text(json_contents, encoding="utf-16")
    if verbose:
        print(f"Wrote {len(entries)} entries to {filename}")


def get_entries(directory: Path, word: str) -> list[Entry]:
    filename = directory / f"{word}.json"
    return read_json_entries(filename) if filename.is_file() else []
