# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
import json
import math
import re
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass

import anthropic
import numpy as np

# ---- Given: every piece from exercises 30 to 38. Do not change them. Yours starts at the bottom of the file. ----

CHUNK_CHARS = 900
ENDS = (". ", "? ", "! ", ".\n", "?\n", "!\n")
K1, B = 1.2, 0.75
RRF_K = 60
POOL = 8                 # how many fused chunks the reranker reads
KEEP = 3                 # how many chunks the reranker hands on
WIDEN_CHARS = 10_800
RERANK_MODEL = "claude-haiku-5-5"
MODEL = "claude-opus-5-5"
RULES = """You choose which passages answer a question about a set of documents.
You are given the question and a numbered list of passages.
Reply with JSON only, in this shape: {"ranked": [2, 0]}
"ranked" holds the numbers of the passages that answer the question, best first.
Use an empty list if none answers it."""
SYSTEM = ("Answer only from the passages, in a few plain sentences without Markdown. "
          "If the answer is not in them, say you don't know.")
DONT_KNOW = "I don't know."
DECLINED = "The model declined."
STOP = set("a an and are as at be by can could do does for from how i if in is it its me my of on or should so that "
           "the their them there this to was what when where which who why will with would you your".split())

Embed = Callable[[str], np.ndarray]          # a function from a text to its vector


@dataclass
class Chunk:
    file: str
    page: int
    seq: int          # its place in its file's order of chunks
    text: str


@dataclass
class Passage:
    file: str
    first_page: int
    last_page: int
    text: str


def chunk_page(text: str) -> list[str]:
    """Exercise 30: one page's text in pieces of at most 900 characters, cut at sentence ends."""
    pieces, rest = [], text.strip()
    while len(rest) > CHUNK_CHARS:
        window = rest[:CHUNK_CHARS]
        sentence = max(window.rfind(end) for end in ENDS)
        space = window.rfind(" ")
        cut = sentence + 1 if sentence > CHUNK_CHARS / 2 else space if space > 0 else CHUNK_CHARS
        pieces.append(rest[:cut].strip())
        rest = rest[cut:].strip()
    if rest:
        pieces.append(rest)
    return pieces


def chunk_file(file: str, pages: list[str]) -> list[Chunk]:
    """Exercise 31: every page of one file, chunked; pages count from 1, seq from 0 across the file."""
    texts = [(page, piece) for page, text in enumerate(pages, 1) for piece in chunk_page(text)]
    return [Chunk(file, page, seq, piece) for seq, (page, piece) in enumerate(texts)]


def words(text: str) -> list[str]:
    """Lower-cased runs of letters and digits, stop words out, a plain plural's "s" off."""
    tokens = [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]
    return [w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w for w in tokens]


def bm25(chunks: list[Chunk], question: str, limit: int) -> list[Chunk]:
    """Exercise 32: the chunks sharing words with the question, best first."""
    docs = [Counter(words(c.text)) for c in chunks]
    if not docs:
        return []
    frequency = Counter(word for doc in docs for word in doc)
    average = sum(doc.total() for doc in docs) / len(docs) or 1
    scored = []
    for chunk, doc in zip(chunks, docs):
        score = 0.0
        for word in set(words(question)):
            n, tf = frequency[word], doc[word]
            if tf == 0:
                continue
            idf = math.log(1 + (len(chunks) - n + 0.5) / (n + 0.5))
            score += idf * tf * (K1 + 1) / (tf + K1 * (1 - B + B * doc.total() / average))
        if score > 0:
            scored.append((score, chunk))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [chunk for _, chunk in scored[:limit]]


def embed_chunks(chunks: list[Chunk], embed: Embed) -> np.ndarray:
    """Exercise 33: one row per chunk."""
    return np.array([embed(chunk.text) for chunk in chunks])


def nearest(vectors: np.ndarray, query: np.ndarray, limit: int) -> list[int]:
    """Exercise 33: the indexes of the rows most like the query, by cosine similarity, best first."""
    scores = vectors @ query / (np.linalg.norm(vectors, axis=1) * np.linalg.norm(query))
    return [int(i) for i in np.argsort(scores)[::-1][:limit]]


def vector_search(chunks: list[Chunk], vectors: np.ndarray, question: str, embed: Embed, limit: int) -> list[Chunk]:
    """Exercise 33: the chunks nearest to the question, best first."""
    if not chunks:
        return []
    return [chunks[i] for i in nearest(vectors, embed(question), limit)]


