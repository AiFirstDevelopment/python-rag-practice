# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
import json
import sys
from dataclasses import dataclass
from pathlib import Path


# Given: exercise 45's comparison. Do not change.
@dataclass
class Comparison:
    gained: list[str]      # ids that did not pass before and pass now, alphabetical
    lost: list[str]        # ids that passed before and do not now, alphabetical
    net: int               # len(gained) - len(lost)


def compare(before: dict[str, str], after: dict[str, str]) -> Comparison:
    both = sorted(set(before) & set(after))
    gained = [i for i in both if before[i] != "pass" and after[i] == "pass"]
    lost = [i for i in both if before[i] == "pass" and after[i] != "pass"]
    return Comparison(gained, lost, len(gained) - len(lost))


def verdict(comparison: Comparison, threshold: int = 2) -> str:
    if comparison.net >= threshold:
        return "gain"
    return "drop" if comparison.net <= -threshold else "noise"


# Yours.
def load_run(path: Path) -> dict[str, str]:
    raise NotImplementedError


def gate(before: dict[str, str], after: dict[str, str], threshold: int = 2) -> tuple[int, str]:
    raise NotImplementedError


def main(argv: list[str]) -> int:
    raise NotImplementedError


# Given: run as a script, the exit code is what main returns.
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
