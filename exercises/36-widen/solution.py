from dataclasses import dataclass

# ---- Given: the Chunk from exercise 31, the Passage and the budget. Do not change them. ----

@dataclass
class Chunk:
    file: str
    page: int
    seq: int          # its place in its file's order of chunks
    text: str


@dataclass
class Passage:
    file: str
    first_page: int
    last_page: int
    text: str


WIDEN_CHARS = 10_800


# ---- Yours ----

def widen(given: list[Chunk], everything: list[Chunk], budget: int = WIDEN_CHARS) -> list[Passage]:
    raise NotImplementedError
