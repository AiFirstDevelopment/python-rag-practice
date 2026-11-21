from pathlib import Path

from pypdf import PdfReader


def pdf_pages(path: Path) -> list[str]:
    raise NotImplementedError


def load_pages(path: Path) -> list[tuple[int, str]]:
    raise NotImplementedError
