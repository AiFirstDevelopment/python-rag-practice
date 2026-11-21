# 24. A matrix of embeddings, searched at once

Calling `cosine` once per chunk in a Python loop is fine for ten chunks and slow for a hundred thousand. The
pipeline keeps every chunk's embedding as one row of a matrix, makes every row length 1 once, and then a search is
a single matrix-vector product: one line, all the scores.

Why it works: cosine similarity is the dot product divided by the two lengths. If both vectors already have length
1, the dot product is the cosine. `matrix @ query` computes the dot product of every row with the query.

In a real pipeline the embeddings come from a model. Here `fake_embed(text)`, given at the top of `solution.py`,
stands in: it counts each word into one of 64 slots, so texts that share words get similar vectors. Your functions
take the embed function as a parameter; the tests pass their own.

Write three functions:

- `normalize_rows(matrix)` returns a new two-dimensional array where every row has length 1. A row of all zeros
  stays zeros (no `nan`). The array given is not changed.
- `build_index(texts, embed)` embeds each text with `embed(text)` and returns the normalized matrix, one row per
  text, in order: shape `(len(texts), d)`.
- `search(index, query, k)`: `index` is a matrix from `build_index`, `query` is a one-dimensional vector of any
  length (normalize it here). Return the `k` best rows as a list of `(position, score)` tuples, a Python `int` and
  `float`, best first; equal scores in position order; all the rows if `k` is larger than their number. Compute the
  scores with one matrix-vector product, no Python loop over the rows.

```python
texts = ["returns are accepted within 30 days", "shipping takes five days", "gift cards never expire"]
index = build_index(texts, fake_embed)        # shape (3, 64)
search(index, fake_embed("how long does shipping take"), 1)   # [(1, 0.2236...)]
```

You will use: `np.array` over a list of vectors, `np.linalg.norm(matrix, axis=1, keepdims=True)`, division of a
matrix by a column, `np.where` (or a small fix for the zero rows), `matrix @ vector`, `np.argsort`.
