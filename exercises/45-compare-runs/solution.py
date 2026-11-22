# Your task is in README.md in this folder. The code at the top is given; yours goes under "Yours" at line 14.
# Write it there, save, then type /check in the Claude chat.
from dataclasses import dataclass


# Given: do not change.
@dataclass
class Comparison:
    gained: list[str]      # ids that did not pass before and pass now, alphabetical
    lost: list[str]        # ids that passed before and do not now, alphabetical
    net: int               # len(gained) - len(lost)


# ---- Yours ----

# compare(before, after): each run is a dict from case id to status. Return a Comparison with gained (ids that did not
# pass before and pass now) and lost (ids that passed before and do not now), both in alphabetical order, and net as
# len(gained) - len(lost). Only "pass" counts as passing; "fail" to "review" is no flip. Only ids in both runs are
# compared; an id in only one is ignored.
#   compare({"a": "pass", "b": "fail", "c": "fail", "d": "pass"},
#           {"a": "pass", "b": "pass", "c": "pass", "d": "review"})
#     ->  Comparison(gained=["b", "c"], lost=["d"], net=1)
def compare(before: dict[str, str], after: dict[str, str]) -> Comparison:
    raise NotImplementedError


# verdict(comparison, threshold=2): return "gain" when net is at least threshold, "drop" when net is at most minus
# threshold, otherwise "noise".
#   verdict(Comparison(gained=["b", "c"], lost=["d"], net=1))               ->  "noise"
#   verdict(Comparison(gained=["b", "c"], lost=["d"], net=1), threshold=1)  ->  "gain"
def verdict(comparison: Comparison, threshold: int = 2) -> str:
    raise NotImplementedError
