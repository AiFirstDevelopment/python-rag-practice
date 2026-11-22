# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
import math
import re
from collections import Counter
from dataclasses import dataclass

# ---- Given: the Chunk from exercise 31 and the word splitter. Do not change them. ----

@dataclass
class Chunk:
    file: str
    page: int
    seq: int          # its place in its file's order of chunks
    text: str


STOP = set("a an and are as at be by can could do does for from how i if in is it its me my of on or should so that "
           "the their them there this to was what when where which who why will with would you your".split())


def words(text: str) -> list[str]:
    """Lower-cased runs of letters and digits, stop words out, a plain plural's "s" off."""
    tokens = [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]
    return [w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w for w in tokens]


# ---- Yours ----

K1 = 1.2
B = 0.75


def bm25(chunks: list[Chunk], question: str, limit: int) -> list[Chunk]:
    raise NotImplementedError
