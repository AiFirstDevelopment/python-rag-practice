# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.

# find_chunk(chunks, file, page): chunks is a list of dicts with the keys "file", "page" and "text". Return the
# first one with that file and page, or None when there is none.
#   find_chunk(chunks, "returns.txt", 1)["text"]  ->  "Returns within 30 days."
#   find_chunk(chunks, "returns.txt", 2)          ->  None
#   (chunks = [{"file": "returns.txt", "page": 1, "text": "Returns within 30 days."}])
def find_chunk(chunks: list[dict], file: str, page: int) -> dict | None:
    raise NotImplementedError


# page_label(first_page, last_page=None): return "p.3" for one page, "pp.3-5" for a range. last_page left out,
# None, or equal to first_page all mean one page.
#   page_label(3)     ->  "p.3"
#   page_label(3, 5)  ->  "pp.3-5"
def page_label(first_page: int, last_page: int | None = None) -> str:
    raise NotImplementedError


# to_pages(value): value is an int, a str or a list[int]; return a list of page numbers: 4 gives [4]; "4" gives [4];
# "3-5" gives [3, 4, 5]; a list gives a new list with the same numbers (not the same list object). Spaces around the
# text or the numbers are allowed. A string that is neither form raises ValueError.
#   to_pages(" 3 - 5 ")  ->  [3, 4, 5]
def to_pages(value: int | str | list[int]) -> list[int]:
    raise NotImplementedError


# retrieved_label(retrieved): retrieved is True, False or None; return "found" for True, "missed" for False, and
# "no source" for None (the case names no source, so there was nothing to find).
#   retrieved_label(None)  ->  "no source"
def retrieved_label(retrieved: bool | None) -> str:
    raise NotImplementedError
