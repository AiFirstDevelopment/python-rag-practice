# 10. A pydantic model for a golden-set line

The eval harness reads its questions from a golden set: a file with one JSON object per line. A typo in that file
(`"fallbak"`, a page written as `"one"`) must stop the run with a clear error, not turn into a wrong score nobody
notices. A dataclass does not check its values. A pydantic model does, every time one is made.

One line of the golden set:

```json
{"id": "returns-02", "question": "Can I get my money back for a sale item?", "expected_behavior": "answer",
 "required_facts": [{"fact": "store credit", "match": ["store credit"]}],
 "sources": [{"file": "returns.txt", "page": 1}]}
```

Write three models (classes that inherit from pydantic's `BaseModel`) and two functions in `solution.py`:

- `Fact`: `fact: str` and `match: list[str]` (the spellings that count as stating the fact).
- `Source`: `file: str` and `page: int`, where `page` must be 1 or more.
- `Case`: `id: str`; `question: str`, at least one character long; `expected_behavior`, which must be exactly
  `"answer"` or `"fallback"`; `required_facts: list[Fact]`; `sources: list[Source]`. All five are required (the two
  lists may be empty).
- `parse_case(line)`: the `Case` for one line of JSON text. A line that is not JSON, or does not fit the model,
  raises pydantic's `ValidationError` (which is a `ValueError`).
- `load_cases(lines)`: takes the lines of a file and returns a tuple `(cases, bad)`: the cases that parsed, in
  order, and the line numbers, counted from 1, of the lines that did not. A line that is empty or only whitespace is
  skipped: it is neither a case nor bad, but it still counts as a line.

```python
case = parse_case(line)            # the line above
case.required_facts[0].match       # ["store credit"]
case.sources[0].page               # 1
parse_case('{"id": "x", "question": "Hi", "expected_behavior": "fallbak", "required_facts": [], "sources": []}')
# ValidationError: expected_behavior: Input should be 'answer' or 'fallback'
load_cases([line, "", "not json", line])   # ([Case(...), Case(...)], [3])
```

You will use: `BaseModel`, `Literal["answer", "fallback"]`, `Field(ge=1)` and `Field(min_length=1)`, a model as the
type of another model's field, `Case.model_validate_json(line)`, `try` / `except ValidationError`.
