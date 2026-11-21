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
