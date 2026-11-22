# Your task is in README.md. Each EXERCISE-TODO comment below is one piece to write.
# Save, then type /check in the Claude chat.
import json
from pathlib import Path


# EXERCISE-TODO: save_run(path, run): write the dict run to path as UTF-8 JSON, indented by 2 spaces, with characters
# outside ASCII written as themselves (é, not \u00e9).
#   save_run(Path("run.json"), {"passed": 18, "failed": 2})
def save_run(path: Path, run: dict) -> None:
    raise NotImplementedError


# EXERCISE-TODO: load_run(path): return the dict read back from a file written by save_run.
#   load_run(Path("run.json"))  ->  {"passed": 18, "failed": 2}
def load_run(path: Path) -> dict:
    raise NotImplementedError


# EXERCISE-TODO: write_jsonl(path, rows): write each dict of rows as one line of JSON, in order, each line ending with a
# line break, replacing the file. Characters outside ASCII are written as themselves. No rows gives an empty file.
#   write_jsonl(Path("results.jsonl"), [{"id": "returns-01", "status": "pass"}])
def write_jsonl(path: Path, rows: list[dict]) -> None:
    raise NotImplementedError


# EXERCISE-TODO: append_jsonl(path, row): add one row as one more line at the end of the file, creating the file if it
# does not exist.
#   append_jsonl(Path("results.jsonl"), {"id": "returns-02", "status": "fail"})
def append_jsonl(path: Path, row: dict) -> None:
    raise NotImplementedError


# EXERCISE-TODO: read_jsonl(path): return the rows as a list of dicts, in order. Lines that are empty or only whitespace
# are skipped. A line that is not JSON raises ValueError with a message that contains "line N", where N is that line's
# number in the file counted from 1 (blank lines count).
#   read_jsonl(Path("results.jsonl"))
#     ->  [{"id": "returns-01", "status": "pass"}, {"id": "returns-02", "status": "fail"}]
#   read_jsonl(path_with_a_bad_third_line)  ->  ValueError: line 3: not JSON
def read_jsonl(path: Path) -> list[dict]:
    raise NotImplementedError
