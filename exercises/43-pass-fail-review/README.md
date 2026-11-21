# 43. Pass, fail and review

Each case ends as one of three words. `pass` and `fail` are decided by code. `review` means code cannot tell and a
person must read the answer: the pipeline answered a question it was expected to decline, and only a reader can say
whether it made something up or the documents hold the answer after all.

The starter gives you the models, `FALLBACK` (the phrases that mean "I don't know") and `missing_facts` from
exercise 42.

Write in `solution.py`:

- `fell_back(reply)`: `True` when the reply contains any of the `FALLBACK` phrases, whatever the case of the reply.
- `score_answer(case, reply)`: returns a tuple `(status, missing)`.
  - A case whose `expected_behavior` is `"fallback"`: `("pass", [])` when the reply fell back, `("review", [])` when
    it did not.
  - A case whose `expected_behavior` is `"answer"`: `missing` is the list from `missing_facts`; the status is
    `"fail"` when something is missing, `"pass"` when nothing is.
  - Falling back is not checked on an answer case. A right answer with a caveat ("14 days. I don't know about
    opened items.") passes, and a reply of only "I don't know" fails because its facts are missing.
- `tally(statuses)`: how many of each, as a dict that always has the three keys `"pass"`, `"fail"` and `"review"`,
  zero included.

```python
score_answer(answer_case, "Within 14 days, as store credit.")   # ("pass", [])
score_answer(answer_case, "As store credit.")                    # ("fail", ["within 14 days"])
score_answer(fallback_case, "I don't know.")                     # ("pass", [])
score_answer(fallback_case, "We open at nine.")                  # ("review", [])
tally(["pass", "review", "pass"])                                # {"pass": 2, "fail": 0, "review": 1}
```

You will use: `any`, a conditional expression (`a if condition else b`), returning a tuple, `list.count` or a dict
you fill in a loop.