def fuse(rankings: list[list[Chunk]], limit: int) -> list[Chunk]:
    """Exercise 34: reciprocal rank fusion of ranked lists, best first."""
    scores: dict[tuple[str, int], float] = {}
    chunk_at: dict[tuple[str, int], Chunk] = {}
    for ranking in rankings:
        for rank, chunk in enumerate(ranking, 1):
            key = (chunk.file, chunk.seq)
            scores[key] = scores.get(key, 0) + 1 / (RRF_K + rank)
            chunk_at[key] = chunk
    best = sorted(scores, key=scores.get, reverse=True)[:limit]
    return [chunk_at[key] for key in best]


async def rerank(client, question: str, pool: list[Chunk], keep: int = KEEP) -> list[Chunk]:
    """Exercise 35: the model's choice first, then the rest of the pool; fusion order if its reply cannot be used."""
    if not pool:
        return []
    numbered = "\n\n".join(f"[{i}] {chunk.text}" for i, chunk in enumerate(pool))
    try:
        response = await client.messages.create(
            model=RERANK_MODEL,
            max_tokens=1024,
            system=RULES,
            messages=[{"role": "user", "content": f"Question: {question}\n\nPassages:\n\n{numbered}"}],
        )
        ranked = json.loads(response.content[0].text)["ranked"]
        if not isinstance(ranked, list) or any(type(n) is not int or not 0 <= n < len(pool) for n in ranked):
            raise ValueError(f"not a list of passage numbers: {ranked}")
    except (anthropic.APIError, ValueError, KeyError, TypeError, IndexError):
        return pool[:keep]
    chosen = list(dict.fromkeys(ranked))
    rest = [n for n in range(len(pool)) if n not in chosen]
    return [pool[n] for n in chosen + rest][:keep]


def widen(given: list[Chunk], everything: list[Chunk], budget: int = WIDEN_CHARS) -> list[Passage]:
    """Exercise 36: each given chunk joined with its neighbours in the same file, within the budget."""
    at = {(c.file, c.seq): c for c in everything}
    taken, added = {(c.file, c.seq) for c in given}, 0
    for chunk in given:
        for seq in (chunk.seq - 1, chunk.seq + 1):
            neighbour = at.get((chunk.file, seq))
            if neighbour is None or (chunk.file, seq) in taken or added + len(neighbour.text) > budget:
                continue
            taken.add((chunk.file, seq))
            added += len(neighbour.text)
    passages, placed = [], set()
    for chunk in given:
        if (chunk.file, chunk.seq) in placed:
            continue
        lo = hi = chunk.seq
        while (chunk.file, lo - 1) in taken:
            lo -= 1
        while (chunk.file, hi + 1) in taken:
            hi += 1
        run = [at[(chunk.file, seq)] for seq in range(lo, hi + 1)]
        placed.update((c.file, c.seq) for c in run)
        passages.append(Passage(chunk.file, run[0].page, run[-1].page, "\n".join(c.text for c in run)))
    return passages


def format_passages(passages: list[Passage]) -> str:
    """Exercise 37: each passage numbered, with its file and page, then its text."""
    return "\n\n".join(
        f"[{n}] {p.file}, " + (f"page {p.first_page}" if p.first_page == p.last_page
                               else f"pages {p.first_page}-{p.last_page}") + f"\n{p.text}"
        for n, p in enumerate(passages, 1)
    )


def build_request(question: str, passages: list[Passage]) -> dict:
    """Exercise 37: the keyword arguments of the answer's model call."""
    content = f"Passages:\n\n{format_passages(passages)}\n\nQuestion: {question}"
    return {"model": MODEL, "max_tokens": 1024, "system": SYSTEM, "messages": [{"role": "user", "content": content}]}


async def answer(client, question: str, passages: list[Passage]) -> str:
    """Exercise 38: the model's answer from the passages only; "I don't know." when there are none."""
    if not passages:
        return DONT_KNOW
    response = await client.messages.create(**build_request(question, passages))
    if response.stop_reason == "refusal":
        return DECLINED
    return response.content[0].text


# ---- Yours ----

async def ask(documents: dict[str, list[str]], question: str, embed: Embed, client) -> tuple[str, list[Passage]]:
    raise NotImplementedError
