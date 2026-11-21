# 33. Vector search

Keyword search misses a chunk that says the same thing in other words. Vector search finds it: an embedding model
turns each text into a vector, texts with a similar meaning get vectors pointing the same way, and the search is the
cosine similarity from module 5, run over every chunk at once. It is the pipeline's second search.

The embedding model is not yours to write. Each function that needs one takes `embed`, a function from a text to a
1-D NumPy array (the same length for every text). The tests pass a small fake that counts a few known words, so
nothing is downloaded; the course uses a real model the same way.

`Chunk` is given at the top of `solution.py`. Write three functions:

- `embed_chunks(chunks, embed)` returns a 2-D array with one row per chunk, in order: row `i` is `embed` of chunk
  `i`'s text. A pipeline does this once, when it starts, not for every question.
- `nearest(vectors, query, limit)` returns the indexes of the rows of `vectors` most like `query`, by cosine
  similarity, best first, at most `limit` of them, as a list of plain Python `int`s (not NumPy integers). The rows
  are not normalized: a long vector must not win for being long.
- `vector_search(chunks, vectors, question, embed, limit)` embeds the question and returns the `limit` chunks
  nearest to it, best first, where `vectors` is what `embed_chunks` returned for these chunks. It returns the
  `Chunk` objects themselves. With no chunks it returns `[]` without calling `embed`.

A `limit` larger than the number of chunks gives all of them.

```python
vectors = np.array([[1.0, 0.0], [0.0, 1.0], [0.7, 0.7]])
nearest(vectors, np.array([1.0, 0.1]), 2)       # [0, 2]
```

You will use: `np.array`, `@` for a matrix times a vector, `np.linalg.norm` with `axis=1`, `np.argsort`, slicing
with a step of -1, `int()`.
