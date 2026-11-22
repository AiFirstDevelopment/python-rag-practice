"""The document side of the server: load the ferry's documents, search them, and say how fresh the index is.

Nothing in this file knows about MCP. Keeping retrieval in plain functions means it can be tested on its own, reused
by an HTTP endpoint or a batch job, and swapped for a real pipeline (embeddings, BM25, rank fusion, a reranker)
without touching the MCP layer. The server modules only translate between these functions and the protocol.
"""

import math
import re
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from itertools import batched, chain, groupby, islice
from pathlib import Path

CORPUS = Path(__file__).resolve().parents[2] / "exercises" / "50-final-project" / "corpus"
PAGE_BREAK = "--- page break ---"
WORD = re.compile(r"[a-z0-9$]+")
STOP = frozenset("a an and are as at be by can do for from how i if in is it of on or the to what when with you".split())


@dataclass(frozen=True)
class Page:
    file: str
    page: int
    text: str


@dataclass(frozen=True)
class Document:
    name: str
    title: str
    modified: datetime          # always timezone-aware, in UTC
    pages: tuple[Page, ...]

    @property
    def text(self) -> str:
        return f"\n{PAGE_BREAK}\n".join(page.text for page in self.pages)


def modified_at(path: Path) -> datetime:
    """A file's last change as an aware UTC datetime.

    `st_mtime` is seconds since the epoch, which has no time zone of its own. Naive datetimes (no tzinfo) compare
    wrongly against aware ones and break the moment a server runs somewhere other than the developer's laptop, so
    every time in this server is aware and in UTC; it is converted to a local zone only for display.
    """
    return datetime.fromtimestamp(path.stat().st_mtime, tz=UTC)


def load(folder: Path = CORPUS) -> dict[str, Document]:
    """Every .txt file in the folder, split into pages, keyed by file name."""
    documents = {}
    for path in sorted(folder.glob("*.txt")):
        raw = path.read_text(encoding="utf-8")
        pages = tuple(Page(path.name, number, text.strip())
                      for number, text in enumerate(raw.split(PAGE_BREAK), start=1))
        documents[path.name] = Document(path.name, raw.splitlines()[0].strip(), modified_at(path), pages)
    return documents


def words(text: str) -> list[str]:
    return [w for w in WORD.findall(text.lower()) if w not in STOP]


@dataclass(frozen=True)
class Hit:
    file: str
    page: int
    score: float
    text: str


class Index:
    """A small BM25 keyword index over pages.

    BM25 rewards a page for containing the query's words, more for rare words than common ones (the idf term), with
    diminishing returns for repeats (k1) and a correction for long pages (b). It stands in for the full pipeline: a
    production server would put vector search and rank fusion behind the same `search` signature.
    """

    k1, b = 1.5, 0.75

    def __init__(self, documents: dict[str, Document]):
        self.built_at = datetime.now(UTC)
        # chain.from_iterable flattens "pages of each document" into one stream of pages without building nested lists.
        self.pages = list(chain.from_iterable(doc.pages for doc in documents.values()))
        self.counts = [Counter(words(page.text)) for page in self.pages]
        self.lengths = [sum(c.values()) for c in self.counts]
        self.average = sum(self.lengths) / max(len(self.lengths), 1)
        frequency = Counter(chain.from_iterable(c.keys() for c in self.counts))
        n = len(self.pages)
        self.idf = {w: math.log(1 + (n - f + 0.5) / (f + 0.5)) for w, f in frequency.items()}

    def search(self, query: str, k: int = 5) -> list[Hit]:
        terms = words(query)
        scored = []
        for page, counts, length in zip(self.pages, self.counts, self.lengths):
            score = 0.0
            for term in terms:
                tf = counts.get(term, 0)
                if tf:
                    score += self.idf[term] * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * length / self.average))
            if score > 0:
                scored.append(Hit(page.file, page.page, round(score, 3), page.text))
        return sorted(scored, key=lambda hit: hit.score, reverse=True)[:k]


def sources_by_document(hits: list[Hit]) -> list[dict]:
    """Collapse page-level hits into one entry per document: {"file": "fares.txt", "pages": [1, 2]}.

    `groupby` only groups *adjacent* items with the same key, so the hits are sorted by file first. Forgetting the
    sort is the classic groupby bug: the same file then shows up as several groups.
    """
    ordered = sorted(hits, key=lambda hit: (hit.file, hit.page))
    return [{"file": file, "pages": sorted({hit.page for hit in group})}
            for file, group in groupby(ordered, key=lambda hit: hit.file)]


def page_of(items: list, cursor: str | None, size: int) -> tuple[list, str | None]:
    """One page of a long list, MCP style: an opaque cursor in, the items and the next cursor (or None) out.

    The cursor here is just the offset as a string, but callers must treat it as opaque, which leaves the server
    free to change it later (a database key, a signed token). `islice` takes the slice from any iterable, so the
    same code works when `items` becomes a generator over a database cursor that cannot be indexed.
    """
    start = int(cursor) if cursor else 0
    if start < 0:
        raise ValueError("cursor must come from a previous page")
    chunk = list(islice(items, start, start + size))
    more = start + size < len(items)
    return chunk, (str(start + size) if more else None)


def stale_documents(documents: dict[str, Document], built_at: datetime) -> list[str]:
    """The documents changed after the index was built: what a re-index has to pick up."""
    return sorted(name for name, doc in documents.items() if doc.modified > built_at)


def describe_age(then: datetime, now: datetime) -> str:
    """'3 days ago', '2 hours ago', 'just now'. Subtracting two aware datetimes gives a timedelta."""
    age = now - then
    if age.days >= 1:
        return f"{age.days} day{'s' if age.days > 1 else ''} ago"
    hours = age.seconds // 3600
    if hours:
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    minutes = age.seconds // 60
    return f"{minutes} minute{'s' if minutes > 1 else ''} ago" if minutes else "just now"


def parse_since(value: str) -> datetime:
    """An ISO 8601 date or date-time from a tool argument, as an aware UTC datetime.

    Models send dates in many shapes. Accept the standard ones ("2026-11-20", "2026-11-20T09:30:00Z", with an
    offset), read a value without a zone as UTC, and raise a ValueError that says what was expected otherwise;
    the server turns that message into a tool error the model can act on.
    """
    try:
        parsed = datetime.fromisoformat(value.strip())
    except ValueError:
        raise ValueError(f"'{value}' is not a date; use ISO 8601, for example 2026-11-20 or 2026-11-20T09:30:00Z") from None
    return parsed.replace(tzinfo=UTC) if parsed.tzinfo is None else parsed.astimezone(UTC)


def reindex_batches(pages: list[Page], size: int = 16):
    """Pages in batches of `size`, the way an embedding API wants them (it caps the inputs per request)."""
    return batched(pages, size)
