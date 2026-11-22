# 05. Functions and default arguments

> **Your lesson:** [lessons/05-functions.md](../../lessons/05-functions.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

Every chunk a pipeline keeps carries where it came from. Write the function that builds one.

Write `make_chunk(text, source, page=1, tags=None)` in `solution.py`. It returns a dict with the keys `"text"`,
`"source"`, `"page"` and `"tags"`. `tags` is a list: the one given, copied, or a new empty list.

```python
make_chunk("Returns within 30 days.", "returns.pdf")
# {"text": "Returns within 30 days.", "source": "returns.pdf", "page": 1, "tags": []}
make_chunk("Sale items are final.", "returns.pdf", page=2, tags=["sale"])
```

Then write `add_tag(chunk, tag)`: it adds `tag` to the chunk's tags unless it is already there, and returns the
chunk.

The tests check one trap in particular: two chunks made without tags must never share the same list.

You will use: default arguments, `None`, keyword arguments, `list(...)` to copy.
