# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
import json
from pathlib import Path


def save_run(path: Path, run: dict) -> None:
    raise NotImplementedError


def load_run(path: Path) -> dict:
    raise NotImplementedError


def write_jsonl(path: Path, rows: list[dict]) -> None:
    raise NotImplementedError


def append_jsonl(path: Path, row: dict) -> None:
    raise NotImplementedError


def read_jsonl(path: Path) -> list[dict]:
    raise NotImplementedError
