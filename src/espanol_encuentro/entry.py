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
