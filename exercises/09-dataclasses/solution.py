# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
from dataclasses import dataclass, field

# Write the Chunk dataclass here (file, page, seq, text, and the method preview).


# Write the Result dataclass here (id, retrieved, status, missing).


def chunks_of(file: str, pages: list[str]) -> list["Chunk"]:
    raise NotImplementedError
