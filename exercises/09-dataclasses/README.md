# 09. Dataclasses

> **Your lesson:** [lessons/09-dataclasses.md](../../lessons/09-dataclasses.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

In module 1 a chunk was a dict, and a typo in a key (`chunk["pgae"]`) only showed up when that line ran. The
pipeline keeps each chunk in a dataclass instead: a small class whose fields are declared once, with their types, and
which gets its constructor, its printed form and `==` written for it.

Write two dataclasses and one function in `solution.py`:

- `Chunk` with the fields `file: str`, `page: int`, `seq: int`, `text: str`, in that order (`seq` is the chunk's
  place in its file, counted from 0). Give it a method `preview(self, n=5)` that returns the file, the page and the
  first `n` words of the text, in the form `"returns.txt p.1: You can return any unused"`.
- `Result`, what the eval harness records for one case: `id: str`, `retrieved: bool | None`, then two fields with
  defaults: `status: str = "not run"` and `missing: list[str]`, which defaults to a new empty list. Two results
  made without `missing` must never share one list (the trap of exercise 05; a dataclass refuses `= []` and wants
  `field(default_factory=list)`).
- `chunks_of(file, pages)`: takes the text of each page of one file and returns one `Chunk` per page that has text,
  in order. `page` is the page's number counted from 1; `seq` counts the chunks made, from 0. A page that is empty
  or only whitespace makes no chunk, but still counts as a page.

```python
c = Chunk("returns.txt", 1, 0, "You can return any unused item within 30 days.")
c.preview()            # "returns.txt p.1: You can return any unused"
c.preview(2)           # "returns.txt p.1: You can"
c == Chunk("returns.txt", 1, 0, "You can return any unused item within 30 days.")   # True
Result("returns-01", True)   # Result(id='returns-01', retrieved=True, status='not run', missing=[])
chunks_of("a.pdf", ["First.", "  ", "Third."])
# [Chunk(file='a.pdf', page=1, seq=0, text='First.'), Chunk(file='a.pdf', page=3, seq=1, text='Third.')]
```

You will use: `@dataclass`, fields with types and defaults, `field(default_factory=list)`, a method with `self`,
`enumerate`.
