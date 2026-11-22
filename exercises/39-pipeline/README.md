# 39. The whole pipeline in one function

> **Your lesson:** [lessons/39-pipeline.md](../../lessons/39-pipeline.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

Each piece of the last nine exercises does one job. A RAG pipeline is those pieces in a fixed order: chunk the
documents, search them two ways, fuse the two rankings, let a model rerank the best of them, widen what it chose,
and have the model answer from those passages only. Writing the order down yourself is how you learn where to look
when an answer is wrong: was the chunk not found, not chosen, or not used?

Every earlier piece is given at the top of `solution.py`, as you wrote it in exercises 30 to 38 (`chunk_file`,
`bm25`, `embed_chunks`, `vector_search`, `fuse`, `rerank`, `widen`, `answer`), so this exercise does not depend on
your earlier files. Read their signatures; do not change them.

Write the async function `ask(documents, question, embed, client)`:

- `documents` is a dict from a file name to the list of that file's page texts, for example
  `{"returns.txt": ["..."], "shipping.pdf": ["page 1 ...", "page 2 ..."]}`.
- `embed` is a function from a text to its vector, as in exercise 33.
- `client` is the model client, as in exercises 35 and 37.

It returns a tuple `(reply, passages)`: the answer's text, and the list of `Passage` the model answered from, so a
caller (or the eval harness of module 8) can see the sources.

The steps, in order:

1. Chunk every file with `chunk_file`, in the dict's order, into one list of chunks. If there are no chunks at all
   (no documents, or only empty pages), return `(DONT_KNOW, [])` at once, with no model call.
2. Keyword search: `bm25` over the chunks, with a limit of `POOL * 2`.
3. Vector search: embed the chunks with `embed_chunks`, then `vector_search` with a limit of `POOL`.
4. Fuse the two rankings (keyword first, then vector) with `fuse`, keeping `POOL` chunks. This is the pool.
5. `rerank` the pool with the client. It returns the `KEEP` best chunks, and falls back to fusion order by itself
   when the model's reply cannot be used.
6. `widen` those chunks with their neighbours, out of all the chunks. These are the passages.
7. `answer` the question from the passages with the client. This is the reply.

`POOL` is 8 and `KEEP` is 3. That makes two model calls a question: the reranker's, then the answer's.

```python
documents = {"returns.txt": ["Returns are accepted within 30 days. Sale items are returned for store credit."]}
reply, passages = await ask(documents, "Can I return a sale item?", embed, client)
# reply: what the model answered from the passages
# passages: [Passage(file="returns.txt", first_page=1, last_page=1, text="Returns are accepted ...")]
```

A real pipeline chunks and embeds its documents once, when it starts, and keeps them (the course's `Index` class);
here it is one function so the order is in front of you.

You will use: a loop over `dict.items()`, `list.extend` or a nested comprehension, `await`, returning a tuple.
