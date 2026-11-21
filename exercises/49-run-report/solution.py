import json
from pathlib import Path


def load_results(path: Path) -> list[dict]:
    raise NotImplementedError


def summarize(results: list[dict], input_price: float, output_price: float, slowest: int = 3) -> dict:
    raise NotImplementedError


def to_markdown(summary: dict) -> str:
    raise NotImplementedError
