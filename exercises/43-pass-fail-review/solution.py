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

# fell_back(reply): return True when the reply contains any of the FALLBACK phrases, whatever the case of the reply.
def fell_back(reply: str) -> bool:
    raise NotImplementedError


# score_answer(case, reply): return a tuple (status, missing). For a case whose expected_behavior is "fallback":
# ("pass", []) when the reply fell back, ("review", []) when it did not. For an "answer" case: missing is the list from
# missing_facts, and the status is "fail" when something is missing, "pass" when nothing is. Falling back is not
# checked on an answer case: a right answer with a caveat passes, and a reply of only "I don't know" fails.
#   score_answer(answer_case, "As store credit.")    ->  ("fail", ["within 14 days"])
#   score_answer(fallback_case, "We open at nine.")  ->  ("review", [])
def score_answer(case: Case, reply: str) -> tuple[str, list[str]]:
    raise NotImplementedError


# tally(statuses): return how many of each status, as a dict that always has the three keys "pass", "fail" and
# "review", zero included.
#   tally(["pass", "review", "pass"])  ->  {"pass": 2, "fail": 0, "review": 1}
def tally(statuses: list[str]) -> dict[str, int]:
    raise NotImplementedError
