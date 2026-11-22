# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
from dataclasses import dataclass

# ---- Given: the Chunk from exercise 31. Do not change it. ----

@dataclass
class Chunk:
    file: str
    page: int
    seq: int          # its place in its file's order of chunks
    text: str


# ---- Yours ----

RRF_K = 60


def rrf_scores(rankings: list[list[Chunk]]) -> dict[tuple[str, int], float]:
    raise NotImplementedError


def fuse(rankings: list[list[Chunk]], limit: int) -> list[Chunk]:
    raise NotImplementedError
