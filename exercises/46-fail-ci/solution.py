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

# load_run(path): return the run file at path (JSONL, one {"id": ..., "status": ...} a line) as a dict from id to
# status. Blank lines are skipped.
def load_run(path: Path) -> dict[str, str]:
    raise NotImplementedError


# gate(before, after, threshold=2): compare the two runs (dicts) and return a tuple (code, message). code is 1 when the
# verdict is "drop", otherwise 0. message is one line containing the verdict word (drop, gain or noise); on a drop it
# also contains the id of every lost case. The rest of the wording is yours.
#   a drop of three  ->  (1, "drop: 3 lost (returns-02, shipping-01, warranty-01), 0 gained")
def gate(before: dict[str, str], after: dict[str, str], threshold: int = 2) -> tuple[int, str]:
    raise NotImplementedError


# main(argv): argv is the command-line arguments without the program name: the baseline run file's path, then the new
# one's. Print the gate's message and return its code, with the default threshold. If argv does not hold exactly two
# arguments, print a line containing the word "usage" and return 2. If either file does not exist, print a line
# containing that file's path and return 2.
def main(argv: list[str]) -> int:
    raise NotImplementedError


# Given: run as a script, the exit code is what main returns.
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
