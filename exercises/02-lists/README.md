# 02. Lists and slicing

> **Your lesson:** [lessons/02-lists.md](../../lessons/02-lists.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

A pipeline often returns a chunk together with its neighbours, so the answer sees the sentence before and after.
That is a slice of a list.

Write `window(items, i, radius)` in `solution.py`: the items from position `i - radius` to `i + radius`, both
included, as a new list. Near either end, take what exists instead of failing or wrapping around.

```python
window(["a", "b", "c", "d", "e"], 2, 1)  # ["b", "c", "d"]
window(["a", "b", "c", "d", "e"], 0, 2)  # ["a", "b", "c"]
window(["a", "b", "c", "d", "e"], 4, 1)  # ["d", "e"]
```

Do not change the list you were given.

You will use: indexing, slicing, `max`, `min`, `len`.
