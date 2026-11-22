# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
from pathlib import Path

from pypdf import PdfReader


def pdf_pages(path: Path) -> list[str]:
    raise NotImplementedError


def load_pages(path: Path) -> list[tuple[int, str]]:
    raise NotImplementedError
