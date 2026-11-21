# 21. NumPy arrays

An embedding model turns a piece of text into a list of a few hundred numbers, a vector. A pipeline keeps thousands
of them and does arithmetic on all of them at once, which plain Python lists are too slow for. NumPy's array is the
type every later exercise in this module works on.

Write five functions in `solution.py`:

- `to_vector(values)` returns a one-dimensional array of floats (`dtype` `float64`) holding `values`, also when the
  values given are whole numbers.
- `length(v)` returns the vector's length (the square root of the sum of its squares) as a Python `float`.
- `normalize(v)` returns a new array pointing the same way with length 1. A vector of all zeros has no direction: return
  zeros, never `nan`. The array given is not changed.
- `stack(rows)` returns a two-dimensional array with one row per list: `n` lists of `d` numbers give the shape
  `(n, d)`. Raise `ValueError` if the lists are not all the same length.
- `mean_vector(matrix)` returns the average row of a two-dimensional array: a one-dimensional array of `d` numbers,
  the mean of each column.

```python
to_vector([3, 4])                    # array([3., 4.])
length(to_vector([3, 4]))            # 5.0
normalize(to_vector([3, 4]))         # array([0.6, 0.8])
stack([[1, 2, 3], [4, 5, 6]]).shape  # (2, 3)
mean_vector(stack([[1, 2], [3, 6]])) # array([2., 4.])
```

Compare arrays of floats with `np.allclose(a, b)`, not `==`: `==` on arrays gives an array of booleans, and floats
are rarely exactly equal.

You will use: `np.array(..., dtype=float)`, `.shape`, `.ndim`, `np.linalg.norm` (or `np.sqrt` and `np.sum`),
arithmetic on a whole array (`v / 2`), `.mean(axis=0)`, `float(...)`.
