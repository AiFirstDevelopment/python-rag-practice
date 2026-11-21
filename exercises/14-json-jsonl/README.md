# 14. JSON and JSONL

Two file formats carry almost everything a pipeline and its harness keep. JSON holds one value (the summary of an
eval run). JSONL, "JSON lines", holds one JSON object per line (the golden set, the chunks, each case's result): it
can be appended to one line at a time, and one bad line does not spoil the rest.

Write five functions in `solution.py`. Every `path` is a `Path`; every file is UTF-8.

- `save_run(path, run)`: writes the dict `run` as JSON, indented by 2 spaces, with characters outside ASCII written
  as themselves (`é`, not `é`).
- `load_run(path)`: the dict read back from such a file.
- `write_jsonl(path, rows)`: writes each dict of `rows` as one line of JSON, in order, each line ending with a line
  break, replacing the file. Characters outside ASCII are written as themselves here too. No rows gives an empty
  file.
- `append_jsonl(path, row)`: adds one row as one more line at the end of the file, creating the file if it does not
  exist.
- `read_jsonl(path)`: the rows as a list of dicts, in order. Lines that are empty or only whitespace are skipped.
  A line that is not JSON raises `ValueError` with a message that contains `line N`, where N is that line's number
  in the file counted from 1 (blank lines count).

```python
save_run(Path("run.json"), {"passed": 18, "failed": 2})
load_run(Path("run.json"))                                 # {"passed": 18, "failed": 2}
write_jsonl(Path("results.jsonl"), [{"id": "returns-01", "status": "pass"}])
append_jsonl(Path("results.jsonl"), {"id": "returns-02", "status": "fail"})
read_jsonl(Path("results.jsonl"))
# [{"id": "returns-01", "status": "pass"}, {"id": "returns-02", "status": "fail"}]
read_jsonl(path_with_a_bad_third_line)                     # ValueError: line 3: not JSON
```

You will use: `json.dumps(value, indent=2, ensure_ascii=False)`, `json.loads(text)`, `path.read_text` and
`path.write_text` with `encoding="utf-8"`, `open(path, "a", encoding="utf-8")` in a `with` block, `splitlines()`,
`enumerate(lines, 1)`, `raise ValueError(...) from error`.
