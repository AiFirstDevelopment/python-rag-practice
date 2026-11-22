# 31. Keep file and page with each chunk

> **Your lesson:** [lessons/31-chunk-pages.md](../../lessons/31-chunk-pages.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

An answer is only worth trusting if it says where it came from, so every chunk carries the file and the page it was
cut from. It also carries its place in its file's order of chunks, which exercise 36 uses to find the chunk before
and after it.

`chunk_page` from exercise 30 is given at the top of `solution.py`. Write two things:

- `Chunk`, a dataclass with four fields in this order: `file` (str), `page` (int), `seq` (int), `text` (str).
- `chunk_file(file, pages)`, where `pages` is a list with the text of each page of one file, in order. It returns
  the file's chunks as a list of `Chunk`, in reading order:
  - each page is cut with `chunk_page`, so a chunk never crosses a page;
  - `page` counts from 1: the first text in `pages` is page 1;
  - `seq` counts from 0 across the whole file, not per page: the first chunk of page 2 continues where page 1
    stopped;
  - a page with no text gives no chunks, but it still counts as a page, so the page after it keeps its number;
  - a file with no pages gives `[]`.

```python
chunk_file("returns.pdf", ["Page one.", "", "Page three."])
# [Chunk(file="returns.pdf", page=1, seq=0, text="Page one."),
#  Chunk(file="returns.pdf", page=3, seq=1, text="Page three.")]
```

You will use: `@dataclass`, `enumerate` with a start value, a nested loop or comprehension.
