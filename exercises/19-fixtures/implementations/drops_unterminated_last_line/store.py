import json
from pathlib import Path


def append_jsonl(path: Path, row: dict) -> None:
    with open(path, "a", encoding="utf-8") as file:
        file.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").split("\n")[:-1]      # whatever follows the last line break is lost
    return [json.loads(line) for line in lines if line.strip()]
