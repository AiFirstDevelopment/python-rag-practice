# Your task is in README.md in this folder. The code at the top is given; yours goes under "Yours" at line 32.
# Each EXERCISE-TODO comment below is one piece to write. Save, then type /check in the Claude chat.
import json
import re
from pathlib import Path

from fastmcp import FastMCP

# ---- Given: the pipeline project's documents and a small keyword search. Do not change. ----

CORPUS = Path(__file__).resolve().parents[1] / "50-pipeline-project" / "corpus"
PAGE_BREAK = "--- page break ---"


def load_documents(folder: Path = CORPUS) -> dict[str, str]:
    """Each document's full text, by file name: {"fares.txt": "Brackwater Ferry: fares and tickets ...", ...}."""
    return {p.name: p.read_text() for p in sorted(folder.glob("*.txt"))}


def keyword_search(documents: dict[str, str], query: str, k: int) -> list[dict]:
    """The k paragraphs that share the most words with the query, best first, as {"file", "text"} dicts."""
    words = set(re.findall(r"[a-z0-9]+", query.lower()))
    scored = []
    for name, text in documents.items():
        for para in re.split(r"\n\s*\n", text.replace(PAGE_BREAK, "\n\n")):
            hits = len(words & set(re.findall(r"[a-z0-9]+", para.lower())))
            if hits:
                scored.append((-hits, name, " ".join(para.split())))
    return [{"file": name, "text": text} for _, name, text in sorted(scored)[:k]]


# ---- Yours ----

# EXERCISE-TODO: create_server(): return a FastMCP server named "ferry-docs" with
# - one resource per document at "ferry://documents/<file name>", named after the file, mime_type "text/plain",
#   whose content is that document's full text;
# - a resource "ferry://documents" (mime_type "application/json"): a JSON list of the file names, sorted;
# - a prompt answer_from_documents(question: str) -> str whose text contains the question and tells the model to
#   answer from the documents only and cite the file.
#   read "ferry://documents/fares.txt"  ->  "Brackwater Ferry: fares and tickets ..."
#   read "ferry://documents"            ->  '["disruptions.txt", "fares.txt", "onboard.txt", "vehicles.txt"]'
def create_server() -> FastMCP:
    raise NotImplementedError
