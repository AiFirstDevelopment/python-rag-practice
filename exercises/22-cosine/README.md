# 22. Dot product and cosine similarity

> **Your lesson:** [lessons/22-cosine.md](../../lessons/22-cosine.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

Vector search ranks chunks by how close each chunk's embedding is to the question's. "Close" is cosine similarity:
1 when two vectors point the same way, 0 when they have nothing in common, -1 when they point opposite ways. It
looks at direction only, so a long chunk and a short one about the same thing still score high.

Write two functions in `solution.py`:

- `dot(a, b)` returns the dot product of two one-dimensional arrays (each pair of numbers multiplied, the products
  added up) as a Python `float`.
- `cosine(a, b)` returns the dot product divided by the two lengths multiplied together, as a Python `float`. If
  either vector is all zeros, return `0.0` (no division by zero, no `nan`).

Both raise `ValueError` when the two arrays do not have the same shape.

```python
a, b = np.array([1.0, 2.0, 3.0]), np.array([4.0, 5.0, 6.0])
dot(a, b)                                          # 32.0
cosine(np.array([1.0, 0.0]), np.array([5.0, 0.0])) # 1.0   same direction, different length
cosine(np.array([1.0, 0.0]), np.array([0.0, 2.0])) # 0.0
cosine(np.array([1.0, 0.0]), np.zeros(2))          # 0.0
```

You will use: `a @ b` (or `np.dot`), `np.linalg.norm`, `.shape`, `raise ValueError(...)`, `float(...)`.
