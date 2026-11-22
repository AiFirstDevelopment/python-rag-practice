# 35. Reranking with a model

> **Your lesson:** [lessons/35-rerank.md](../../lessons/35-rerank.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

Fusion gives a pool of likely chunks, ranked by word overlap and vector distance, neither of which reads the
question. A small, cheap model does: it is shown the question and the pool, and names the passages that answer it.
Its choice goes first; the rest of the pool follows in fusion order, so the reranker orders the context, it never
empties it. And when the model's reply cannot be used, the pipeline carries on with fusion order instead of failing.

`Chunk`, `RERANK_MODEL`, `KEEP` (3) and the system prompt `RULES` are given at the top of `solution.py`. Write the
async function `rerank(client, question, pool, keep=KEEP)`, where `pool` is the fused chunks, best first. It returns
at most `keep` chunks:

1. An empty pool returns `[]` without calling the model.
2. Otherwise make one call, `await client.messages.create(...)`, with `model=RERANK_MODEL`, `max_tokens=1024`,
   `system=RULES` and one user message whose content is

   ```
   Question: <the question>

   Passages:

   [0] <text of pool[0]>

   [1] <text of pool[1]>
   ```

   The passages are numbered from 0 and separated by one blank line.
3. The reply's text is `response.content[0].text`. `RULES` asks for JSON such as `{"ranked": [4, 0]}`: the numbers
   of the passages that answer the question, best first.
4. The result is the chunks the model named, in its order, each once even if it named one twice, then the rest of
   the pool in pool order, cut to `keep`. So `{"ranked": []}` gives the first `keep` of the pool.
5. Fall back to fusion order, `pool[:keep]`, when:
   - the call raises `anthropic.APIError` (every error of the SDK is one: no connection, rate limit, a 500);
   - the text is not JSON;
   - the JSON is not an object with a list under `"ranked"`;
   - an item of the list is not a whole number (`"1"` is a string, not a number);
   - a number is outside the pool: less than 0, or `len(pool)` or more. Check this yourself: Python would accept -1
     and quietly give you the last chunk.

```python
pool = [Chunk("f.txt", 1, i, f"passage {i}") for i in range(6)]
# the model replies {"ranked": [4]}
await rerank(client, "q", pool)       # [pool[4], pool[0], pool[1]]
# the model replies {"ranked": [1, 9]}
await rerank(client, "q", pool)       # [pool[0], pool[1], pool[2]]
```

The tests pass a fake client with the same `messages.create`, so no key is needed and nothing is spent.

You will use: `async def` and `await`, `json.loads`, `try` / `except` with several exception types, `isinstance`,
`dict.fromkeys` (it drops repeats and keeps the order), `str.join`, slicing.
