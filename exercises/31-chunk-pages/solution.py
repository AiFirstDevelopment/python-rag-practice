# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
from dataclasses import dataclass

# ---- Given: chunk_page from exercise 30. Do not change it. ----

CHUNK_CHARS = 900
ENDS = (". ", "? ", "! ", ".\n", "?\n", "!\n")


def chunk_page(text: str) -> list[str]:
    pieces, rest = [], text.strip()
    while len(rest) > CHUNK_CHARS:
        window = rest[:CHUNK_CHARS]
        sentence = max(window.rfind(end) for end in ENDS)
        space = window.rfind(" ")
        cut = sentence + 1 if sentence > CHUNK_CHARS / 2 else space if space > 0 else CHUNK_CHARS
        pieces.append(rest[:cut].strip())
        rest = rest[cut:].strip()
    if rest:
        pieces.append(rest)
    return pieces


# ---- Yours ----

# Write the Chunk dataclass here: file, page, seq, text.
# Chunk: a dataclass with four fields in this order: file (str), page (int), seq (int), text (str).


# chunk_file(file, pages): pages is the text of each page of one file, in order. Return the file's chunks as a list
# of Chunk, in reading order. Each page is cut with chunk_page, so a chunk never crosses a page. page counts from 1
# (the first text in pages is page 1); seq counts from 0 across the whole file, not per page. A page with no text gives
# no chunks but still counts as a page, so the page after it keeps its number. A file with no pages gives [].
#   chunk_file("returns.pdf", ["Page one.", "", "Page three."])
#     ->  [Chunk("returns.pdf", 1, 0, "Page one."), Chunk("returns.pdf", 3, 1, "Page three.")]
def chunk_file(file: str, pages: list[str]) -> list["Chunk"]:
    raise NotImplementedError
