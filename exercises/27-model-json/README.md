# 27. Parsing JSON a model returns, and refusing bad JSON

The reranker asks a model which passages answer the question and wants numbers back, not prose:
`{"ranked": [2, 0]}`. A model usually complies. Sometimes it wraps the JSON in a code fence, writes a sentence
instead, or names a passage it was never given. Code that trusts the reply breaks in production; code that checks it
falls back to the order it already had.

Write three functions in `solution.py`:

- `strip_fence(text)` returns the text without whitespace at the ends and, if it is wrapped in a Markdown code fence
  (a first line starting with three backticks, with or without the word `json`, and a last line of three
  backticks), without those two lines. Text with no fence comes back stripped, otherwise unchanged.
- `parse_ranking(text, pool_size)` returns the list of passage numbers in the reply, in the reply's order, repeats
  dropped (the first one stays). It accepts a fenced reply. It raises `ValueError` when:
  - the text is not JSON;
  - the JSON is not an object with the key `"ranked"`;
  - `"ranked"` is not a list, or an item in it is not a whole number (`"two"`, `1.5`);
  - a number is less than 0 or not less than `pool_size`.
- `rerank(client, question, passages, keep=3)` returns `keep` passage positions, best first. With no passages it
  returns `[]` and makes no call. Otherwise it makes one call, `client.messages.create(model=RERANK_MODEL,
  max_tokens=1024, system=RULES, messages=[...])`, with one user message whose content is `prompt(question,
  passages)` (given), and parses `response.content[0].text` with `parse_ranking`. The model's choice goes first,
  then the positions it did not name in their original order, and the list is cut to `keep`. If `parse_ranking`
  raises `ValueError`, return the first `keep` positions in their original order.

```python
strip_fence('```json\n{"ranked": [2, 0]}\n```')    # '{"ranked": [2, 0]}'
parse_ranking('{"ranked": [2, 0, 2]}', 4)          # [2, 0]
parse_ranking('{"ranked": [7]}', 4)                # ValueError
parse_ranking("Passage 2 is the best.", 4)         # ValueError

# four passages, the model replies {"ranked": [2]}
rerank(client, "Can I return a sale item?", passages, keep=3)   # [2, 0, 1]
# the model replies "Passage 2 is the best."
rerank(client, "Can I return a sale item?", passages, keep=3)   # [0, 1, 2]
```

Two ways to check the shape, both fine: `json.loads` and your own `isinstance` checks, or a pydantic model
(`class Ranking(BaseModel): ranked: list[int]`) and `Ranking.model_validate_json(text)`. `json.JSONDecodeError` and
pydantic's `ValidationError` are both kinds of `ValueError` already, so they need no translating. If you check by
hand: in Python `True` is an `int`; the tests do not send booleans.

You will use: `str.strip`, `str.splitlines`, `str.startswith`, `json.loads` or pydantic, `isinstance`,
`dict.fromkeys` (drops repeats, keeps order), `try` / `except ValueError`.
