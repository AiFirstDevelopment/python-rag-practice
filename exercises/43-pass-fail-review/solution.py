# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
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


# Given: the phrases that mean "I don't know", and exercise 42's check. Do not change.
FALLBACK = ("don't know", "do not know", "not in the passages", "doesn't say", "does not say")


def missing_facts(facts: list[Fact], answer: str) -> list[str]:
    text = answer.lower()
    return [f.fact for f in facts if not any(m.lower() in text for m in f.match)]


# Yours.
def fell_back(reply: str) -> bool:
    raise NotImplementedError


def score_answer(case: Case, reply: str) -> tuple[str, list[str]]:
    raise NotImplementedError


def tally(statuses: list[str]) -> dict[str, int]:
    raise NotImplementedError
