# 36. Widening a chunk with its neighbours

A chunk is cut at a sentence end, so a rule and its exception often land in two chunks: "Returns are accepted within
30 days." in one, "Sale items are the exception." in the next. Search finds the first, and the model would answer
without the second. Widening joins each chosen chunk with the chunk before and after it in the same file, up to a
budget of characters so the prompt does not grow without limit.

`Chunk`, `Passage` and `WIDEN_CHARS` (10,800) are given at the top of `solution.py`. A `Passage` is what the model
will read: a run of neighbouring chunks of one file, with the first and last page it covers. A chunk is named by its
`file` and `seq` together; its neighbours are the chunks with the same `file` and `seq - 1` and `seq + 1`.

Write `widen(given, everything, budget=WIDEN_CHARS)`, where `given` is the chosen chunks, best first, and
`everything` is every chunk of every file. It works in two steps.

Step 1, take neighbours. Go through `given` in order, and for each chunk look at the chunk before it, then the chunk
after it. Take the neighbour unless:

- there is no such chunk (the start or end of the file; another file's chunk is never a neighbour);
- it is one of the `given` chunks, or was already taken;
- its text would bring the total length of the neighbours taken so far over `budget`. Only neighbours count toward
  the budget, never the given chunks. A neighbour that does not fit is skipped, and the walk goes on: a later,
  smaller one may still fit.

Because `given` is best first, the best chunks get their neighbours first.

Step 2, build passages. Go through `given` in order again. Skip a chunk that is already inside an earlier passage.
Otherwise its passage is the longest unbroken run of `seq` numbers around it, in its file, in which every chunk is a
given one or a taken neighbour. The passage has the file, the `page` of the run's first chunk as `first_page`, the
`page` of its last chunk as `last_page`, and the chunks' texts joined with `"\n"`.

So two given chunks side by side, or sharing a neighbour, come out as one passage, not two that repeat each other,
and the passages are in the order of `given`. No given chunks gives `[]`.

```python
chunks = [Chunk("f.txt", 1, i, f"part {i}.") for i in range(5)]
widen([chunks[2]], chunks)
# [Passage(file="f.txt", first_page=1, last_page=1, text="part 1.\npart 2.\npart 3.")]
widen([chunks[1], chunks[2]], chunks)
# one passage: "part 0.\npart 1.\npart 2.\npart 3."
```

You will use: a dict with tuple keys and `dict.get`, a set of `(file, seq)` tuples, `while` loops, `range`,
`str.join`.
