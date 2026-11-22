# Your task is in README.md in this folder. The code at the top is given; yours goes under "Yours" at line 18.
# Each EXERCISE-TODO comment below is one piece to write. Save, then type /check in the Claude chat.
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ValidationError


# Given: do not change.
class GoldenSetError(ValueError):
    """Raised when the golden set has bad lines. `lines` holds their line numbers, starting at 1."""

    def __init__(self, lines: list[int]):
        self.lines = lines
        super().__init__(f"bad lines in the golden set: {', '.join(str(n) for n in lines)}")


# Yours: give each model its fields (replace the `...`), then write load_cases.

# EXERCISE-TODO: Fact: a pydantic model with `fact` (a string, the fact in words) and `match` (a list of strings, any
# one of which in an answer counts as the fact). Both required.
class Fact(BaseModel):
    ...


# EXERCISE-TODO: Source: a pydantic model with `file` (a string) and `page` (an integer). Both required.
class Source(BaseModel):
    ...


# EXERCISE-TODO: Case: a pydantic model with `id` (string), `category` (one of "answerable", "inferred", "absent"),
# `question` (string), `expected_behavior` (one of "answer", "fallback"), `required_facts` (a list of Fact) and
# `sources` (a list of Source). Every field is required; the two lists may be empty.
class Case(BaseModel):
    ...


# EXERCISE-TODO: load_cases(path): read the file at path (UTF-8, one JSON case per line) and return its cases as a list
# of Case, in file order. A blank line (empty or only whitespace) is skipped. A line is bad when it is not JSON, does
# not fit Case (a field missing, a value not allowed), or reuses the id of an earlier good line. If any line is bad,
# raise GoldenSetError(lines) with the line numbers of every bad line in ascending order; line numbers start at 1 and
# count blank lines.
#   load_cases(Path("golden.jsonl"))[0].id  ->  "returns-01"
#   load_cases(Path("broken.jsonl"))        ->  GoldenSetError: bad lines in the golden set: 2, 5
def load_cases(path: Path) -> list[Case]:
    raise NotImplementedError
