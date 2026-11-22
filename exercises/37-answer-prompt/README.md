# 37. A prompt that answers from passages only

> **Your lesson:** [lessons/37-answer-prompt.md](../../lessons/37-answer-prompt.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

Everything so far chooses what the model reads. This is the step that makes it a RAG pipeline: the model is told to
answer from the passages and nothing else, and each passage is labelled with its file and page so an answer can be
traced to where it came from.

`Passage`, `MODEL` and the system prompt `SYSTEM` are given at the top of `solution.py`. Write three functions.

`format_passages(passages)` returns the passages as one string. Each passage is a label line, then its text. The
label is the passage's number in square brackets (counting from 1), the file, and the page: `page 2` when the passage
is on one page, `pages 2-3` when `first_page` and `last_page` differ. Passages are separated by one blank line. No
passages gives `""`.

```
[1] returns.txt, page 1
Sale items can be returned for store credit.

[2] gear-care.pdf, pages 2-3
Wash the tent by hand.
Dry it before storing it.
```

`build_request(question, passages)` returns the keyword arguments of the model call as a dict with exactly these
keys:

- `"model"`: `MODEL`
- `"max_tokens"`: `1024`
- `"system"`: `SYSTEM`
- `"messages"`: a list with one user message, whose content is `Passages:`, a blank line, the formatted passages, a
  blank line, and `Question: ` followed by the question:

```
Passages:

[1] returns.txt, page 1
Sale items can be returned for store credit.

Question: Can I return a sale item?
```

`answer(client, question, passages)` is async. It calls `await client.messages.create(...)` once with that request
and returns the reply's text, `response.content[0].text`.

The passages come before the question because a model answers better when the long material is first and the
question last.

You will use: `enumerate` with a start value, f-strings, a conditional expression, `str.join`, a dict passed as
keyword arguments with `**`, `async def` and `await`.
