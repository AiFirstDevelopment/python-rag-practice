# Your task is in README.md in this folder. The code at the top is given; yours goes under "Yours" at line 28.
# Each EXERCISE-TODO comment below is one piece to write. Save, then type /check in the Claude chat.
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


# EXERCISE-TODO: bm25(chunks, question, limit): return the chunks that share at least one word with the question (use
# words() for the chunks and the question), best score first, at most limit of them. A chunk's score is the sum, over
# each distinct word w of the question that the chunk holds, of
#   idf(w) * tf * (K1 + 1) / (tf + K1 * (1 - B + B * length / average))
#   idf(w) = ln(1 + (N - n + 0.5) / (n + 0.5))
# where tf is how many times w is in the chunk's words, length is how many words the chunk has, average is the mean
# length over all the chunks, N is the number of chunks, n is the number of chunks that hold w, and ln is math.log.
# A word in the question twice counts once. A chunk with no word of the question is not in the result, so the result
# can be shorter than limit, or empty. No chunks gives []. Return the Chunk objects themselves, not copies or texts.
#   chunks with texts "shipping is free", "refund refund policy", "refund window policy":
#   bm25(chunks, "refund", 5)  ->  [chunks[1], chunks[2]]
def bm25(chunks: list[Chunk], question: str, limit: int) -> list[Chunk]:
    raise NotImplementedError
