# 06. Exceptions

A reranker asks a model to score each passage from 0 to 1 and gets text back. Sometimes the text is not a number.
The pipeline must notice, not crash and not guess.

Write two functions in `solution.py`:

- `parse_score(text)`: the number in `text` (spaces around it allowed) as a float. Raise `ValueError` if it is not a
  number or is outside 0 to 1, with a message that contains the text you were given.
- `parse_all(texts)`: returns a tuple `(scores, errors)`: the scores that parsed, in order, and for each text that
  did not, its position in the list.

```python
parse_score(" 0.8 ")                  # 0.8
parse_score("high")                   # ValueError: not a score: 'high'
parse_all(["0.9", "high", "1.5", "0"])  # ([0.9, 0.0], [1, 2])
```

Catch only `ValueError`, never everything.

You will use: `float()`, `raise`, `try` / `except ValueError`, `enumerate`, tuples.
