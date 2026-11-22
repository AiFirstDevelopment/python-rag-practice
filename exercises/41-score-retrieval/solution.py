# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel


# Given: the golden set's models from exercise 40. Do not change.
class Fact(BaseModel):
    fact: str
    match: list[str]


class Source(BaseModel):
    file: str
    page: int


class Case(BaseModel):
    id: str
    category: Literal["answerable", "inferred", "absent"]
    question: str
    expected_behavior: Literal["answer", "fallback"]
    required_facts: list[Fact]
    sources: list[Source]


# Given: what the pipeline retrieves. Do not change.
@dataclass
class Passage:
    file: str
    first_page: int
    last_page: int
    text: str


# Yours.
def source_found(source: Source, passages: list[Passage]) -> bool:
    raise NotImplementedError


def recall(case: Case, passages: list[Passage]) -> float | None:
    raise NotImplementedError


def mean_recall(recalls: list[float | None]) -> float:
    raise NotImplementedError
