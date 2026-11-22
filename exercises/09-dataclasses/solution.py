# Your task is in README.md. Each EXERCISE-TODO comment below is one piece to write.
# Save, then type /check in the Claude chat.
from dataclasses import dataclass, field

# EXERCISE-TODO: Write the Chunk dataclass here (file, page, seq, text, and the method preview).
# Chunk: a dataclass with the fields file: str, page: int, seq: int, text: str, in that order (seq is the chunk's
# place in its file, counted from 0). Equal fields make equal chunks (==).
# preview(self, n=5): return the file, the page and the first n words of the text, in the form
# "returns.txt p.1: You can return any unused".
#   c = Chunk("returns.txt", 1, 0, "You can return any unused item within 30 days.")
#   c.preview()   ->  "returns.txt p.1: You can return any unused"
#   c.preview(2)  ->  "returns.txt p.1: You can"


# EXERCISE-TODO: Write the Result dataclass here (id, retrieved, status, missing).
# Result: what the eval harness records for one case: id: str, retrieved: bool | None, then two fields with
# defaults: status: str = "not run" and missing: list[str], which defaults to a new empty list. Two results made
# without missing must never share one list.
#   Result("returns-01", True)  ->  Result(id='returns-01', retrieved=True, status='not run', missing=[])


# EXERCISE-TODO: chunks_of(file, pages): takes the text of each page of one file and returns one Chunk per page that has
# text, in order. page is the page's number counted from 1; seq counts the chunks made, from 0. A page that is empty or
# only whitespace makes no chunk, but still counts as a page.
#   chunks_of("a.pdf", ["First.", "  ", "Third."])
#     ->  [Chunk(file='a.pdf', page=1, seq=0, text='First.'), Chunk(file='a.pdf', page=3, seq=1, text='Third.')]
def chunks_of(file: str, pages: list[str]) -> list["Chunk"]:
    raise NotImplementedError
