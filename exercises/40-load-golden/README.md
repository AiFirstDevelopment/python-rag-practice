# 40. Load the golden set

> **Your lesson:** [lessons/40-load-golden.md](../../lessons/40-load-golden.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

The golden set is the list of questions the harness asks the pipeline, each with what a right answer must hold and
where in the documents it comes from. It is a JSONL file people edit by hand, so it will have typos. A typo must stop
the run with the line number, not turn into a wrong score nobody notices.

One line of the file:

```json
{"id": "returns-01", "category": "answerable", "question": "How long do I have to return an item?", "expected_behavior": "answer", "required_facts": [{"fact": "30 days of delivery", "match": ["30 days", "thirty days"]}], "sources": [{"file": "returns.txt", "page": 1}]}
```

Exercise 10 built a first version of these models. This one is the harness's own: it adds `category`, which the
run report groups by, and leaves out the length and page checks to match the course's `evals/harness.py`.

Write in `solution.py`:

- Three pydantic models:
  - `Fact`: `fact` (a string, the fact in words) and `match` (a list of strings, any one of which in an answer counts
    as the fact).
  - `Source`: `file` (a string) and `page` (an integer).
  - `Case`: `id` (string), `category` (one of `"answerable"`, `"inferred"`, `"absent"`), `question` (string),
    `expected_behavior` (one of `"answer"`, `"fallback"`), `required_facts` (a list of `Fact`), `sources` (a list of
    `Source`). Every field is required; the two lists may be empty.
- `load_cases(path)`: reads the file at `path` (UTF-8) and returns its cases as a list of `Case`, in file order.
  - A blank line (empty or only whitespace) is skipped.
  - A line is bad when it is not JSON, when it does not fit `Case` (a field missing, a value not allowed), or when
    its `id` was already used by an earlier good line.
  - If any line is bad, raise `GoldenSetError(lines)` (given in the starter) with the line numbers of every bad
    line, not only the first, in ascending order. Line numbers start at 1 and count blank lines, so they match what
    an editor shows.

```python
cases = load_cases(Path("golden.jsonl"))
cases[0].id                        # "returns-01"
cases[0].required_facts[0].match   # ["30 days", "thirty days"]
cases[0].sources[0].page           # 1

load_cases(Path("broken.jsonl"))   # GoldenSetError: bad lines in the golden set: 2, 5
```

You will use: `pydantic.BaseModel`, `typing.Literal`, `Case.model_validate_json(line)`, `pydantic.ValidationError`
(raised for bad JSON and for a line that does not fit), `Path.read_text`, `enumerate(lines, 1)`.
