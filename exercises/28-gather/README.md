# 28. Async and gather

> **Your lesson:** [lessons/28-gather.md](../../lessons/28-gather.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

A model call is mostly waiting: a second or more for the reply to come back. An eval run of fifty cases one after
another waits fifty times; with `async` the fifty calls wait at the same time and the run takes about as long as the
slowest. A provider also limits how many calls you may have open at once, so the pipeline caps it.

The async client, `AsyncAnthropic`, has the same call as before, awaited:
`response = await client.messages.create(...)`.

Write two functions in `solution.py`:

- `async def ask(client, question, model=MODEL, max_tokens=1024)` awaits one call (keyword arguments `model`,
  `max_tokens`, and `messages` holding the question as one `user` message) and returns `response.content[0].text`.
- `async def ask_all(client, questions, limit=5)` asks every question and returns the answers as a list in the
  order of the questions, whichever call finished first. The calls run at the same time, but never more than
  `limit` of them are in flight at once. Each question is asked once. No questions: `[]`, no call.

```python
answers = asyncio.run(ask_all(client, ["Can I return shoes?", "How long is shipping?"], limit=5))
# ["Yes, within 30 days.", "Five days."]
```

`asyncio.gather(*coroutines)` runs them together and returns their results in the order they were given. An
`asyncio.Semaphore(limit)` lets `limit` holders in at a time: `async with semaphore:` around the call waits for a
free place. Make the semaphore inside `ask_all`, not at the top of the file.

You will use: `async def`, `await`, `asyncio.gather`, `asyncio.Semaphore`, `async with`, a small `async def` inside
`ask_all`.
