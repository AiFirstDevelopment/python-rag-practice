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


def chunk_file(file: str, pages: list[str]) -> list["Chunk"]:
    raise NotImplementedError
