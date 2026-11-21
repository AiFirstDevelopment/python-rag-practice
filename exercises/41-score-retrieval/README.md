# 41. Score retrieval

When an answer is wrong, the first question is whether the pipeline even found the right text. The harness answers
that without a model call: each golden case names the file and page its answer comes from, and the harness checks
that the passages the pipeline retrieved cover them. It is free, so it runs on every change.

The starter gives you the golden set's models and `Passage`, what the pipeline retrieves after widening: a `file`,
the `first_page` and `last_page` its text spans, and the `text`.

Write in `solution.py`:

- `source_found(source, passages)`: `True` when at least one passage is from the source's file and the source's page
  is within that passage's pages (`first_page` and `last_page` included). The same page number in another file does
  not count.
- `recall(case, passages)`: the fraction of the case's sources that were found, a float from 0.0 to 1.0. A case with
  no sources (a fallback case) has nothing to find: return `None`.
- `mean_recall(recalls)`: the average of the recalls that are not `None`. If there are none to average, 0.0.

```python
passages = [Passage("shipping.pdf", 1, 2, "..."), Passage("returns.txt", 1, 1, "...")]
source_found(Source(file="shipping.pdf", page=2), passages)   # True
source_found(Source(file="warranty.txt", page=1), passages)   # False
recall(case_with_those_two_sources, passages)                 # 0.5
recall(fallback_case, passages)                               # None
mean_recall([1.0, 0.5, None])                                 # 0.75
```

You will use: `any`, `sum` over a generator, chained comparison (`a <= b <= c`), `is None`.
