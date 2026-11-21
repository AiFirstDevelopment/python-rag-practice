# 34. Reciprocal rank fusion

Keyword search and vector search each return a ranked list, and their scores cannot be compared: a BM25 score and a
cosine similarity are different units. Reciprocal rank fusion ignores the scores and uses only the places: a chunk
near the top of either list does well, and a chunk both searches found does best.

Each chunk scores `1 / (RRF_K + rank)` in each list it is in, where `rank` is its place in that list counting from 1
and `RRF_K` is 60, and its scores from the lists add up.

`Chunk` is given at the top of `solution.py`. A `Chunk` cannot be a dict key (a dataclass that compares by value is
not hashable), so name each chunk by the tuple `(chunk.file, chunk.seq)`, which no two chunks share. Write:

- `rrf_scores(rankings)`, where `rankings` is a list of ranked lists of chunks (best first). It returns a dict from
  each chunk's `(file, seq)` to its fused score. A chunk in no list is not in the dict.
- `fuse(rankings, limit)` returns the chunks with the highest fused scores, best first, at most `limit` of them, each
  chunk once. Chunks with the same score stay in the order they were first met, reading the first list from its
  top, then the second, and so on.

Any number of lists works, also one, and none (`{}` and `[]`).

```python
a, b, c = Chunk("f.txt", 1, 0, "a"), Chunk("f.txt", 1, 1, "b"), Chunk("f.txt", 1, 2, "c")
rrf_scores([[a, b], [c, b]])
# {("f.txt", 0): 1/61, ("f.txt", 1): 1/62 + 1/62, ("f.txt", 2): 1/61}
fuse([[a, b], [c, b]], 2)     # [b, a]: b is second in both lists, and 2/62 beats 1/61
```

You will use: a dict with tuple keys, `dict.get` with a default, `enumerate` with a start value, `sorted` with a
`key` and `reverse=True` (Python's sort keeps equal items in their order).
