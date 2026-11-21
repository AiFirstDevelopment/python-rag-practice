# 03. Dictionaries

An eval run produces one record per question. To see where it fails, you count the records by a field.

Write two functions in `solution.py`:

- `count_by(records, key)`: each record is a dict; return a dict from each value of `record[key]` to how many
  records have it. A record without that key is counted under `None`.
- `pass_rate(records)`: the share of records whose `"result"` is `"pass"`, as a float from 0 to 1, rounded to 2
  places. An empty list gives `0.0`.

```python
runs = [{"category": "absent", "result": "pass"},
        {"category": "answerable", "result": "fail"},
        {"category": "answerable", "result": "pass"}]
count_by(runs, "category")  # {"absent": 1, "answerable": 2}
pass_rate(runs)             # 0.67
```

You will use: dicts, `.get`, loops, `round`.
