# 38. "I don't know" when nothing fits

> **Your lesson:** [lessons/38-i-dont-know.md](../../lessons/38-i-dont-know.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

A model asked a question its passages do not answer will often answer anyway, from what it learned in training, and
sound just as sure. A RAG pipeline must do the opposite: say it does not know. The course does this with the system
prompt ("If the answer is not in them, say you don't know."), and the eval harness later checks that the pipeline
really fell back on questions the documents cannot answer. This exercise adds the two cases where there is nothing
to read from the model, and the check the harness uses.

`Passage`, `SYSTEM`, `build_request` (exercise 37) and three constants are given at the top of `solution.py`:
`DONT_KNOW` is `"I don't know."`, `DECLINED` is `"The model declined."`, and `FALLBACK` is the phrases a reply uses
when it falls back.

Write two functions.

`answer(client, question, passages)`, async, returns the reply to show:

- With no passages it returns `DONT_KNOW` and does not call the model: there is nothing to answer from, and a call
  costs money.
- Otherwise it calls `await client.messages.create(...)` once with `build_request(question, passages)`.
- If the response's `stop_reason` is `"refusal"`, the model declined to answer and its content may be empty: return
  `DECLINED` without reading the content.
- Otherwise return the reply's text, `response.content[0].text`.

`is_fallback(reply)` returns `True` when the reply says the pipeline does not know: when any phrase of `FALLBACK` is
in the reply, in any case ("I DON'T KNOW" counts), anywhere in it. Otherwise `False`. It only looks for the phrases;
it does not judge the answer.

```python
is_fallback("I don't know.")                                        # True
is_fallback("The policy does not say when the store opens.")       # True
is_fallback("Sale items can be returned within 14 days.")          # False
```

You will use: `if not passages`, `async def` and `await`, `**` to pass a dict as keyword arguments, `str.lower`,
`in` on strings, `any` with a generator expression.
