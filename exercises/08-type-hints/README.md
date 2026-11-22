# 08. Type hints

> **Your lesson:** [lessons/08-type-hints.md](../../lessons/08-type-hints.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

Python runs without types, but a pipeline passes pages, chunks and scores through a dozen functions, and a hint on
each signature is how the next reader (and the editor, and pydantic later) knows what goes in and what comes out.
Python does not check hints when the code runs; they are read by tools and by people.

The starter in `solution.py` has three functions with no hints. Write each body, and add a type hint to every
parameter and to the return value:

- `first_words(text, n=5)`: takes a `str` and an `int`, returns a `str`: the first `n` words of `text` joined by
  single spaces. Fewer than `n` words gives all of them. The default `n` stays 5.
- `page_lengths(pages)`: takes a `list[str]` (the text of each page), returns a `dict[int, int]`: page number,
  counted from 1, to the number of characters on that page. No pages gives an empty dict.
- `longest_page(pages)`: takes a `list[str]`, returns a `tuple[int, str]`: the page number (from 1) and text of the
  page with the most characters; the earliest one when two are equally long. Raises `ValueError` when `pages` is
  empty.

The tests read the hints from each function and compare them with the ones above, so `list` alone is not enough: say
what is inside it.

```python
first_words("You can return any unused item within 30 days.", 3)   # "You can return"
page_lengths(["Returns", "Shipping costs"])                         # {1: 7, 2: 14}
longest_page(["Returns", "Shipping costs"])                         # (2, "Shipping costs")
```

You will use: `name: type` on parameters, `-> type` for the return value, `list[str]`, `dict[int, int]`,
`tuple[int, str]`, `enumerate(pages, 1)`.
