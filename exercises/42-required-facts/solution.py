# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
from pydantic import BaseModel


# Given: one required fact of a golden case. Do not change.
class Fact(BaseModel):
    fact: str
    match: list[str]


# Yours.
def has_fact(fact: Fact, answer: str) -> bool:
    raise NotImplementedError


def missing_facts(facts: list[Fact], answer: str) -> list[str]:
    raise NotImplementedError
