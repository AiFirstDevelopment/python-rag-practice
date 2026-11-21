# 07. Putting it together: the words that matter

Keyword search weighs rare words above common ones. The first step is knowing which words a document uses most,
leaving out words like "the" that say nothing.

Write `top_words(text, n, stopwords)` in `solution.py`: the `n` most frequent words of `text` that are not in
`stopwords`, as a list of `(word, count)` tuples, most frequent first; words with the same count in alphabetical
order. Words are found as in exercise 04 (lowercased runs of letters, digits and apostrophes); `stopwords` may be in
any case.

```python
top_words("The refund is a refund. The receipt is the proof.", 2, {"the", "is", "a"})
# [("refund", 2), ("proof", 1)]
```

Write the word splitting again here (copy your own from 04 if you like); this file stands alone.

You will use: everything so far, plus `sorted` with a `key`, or `collections.Counter`.
