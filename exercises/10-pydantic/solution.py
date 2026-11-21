from typing import Literal

from pydantic import BaseModel, Field, ValidationError

# Write the models Fact, Source and Case here.


def parse_case(line: str) -> "Case":
    raise NotImplementedError


def load_cases(lines: list[str]) -> tuple[list["Case"], list[int]]:
    raise NotImplementedError
