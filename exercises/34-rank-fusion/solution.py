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


# rrf_scores(rankings): rankings is a list of ranked lists of chunks, best first. Return a dict from each chunk's
# (file, seq) to its fused score: in each list it is in it scores 1 / (RRF_K + rank), rank counting from 1, and its
# scores from the lists add up. A chunk in no list is not in the dict. Any number of lists works; none gives {}.
#   rrf_scores([[a, b], [c, b]])  ->  {("f.txt", 0): 1/61, ("f.txt", 1): 1/62 + 1/62, ("f.txt", 2): 1/61}
def rrf_scores(rankings: list[list[Chunk]]) -> dict[tuple[str, int], float]:
    raise NotImplementedError


# fuse(rankings, limit): return the chunks with the highest fused scores, best first, at most limit of them, each
# chunk once. Chunks with the same score stay in the order they were first met, reading the first list from its top,
# then the second, and so on. Any number of lists works; none gives [].
#   fuse([[a, b], [c, b]], 2)  ->  [b, a]     (b is second in both lists, and 2/62 beats 1/61)
def fuse(rankings: list[list[Chunk]], limit: int) -> list[Chunk]:
    raise NotImplementedError
