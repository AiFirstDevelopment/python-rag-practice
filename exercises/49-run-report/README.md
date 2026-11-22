# 49. A run report

> **Your lesson:** [lessons/49-run-report.md](../../lessons/49-run-report.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

An eval run leaves one line of JSON per case: did it pass, how long it took, how many tokens it used. Nobody reads
fifty lines. What gets read is the summary: the pass rate, where the failures are, which cases are slow, what the
run cost. The course explores a run in a notebook; here you write the same summary as functions, so it can be
tested and pasted into a pull request.

A results file is JSONL, one case per line:

```
{"id": "returns-01", "category": "answerable", "status": "pass", "seconds": 1.8, "input_tokens": 1200, "output_tokens": 80}
```

`status` is `"pass"`, `"fail"` or `"review"` (a person must read it). Only `"pass"` counts as passed.

Write three functions in `solution.py`:

- `load_results(path)` reads the file at `path` (a `pathlib.Path`) and returns a list of dicts, one per line, in
  file order. Blank lines are skipped.
- `summarize(results, input_price, output_price, slowest=3)` returns a dict with exactly these keys:
  - `"cases"`: the number of results.
  - `"passed"`: how many have the status `"pass"`.
  - `"pass_rate"`: passed divided by cases, a float from 0 to 1; `0.0` when there are no cases.
  - `"by_category"`: a dict from each category to `{"cases": ..., "passed": ..., "pass_rate": ...}` for the results
    in that category.
  - `"slowest"`: the ids of the `slowest` cases with the most seconds, slowest first (all of them if there are
    fewer).
  - `"cost"`: the dollars for all the tokens of the run. The prices are dollars per million tokens, as in
    exercise 25.
- `to_markdown(summary)` returns the summary as a Markdown table, a string of lines joined with `"\n"`: the header
  and separator below, one row per category in alphabetical order, and a last row `all`. Pass rates are whole
  percents (`f"{rate:.0%}"`).

For a `run.jsonl` holding the first four results in `test_run_report.py` (`returns-01` to `returns-03` and
`absent-01`):

```python
results = load_results(Path("run.jsonl"))
summary = summarize(results, 5.0, 25.0, slowest=2)
# {"cases": 4, "passed": 3, "pass_rate": 0.75,
#  "by_category": {"answerable": {"cases": 3, "passed": 2, "pass_rate": 0.666...},
#                  "absent": {"cases": 1, "passed": 1, "pass_rate": 1.0}},
#  "slowest": ["returns-03", "returns-01"], "cost": 0.02875}
print(to_markdown(summary))
```

```
| category | cases | passed | pass rate |
| --- | --- | --- | --- |
| absent | 1 | 1 | 100% |
| answerable | 3 | 2 | 67% |
| all | 4 | 3 | 75% |
```

You will use: `Path.read_text`, `str.splitlines`, `json.loads`, a dict built in a loop (or `collections.defaultdict`),
`sum` with a generator, `sorted` with `key` and `reverse=True`, f-strings with a format, `"\n".join`.
