# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
def find_chunk(chunks: list[dict], file: str, page: int) -> dict | None:
    raise NotImplementedError


def page_label(first_page: int, last_page: int | None = None) -> str:
    raise NotImplementedError


def to_pages(value: int | str | list[int]) -> list[int]:
    raise NotImplementedError


def retrieved_label(retrieved: bool | None) -> str:
    raise NotImplementedError
