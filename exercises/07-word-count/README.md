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

`sorted(items, key=f)` sorts by what the function `f` returns for each item. `lambda x: ...` writes a one-line
function in place. A tuple as the key sorts by its first part, then by the second when the first is equal; and
negating a number turns largest-first into smallest-first:

```python
people = [("ana", 31), ("bo", 25), ("cy", 31)]
sorted(people, key=lambda person: person[1])                  # by age: bo, then ana and cy
sorted(people, key=lambda person: (-person[1], person[0]))    # oldest first, names A-Z among equals: ana, cy, bo
```

`collections.Counter(words)` counts a list for you, and `.items()` gives its `(word, count)` pairs.
`Counter.most_common(n)` does not put equal counts in alphabetical order, so the sort is still yours.

You will use: everything so far, plus `sorted` with a `key` and a `lambda`, and `collections.Counter` if you like.
