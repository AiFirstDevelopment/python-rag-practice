# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.

# make_chunk(text, source, page=1, tags=None): return a dict with the keys "text", "source", "page" and "tags".
# tags is a list: the one given, copied, or a new empty list. Two chunks made without tags must never share the
# same list.
#   make_chunk("Returns within 30 days.", "returns.pdf")
#     ->  {"text": "Returns within 30 days.", "source": "returns.pdf", "page": 1, "tags": []}
#   make_chunk("Sale items are final.", "returns.pdf", page=2, tags=["sale"])
def make_chunk(text: str, source: str, page: int = 1, tags: list[str] | None = None) -> dict:
    raise NotImplementedError


# add_tag(chunk, tag): add tag to the chunk's tags unless it is already there, and return the chunk.
def add_tag(chunk: dict, tag: str) -> dict:
    raise NotImplementedError
