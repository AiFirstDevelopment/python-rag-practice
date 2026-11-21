# 44. Run cases concurrently

Each case waits a few seconds on the model. Run one after another, fifty cases take minutes; run all at once, the
API answers with rate-limit errors. The harness runs them concurrently, a fixed number at a time.

The starter gives you the models, `score_answer` from exercise 43 and the `Result` dataclass. The pipeline is handed
to you as a function, so the tests can pass a fake: `await pipeline(question)` returns the reply as a string.

Write `async def run_cases(cases, pipeline, limit=4)` in `solution.py`. It returns one `Result` per case:

- The results are in the order of `cases`, whichever case finished first.
- The pipeline is called once per case, with the case's `question`.
- Never more than `limit` calls are in flight at once, and they do run concurrently: with more cases than `limit`,
  exactly `limit` are in flight at the busiest moment. With `limit=1` they run one at a time.
- For a reply, the result's `status` and `missing` come from `score_answer(case, reply)`, and `error` is `None`.
- If the pipeline raises an exception for a case, that case's result has status `"fail"`, `missing` empty and
  `error` set to the exception's message (`str(exception)`). The other cases still run and are scored.
- No cases: an empty list.

```python
async def pipeline(question: str) -> str:
    return "Within 30 days."

results = asyncio.run(run_cases(cases, pipeline, limit=2))
results[0]   # Result(id="returns-01", status="pass", missing=[], error=None)
```

You will use: `async def`, `await`, `asyncio.Semaphore` with `async with`, `asyncio.gather`, `try` / `except
Exception`.
