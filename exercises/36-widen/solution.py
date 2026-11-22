# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
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

# widen(given, everything, budget=WIDEN_CHARS): given is the chosen chunks, best first; everything is every chunk of
# every file. A chunk's neighbours are the chunks with the same file and seq - 1 and seq + 1. Return a list of Passage.
# Step 1: go through given in order; for each chunk look at the chunk before it, then after it, and take it unless it
# does not exist (another file's chunk is never a neighbour), it is a given chunk or already taken, or its text would
# bring the total length of the neighbours taken so far over budget (given chunks never count). A neighbour that does
# not fit is skipped and the walk goes on.
# Step 2: go through given in order again, skipping a chunk already inside an earlier passage. Its passage is the
# longest unbroken run of seq numbers around it, in its file, where every chunk is given or taken: the file, the page of
# the run's first chunk as first_page, the page of its last as last_page, and the texts joined with "\n".
# Passages are in the order of given. No given chunks gives [].
#   chunks = [Chunk("f.txt", 1, i, f"part {i}.") for i in range(5)]
#   widen([chunks[2]], chunks)  ->  [Passage("f.txt", 1, 1, "part 1.\npart 2.\npart 3.")]
#   widen([chunks[1], chunks[2]], chunks)  ->  one passage: "part 0.\npart 1.\npart 2.\npart 3."
def widen(given: list[Chunk], everything: list[Chunk], budget: int = WIDEN_CHARS) -> list[Passage]:
    raise NotImplementedError
