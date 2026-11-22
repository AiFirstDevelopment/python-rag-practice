# 26. A system prompt and a list of messages

> **Your lesson:** [lessons/26-messages.md](../../lessons/26-messages.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

A model keeps nothing between calls. A chatbot that follows a conversation sends the whole conversation every
time, as a list of messages that alternate between `user` and `assistant`. The standing instructions ("answer only
from the passages") are not a message: they go in the separate `system` argument.

Write two functions in `solution.py`:

- `build_messages(history, question)`: `history` is a list of `(question, answer)` tuples, oldest first. Return a
  new list of dicts: for each pair `{"role": "user", "content": question}` then
  `{"role": "assistant", "content": answer}`, and last the new question as a `user` message. `history` is not
  changed.
- `chat(client, system, history, question, model=MODEL, max_tokens=1024)` calls
  `client.messages.create(...)` once with the keyword arguments `model`, `max_tokens`, `system` (the string given)
  and `messages` (from `build_messages`), and returns the reply's text, `response.content[0].text`. No message has
  the role `system`. If `question` is empty or only whitespace, raise `ValueError` without calling the client.

```python
build_messages([("Can I return shoes?", "Yes, within 30 days.")], "And sale items?")
# [{"role": "user", "content": "Can I return shoes?"},
#  {"role": "assistant", "content": "Yes, within 30 days."},
#  {"role": "user", "content": "And sale items?"}]

chat(client, "Answer in one sentence.", [], "Can I return shoes?")   # "Yes, within 30 days."
```

You will use: a loop over tuples (`for asked, answered in history`), `list.append`, `str.strip`, keyword arguments.
