# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
# Your tests and your fake client go in this file. Keep these imports: the grader decides which implementation of
# asking it finds.
from types import SimpleNamespace

import pytest

from asking import DEFAULT_MODEL, FALLBACK, SYSTEM, ask


# Your tests and fake client: replace this placeholder with tests for ask(client, question, passages) and the fake
# client they use. The fake has a messages attribute with a create method that keeps the keyword arguments it was
# called with (and how many times it was called) and returns a reply shaped like the SDK's: reply.content[0].text,
# reply.usage.input_tokens, reply.usage.output_tokens. No real client, no network. At least one test must ask for
# monkeypatch. Against the correct asking every test must pass; against each of the five broken versions at least one
# must fail. Behaviors to cover:
#   With passages empty, it does not call the model and returns
#     {"answer": FALLBACK, "input_tokens": 0, "output_tokens": 0}.
#   Otherwise it calls client.messages.create(...) exactly once, with keyword arguments:
#     model: the PRACTICE_MODEL environment variable, read at the time of the call, or DEFAULT_MODEL when it is not
#     set (unset it first in a test of the default);
#     max_tokens: a whole number;
#     system: SYSTEM;
#     messages: a list with one dict, {"role": "user", "content": ...}, whose content is one string containing every
#     passage and the question.
#   It returns {"answer": ..., "input_tokens": ..., "output_tokens": ...}: the reply's text with whitespace removed
#   from both ends, and the two token counts.
def test_replace_this_with_your_own_tests():
    raise NotImplementedError
