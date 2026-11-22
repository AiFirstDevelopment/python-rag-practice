# 11. Optional and unions

> **Your lesson:** [lessons/11-optional.md](../../lessons/11-optional.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

Some values in a pipeline are honestly "one of several things": a search that may find nothing, a passage that
covers one page or a range, a harness result that is found, missed, or not applicable. Python writes these as
unions, `int | str`, and the commonest union is "this or nothing": `str | None`. The work is in telling the cases
apart, and `None` from `False`, `0` and `""`.

Write four functions in `solution.py`:

- `find_chunk(chunks, file, page)`: `chunks` is a list of dicts with the keys `"file"`, `"page"` and `"text"`.
  Returns the first one with that file and page, or `None` when there is none.
- `page_label(first_page, last_page=None)`: `"p.3"` for one page, `"pp.3-5"` for a range. `last_page` left out,
  `None`, or equal to `first_page` all mean one page.
- `to_pages(value)`: `value` is an `int`, a `str` or a `list[int]`, and the result is always a list of page numbers:
  `4` gives `[4]`; `"4"` gives `[4]`; `"3-5"` gives `[3, 4, 5]`; a list gives a new list with the same numbers (not
  the same list object). Spaces around the text or the numbers are allowed. A string that is neither form raises
  `ValueError`.
- `retrieved_label(retrieved)`: `retrieved` is `True`, `False` or `None`, as the harness records it: `True` gives
  `"found"`, `False` gives `"missed"`, and `None` (the case names no source, so there was nothing to find) gives
  `"no source"`.

```python
chunks = [{"file": "returns.txt", "page": 1, "text": "Returns within 30 days."}]
find_chunk(chunks, "returns.txt", 1)["text"]    # "Returns within 30 days."
find_chunk(chunks, "returns.txt", 2)            # None
page_label(3)                                   # "p.3"
page_label(3, 5)                                # "pp.3-5"
to_pages(" 3 - 5 ")                             # [3, 4, 5]
retrieved_label(None)                           # "no source"
```

You will use: `X | None` and `int | str | list[int]` in hints, `is None` and `is not None` (never `== None`),
`isinstance(value, int)`, `str.split("-")`, `range`.
