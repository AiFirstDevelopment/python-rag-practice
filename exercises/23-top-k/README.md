# 23. Top k by similarity

A search does not return every chunk, it returns the best few: the top k. Given one score per chunk, the pipeline
needs the positions of the k highest, best first, because a position is what leads back to the chunk's text.

`cosine(a, b)` from exercise 22 is given at the top of `solution.py`. Write two functions:

- `top_k(scores, k)`: `scores` is a one-dimensional array. Return the positions of the `k` highest scores as a list
  of Python `int`s, highest score first. When two scores are equal, the lower position comes first. If `k` is larger
  than the number of scores, return all the positions; if `k` is 0 or less, return `[]`.
- `most_similar(query, vectors, k)`: `vectors` is a list of arrays. Return the `k` vectors most similar to `query` by
  cosine similarity as a list of `(position, score)` tuples, best first, with the same rules as `top_k`; each score a
  Python `float`.

```python
top_k(np.array([0.1, 0.9, 0.4, 0.9]), 3)   # [1, 3, 2]   the two 0.9s in position order
most_similar(np.array([1.0, 0.0]), [np.array([0.0, 1.0]), np.array([2.0, 0.0]), np.array([1.0, 1.0])], 2)
# [(1, 1.0), (2, 0.7071...)]
```

`np.argsort(scores)` returns the positions that would sort the array, lowest first. Sorting the negated scores with
`kind="stable"` gives highest first and keeps equal scores in position order; reversing an ascending sort with
`[::-1]` does not (it reverses the ties too). `np.argpartition` finds the top k without sorting everything, which
matters at a million chunks; it leaves them unordered, so you would still sort those k and settle the ties
yourself. Either passes.

You will use: `np.argsort`, slicing, `int(...)`, a list comprehension, tuples.
