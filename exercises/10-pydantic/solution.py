# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

# Write the models Fact, Source and Case here.


def parse_case(line: str) -> "Case":
    raise NotImplementedError


def load_cases(lines: list[str]) -> tuple[list["Case"], list[int]]:
    raise NotImplementedError
