# 32. BM25 keyword search

Keyword search finds the chunks that share words with the question. BM25 is the standard way to score them: a word
found in few chunks counts for more than one found in most, a word repeated in a chunk counts for more but less
each time, and a long chunk does not win just by holding more words. It is one of the two searches the pipeline runs.

`Chunk` and `words(text)` are given at the top of `solution.py`. `words` turns a text into its search words:
lower-cased runs of letters and digits, without stop words such as "the", and with a plain plural's "s" taken off,
so "Returns" and "return" are the same word. Use it for the chunks and for the question.

Write `bm25(chunks, question, limit)`: the chunks that share at least one word with the question, best score first,
at most `limit` of them.

A chunk's score is the sum, over each distinct word `w` of the question that the chunk holds, of

```
idf(w) * tf * (k1 + 1) / (tf + k1 * (1 - b + b * length / average))

idf(w) = ln(1 + (N - n + 0.5) / (n + 0.5))
```

with `k1 = 1.2` and `b = 0.75`, and where

- `tf` is how many times `w` is in the chunk's words,
- `length` is how many words the chunk has, and `average` is the mean `length` over all the chunks,
- `N` is the number of chunks and `n` is the number of chunks that hold `w`,
- `ln` is the natural logarithm, `math.log`.

Details the tests check:

- A word that is in the question twice counts once.
- A chunk with no word of the question has no score and is not in the result, so the result can be shorter than
  `limit`, or empty.
- No chunks gives `[]`.
- The result holds the `Chunk` objects themselves, not copies or texts.

```python
chunks = [Chunk("f.txt", 1, 0, "shipping is free"),
          Chunk("f.txt", 1, 1, "refund refund policy"),
          Chunk("f.txt", 1, 2, "refund window policy")]
bm25(chunks, "refund", 5)     # [chunks[1], chunks[2]]: "refund" twice beats once; chunks[0] has no match
```

You will use: `collections.Counter`, `math.log`, `set`, `zip`, `sorted` or `list.sort` with a `key`, slicing.
