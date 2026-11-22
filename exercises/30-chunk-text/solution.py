# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
CHUNK_CHARS = 900
ENDS = (". ", "? ", "! ", ".\n", "?\n", "!\n")


def chunk_page(text: str) -> list[str]:
    raise NotImplementedError
