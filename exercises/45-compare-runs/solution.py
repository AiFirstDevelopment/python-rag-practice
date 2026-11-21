from dataclasses import dataclass


# Given: do not change.
@dataclass
class Comparison:
    gained: list[str]      # ids that did not pass before and pass now, alphabetical
    lost: list[str]        # ids that passed before and do not now, alphabetical
    net: int               # len(gained) - len(lost)


# Yours.
def compare(before: dict[str, str], after: dict[str, str]) -> Comparison:
    raise NotImplementedError


def verdict(comparison: Comparison, threshold: int = 2) -> str:
    raise NotImplementedError
