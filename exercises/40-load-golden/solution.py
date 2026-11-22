# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
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
class Fact(BaseModel):
    ...


class Source(BaseModel):
    ...


class Case(BaseModel):
    ...


def load_cases(path: Path) -> list[Case]:
    raise NotImplementedError
