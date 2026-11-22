# Your task is in README.md. Each EXERCISE-TODO comment below is one piece to write.
# Save, then type /check in the Claude chat.
from pathlib import Path

# Given: the suffixes that make a file a document.
DOC_SUFFIXES = {".txt", ".md", ".pdf"}


# EXERCISE-TODO: list_docs(folder): folder is a Path; return the names ("returns.txt", not the whole path) of the
# documents directly in folder, sorted. Documents are files whose suffix is .txt, .md or .pdf, in any case (NOTES.TXT
# counts). Folders are left out even when their name ends in .txt, and so are files in subfolders.
#   list_docs(Path("docs"))  ->  ["returns.txt", "shipping.pdf"]
def list_docs(folder: Path) -> list[str]:
    raise NotImplementedError


# EXERCISE-TODO: all_docs(folder): return the documents in folder and in every folder below it, each as its path
# relative to folder written with forward slashes ("policies/warranty.txt"), sorted.
#   all_docs(Path("docs"))  ->  ["policies/warranty.txt", "returns.txt", "shipping.pdf"]
def all_docs(folder: Path) -> list[str]:
    raise NotImplementedError


# EXERCISE-TODO: output_path(doc, out_dir): return the Path where the chunks of doc are written: in out_dir, the
# document's name without its suffix, then .chunks.jsonl. Nothing is created; it only builds the Path.
#   output_path(Path("docs/shipping.pdf"), Path("out"))  ->  Path("out/shipping.chunks.jsonl")
def output_path(doc: Path, out_dir: Path) -> Path:
    raise NotImplementedError


# EXERCISE-TODO: save(path, text): write text to path as UTF-8, creating any missing folders above it, replacing the
# file if it exists, and return path.
#   save(Path("out/runs/today/notes.txt"), "café")  ->  Path("out/runs/today/notes.txt"), folders created
def save(path: Path, text: str) -> Path:
    raise NotImplementedError
