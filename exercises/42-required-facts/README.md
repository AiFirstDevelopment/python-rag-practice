# 42. Check required facts in an answer

> **Your lesson:** [lessons/42-required-facts.md](../../lessons/42-required-facts.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

A model never words an answer the same way twice, so the harness cannot compare an answer to one expected string.
Instead each golden case lists the facts a right answer must hold, and for each fact the words that count as saying
it: "30 days" or "thirty days". Checking is plain text search: no model call, the same result every time.

The starter gives you the `Fact` model: `fact` is the fact in words (for the report), `match` is the list of
strings, any one of which in the answer counts.

Write in `solution.py`:

- `has_fact(fact, answer)`: `True` when at least one of the fact's `match` strings appears in the answer.
  - Case does not matter, in the answer or in the match string: `"No."` matches an answer that says `"no."`.
  - It is a substring search: `"tennis ball"` matches an answer that says "tennis balls".
  - A fact with an empty `match` list is never found.
- `missing_facts(facts, answer)`: the `fact` text of every fact the answer does not hold, in the order the facts were
  given. An empty list means the answer holds them all.

```python
facts = [Fact(fact="store credit", match=["store credit"]),
         Fact(fact="within 14 days", match=["14 days", "fourteen days"])]
has_fact(facts[1], "Bring it back within Fourteen Days.")       # True
missing_facts(facts, "You get Store Credit.")                   # ["within 14 days"]
missing_facts(facts, "Store credit, within 14 days.")           # []
```

You will use: `str.lower`, `in` on strings, `any`, a list comprehension with a condition.
