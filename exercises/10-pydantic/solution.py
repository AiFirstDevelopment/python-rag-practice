# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

# Write the models Fact, Source and Case here.
# Fact: a pydantic model with fact: str and match: list[str] (the spellings that count as stating the fact).
# Source: a pydantic model with file: str and page: int, where page must be 1 or more.
# Case: a pydantic model with id: str; question: str, at least one character long; expected_behavior, which must be
# exactly "answer" or "fallback"; required_facts: list[Fact]; sources: list[Source]. All five are required (the two
# lists may be empty).


# parse_case(line): return the Case for one line of JSON text. A line that is not JSON, or does not fit the model,
# raises pydantic's ValidationError (which is a ValueError).
#   parse_case(line).required_facts[0].match  ->  ["store credit"]   (line: the golden-set line in README.md)
#   parse_case('{"id": "x", "question": "Hi", "expected_behavior": "fallbak", "required_facts": [], "sources": []}')
#     ->  ValidationError: expected_behavior: Input should be 'answer' or 'fallback'
def parse_case(line: str) -> "Case":
    raise NotImplementedError


# load_cases(lines): takes the lines of a file and returns a tuple (cases, bad): the cases that parsed, in order, and
# the line numbers, counted from 1, of the lines that did not. A line that is empty or only whitespace is skipped:
# it is neither a case nor bad, but it still counts as a line.
#   load_cases([line, "", "not json", line])  ->  ([Case(...), Case(...)], [3])
def load_cases(lines: list[str]) -> tuple[list["Case"], list[int]]:
    raise NotImplementedError
