# 45. Compare two runs

You change the chunk size and the pass count goes from 15 to 16. Better? A model does not give the same answer
twice, so one case can flip between two runs of the same code. The harness needs a rule that says when a difference
is a real change and when it is noise, and the rule has to be simple enough to argue with.

A run is a dict from case id to status: `{"returns-01": "pass", "returns-02": "fail", "absent-01": "review"}`.

The rule here: count the flips. A case is **gained** when it did not pass before and passes now, and **lost** when it
passed before and does not now. Only `"pass"` counts as passing: `"fail"` and `"review"` are both not passing, so a
move between those two is no flip. The net is gained minus lost, and a net smaller than the threshold in either
direction is noise.

Write in `solution.py` (the `Comparison` dataclass is given):

- `compare(before, after)`: a `Comparison` with `gained` and `lost` as lists of case ids in alphabetical order, and
  `net` as `len(gained) - len(lost)`. Only ids in both runs are compared; an id in only one of them is ignored.
- `verdict(comparison, threshold=2)`: `"gain"` when `net` is at least `threshold`, `"drop"` when `net` is at most
  minus `threshold`, otherwise `"noise"`. Three gained and three lost is a net of 0: noise.

```python
before = {"a": "pass", "b": "fail", "c": "fail", "d": "pass"}
after  = {"a": "pass", "b": "pass", "c": "pass", "d": "review"}
c = compare(before, after)         # Comparison(gained=["b", "c"], lost=["d"], net=1)
verdict(c)                         # "noise"
verdict(c, threshold=1)            # "gain"
```

You will use: iterating a dict, `in` on a dict, `sorted`, a dataclass, `if` / `elif` / `else`.
