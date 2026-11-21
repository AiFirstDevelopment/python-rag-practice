from pathlib import Path

# Given: the suffixes that make a file a document.
DOC_SUFFIXES = {".txt", ".md", ".pdf"}


def list_docs(folder: Path) -> list[str]:
    raise NotImplementedError


def all_docs(folder: Path) -> list[str]:
    raise NotImplementedError


def output_path(doc: Path, out_dir: Path) -> Path:
    raise NotImplementedError


def save(path: Path, text: str) -> Path:
    raise NotImplementedError
