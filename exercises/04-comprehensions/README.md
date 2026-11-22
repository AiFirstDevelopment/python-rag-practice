# 04. Loops and comprehensions

> **Your lesson:** [lessons/04-comprehensions.md](../../lessons/04-comprehensions.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

Keyword search starts by turning text into words. Write it with list and dict comprehensions where they fit.

Write two functions in `solution.py`:

- `words(text)`: the words of `text`, lowercased, in order. A word is a run of letters, digits or apostrophes; every
  other character separates words.
- `keyword_hits(text, keywords)`: a dict from each keyword (as given) to how many times it appears in `words(text)`,
  ignoring case. Keywords that never appear map to `0`.

```python
words("Refunds: 30 days, no receipt? Don't worry.")
# ["refunds", "30", "days", "no", "receipt", "don't", "worry"]
keyword_hits("Refund or refund? REFUND!", ["refund", "Receipt"])
# {"refund": 3, "Receipt": 0}
```

You will use: a loop over characters (or the `re` module), list and dict comprehensions, `str.lower`.
