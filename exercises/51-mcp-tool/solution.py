# Your task is in README.md in this folder. The code at the top is given; yours goes under "Yours" at line 32.
# Each EXERCISE-TODO comment below is one piece to write. Save, then type /check in the Claude chat.
import re
from pathlib import Path

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

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

# EXERCISE-TODO: create_server(): return a FastMCP server named "ferry-docs" with one tool, search(query: str,
# k: int = 3) -> dict. search returns {"passages": keyword_search(documents, query, k)}: at most k {"file", "text"}
# dicts. Its docstring is the description the model reads: say it searches Brackwater Ferry's documents. Mark it
# read-only with the annotation readOnlyHint True. A query shorter than 2 characters after stripping raises
# ToolError with a message containing "at least 2 characters".
#   search(query="How much do children pay?")  ->  {"passages": [{"file": "fares.txt", "text": "..."}, ...]}
def create_server() -> FastMCP:
    raise NotImplementedError
