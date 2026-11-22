# 20. Faking a dependency

> **Your lesson:** [lessons/20-faking.md](../../lessons/20-faking.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

The last step of a pipeline calls a model: a network call that costs money, takes seconds and answers differently
each time. None of that belongs in a test. What a test can check exactly is your side of the call: what the code
sent, and what it did with the reply. So the code takes its client as a parameter, and a test hands it a fake: a
small object of your own with the same methods, which records what it was sent and returns a reply you chose.

As in exercises 17 to 19, the code is given and you write its tests in `solution.py`.

## The code under test

A module `asking` with one function, `ask(client, question, passages)`, and three constants, `DEFAULT_MODEL`,
`SYSTEM` and `FALLBACK`. `passages` is a list of strings.

- When `passages` is empty it does not call the model at all and returns
  `{"answer": FALLBACK, "input_tokens": 0, "output_tokens": 0}`.
- Otherwise it calls `client.messages.create(...)` exactly once, with four keyword arguments:
  - `model`: the value of the environment variable `PRACTICE_MODEL`, read at the time of the call, or
    `DEFAULT_MODEL` when the variable is not set;
  - `max_tokens`: a whole number;
  - `system`: `SYSTEM`;
  - `messages`: a list with one dict, `{"role": "user", "content": ...}`, whose content is one string that
    contains every passage and the question.
- The reply is an object, as the Anthropic SDK returns it: the text is `reply.content[0].text`, and the token counts
  are `reply.usage.input_tokens` and `reply.usage.output_tokens`.
- It returns `{"answer": ..., "input_tokens": ..., "output_tokens": ...}`: the reply's text with whitespace
  removed from both ends, and the two counts.

## What to write

In `solution.py`, replace the placeholder with tests for `ask`, and the fake client they use. The fake needs a
`messages` attribute with a `create` method that keeps the keyword arguments it was called with (and how many times
it was called) and returns a reply of the shape above. A class is how you make such an object: `__init__` runs when one is made and sets its attributes on `self`, and
each method takes `self` first. `**request` in a parameter list collects every keyword argument into one dict:

```python
class Recorder:
    def __init__(self):
        self.calls = []                  # starts empty for each Recorder made

    def send(self, **request):
        self.calls.append(request)       # send(to="a", body="hi") stores {"to": "a", "body": "hi"}
        return "sent"


recorder = Recorder()
recorder.send(to="a", body="hi")
recorder.calls                           # [{"to": "a", "body": "hi"}]
```

An attribute can hold any object, including the object itself (`self.messages = self`) or another one you made.
`types.SimpleNamespace` makes an object with whatever attributes you give it, which is enough for the reply:

```python
from types import SimpleNamespace

point = SimpleNamespace(x=1, inner=SimpleNamespace(y=2))
point.inner.y       # 2
```

For the environment variable, use the `monkeypatch` fixture, which undoes its changes when the test ends:
`monkeypatch.setenv("PRACTICE_MODEL", "some-model")` and `monkeypatch.delenv("PRACTICE_MODEL", raising=False)`. A
test of the default model should unset the variable first, so that it passes on a machine where it happens to be
set.

Keep the imports at the top of the starter as they are. No test may use a real client or the network.

## How it is graded

The same way as exercise 17. `implementations/` holds a correct `asking.py` and five with one bug each; `/check`
runs your tests against each. They must all pass against `correct` and at least one must fail against each of the
others. It also checks that at least one test asks for `monkeypatch`.

To run your tests yourself against the correct version, from the repository root:

```bash
PYTHONPATH=exercises/20-faking/implementations/correct uv run pytest exercises/20-faking/solution.py
```

You will use: a class with `__init__` and a method that takes `**request`, `SimpleNamespace`, `monkeypatch.setenv`
and `monkeypatch.delenv`, `in` on strings.
