# Your task is in README.md in this folder. The code at the top is given; yours goes under "Yours" at line 38.
# Write it there, save, then type /check in the Claude chat.
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel


# Given: the golden set's models from exercise 40. Do not change.
class Fact(BaseModel):
    fact: str
    match: list[str]


class Source(BaseModel):
    file: str
    page: int


class Case(BaseModel):
    id: str
    category: Literal["answerable", "inferred", "absent"]
    question: str
    expected_behavior: Literal["answer", "fallback"]
    required_facts: list[Fact]
    sources: list[Source]


# Given: what the pipeline retrieves. Do not change.
@dataclass
class Passage:
    file: str
    first_page: int
    last_page: int
    text: str


# ---- Yours ----

# source_found(source, passages): return True when at least one passage is from the source's file and the source's
# page is within that passage's pages (first_page and last_page included). The same page in another file does not count.
#   passages = [Passage("shipping.pdf", 1, 2, "..."), Passage("returns.txt", 1, 1, "...")]
#   source_found(Source(file="shipping.pdf", page=2), passages)  ->  True
#   source_found(Source(file="warranty.txt", page=1), passages)  ->  False
def source_found(source: Source, passages: list[Passage]) -> bool:
    raise NotImplementedError


# recall(case, passages): return the fraction of the case's sources that were found, a float from 0.0 to 1.0. A case
# with no sources (a fallback case) has nothing to find: return None.
#   recall(case_with_those_two_sources, passages)  ->  0.5
#   recall(fallback_case, passages)                ->  None
def recall(case: Case, passages: list[Passage]) -> float | None:
    raise NotImplementedError


# mean_recall(recalls): return the average of the recalls that are not None; 0.0 if there are none to average.
#   mean_recall([1.0, 0.5, None])  ->  0.75
def mean_recall(recalls: list[float | None]) -> float:
    raise NotImplementedError
