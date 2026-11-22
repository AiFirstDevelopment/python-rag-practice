# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
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


# Given: exercise 43's scoring and one case's result. Do not change.
FALLBACK = ("don't know", "do not know", "not in the passages", "doesn't say", "does not say")


def score_answer(case: Case, reply: str) -> tuple[str, list[str]]:
    text = reply.lower()
    if case.expected_behavior == "fallback":
        return ("pass" if any(phrase in text for phrase in FALLBACK) else "review"), []
    missing = [f.fact for f in case.required_facts if not any(m.lower() in text for m in f.match)]
    return ("fail" if missing else "pass"), missing


@dataclass
class Result:
    id: str
    status: str                                   # pass, fail or review
    missing: list[str] = field(default_factory=list)
    error: str | None = None                      # the exception's message when the pipeline raised


# Yours.
async def run_cases(cases: list[Case], pipeline: Callable[[str], Awaitable[str]], limit: int = 4) -> list[Result]:
    raise NotImplementedError
