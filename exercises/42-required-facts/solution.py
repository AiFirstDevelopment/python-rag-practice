# Your task is in README.md in this folder. The code at the top is given; yours goes under "Yours" at line 12.
# Each EXERCISE-TODO comment below is one piece to write. Save, then type /check in the Claude chat.
from pydantic import BaseModel


# Given: one required fact of a golden case. Do not change.
class Fact(BaseModel):
    fact: str
    match: list[str]


# ---- Yours ----

# EXERCISE-TODO: has_fact(fact, answer): return True when at least one of the fact's match strings appears in the
# answer. Case does not matter on either side, and it is a substring search ("tennis ball" matches "tennis balls"). A
# fact with an empty match list is never found.
#   has_fact(Fact(fact="within 14 days", match=["14 days", "fourteen days"]), "Bring it back within Fourteen Days.")
#     ->  True
def has_fact(fact: Fact, answer: str) -> bool:
    raise NotImplementedError


# EXERCISE-TODO: missing_facts(facts, answer): return the `fact` text of every fact the answer does not hold, in the
# order the facts were given. An empty list means the answer holds them all.
#   missing_facts(facts, "You get Store Credit.")          ->  ["within 14 days"]
#   missing_facts(facts, "Store credit, within 14 days.")  ->  []
def missing_facts(facts: list[Fact], answer: str) -> list[str]:
    raise NotImplementedError
