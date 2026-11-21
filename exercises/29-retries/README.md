# 29. Retries with backoff

A provider under load answers some calls with "too many requests" or "overloaded". The call was fine; the moment
was not. A harness running fifty cases must wait and try again, waiting longer each time (1 s, 2 s, 4 s: exponential
backoff), and give up after a few tries rather than loop forever. Any other error (a bad request, a bug) is not
retried: trying again would fail the same way.

`RateLimited`, the error to retry, is given at the top of `solution.py`. Write two functions:

- `backoff(attempt, base=1.0, cap=30.0)` returns the seconds to wait after failed attempt number `attempt`, counted
  from 0: `base` doubled `attempt` times, and never more than `cap`.
- `async def with_retries(call, retries=3, sleep=asyncio.sleep, base=1.0, cap=30.0)`: `call` is a function taking no
  arguments that returns something to await (`await call()`). Await it and return its result. If it raises
  `RateLimited`, `await sleep(backoff(attempt, base, cap))` and call it again, at most `retries` more times
  (`retries=3` means up to 4 calls and 3 sleeps). When the last allowed call also raises `RateLimited`, let that
  error out, without sleeping after it. Any other exception goes straight out: no sleep, no second call.

```python
backoff(0)      # 1.0
backoff(3)      # 8.0
backoff(10)     # 30.0   capped

text = await with_retries(lambda: ask(client, "Can I return shoes?"))
# RateLimited twice, then a reply: three calls, sleeps of 1.0 and 2.0 seconds
```

`sleep` is a parameter so the tests can pass one that records the seconds and returns at once: they check the waits
without waiting. In your own code the default, `asyncio.sleep`, really waits.

The real SDK retries rate limits by itself (its `max_retries` setting) and adds a random part to each wait so that
many clients do not all come back at the same instant. This exercise leaves the random part out so the waits can be
checked.

You will use: `min`, `**`, a `for` loop over `range`, `try` / `except RateLimited`, `raise` on its own to re-raise,
`await`.
