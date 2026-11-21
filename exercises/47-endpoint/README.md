# 47. A FastAPI endpoint for the pipeline

A pipeline that runs from the command line answers one person at one keyboard. Behind an HTTP endpoint, a web page
or another program can ask it: one `POST /ask` with the question as JSON, the answer and its sources back as JSON.
FastAPI reads the request into a pydantic model, so a request of the wrong shape is refused before your code runs.

The pipeline is given to your code as a parameter: an async function `pipeline(question)` that returns a tuple
`(answer, sources)`, the answer's text and a list of strings such as `"returns.txt, page 1"`. `demo_pipeline` and
the error `PipelineDown` are given at the top of `solution.py`.

Write two pydantic models and one function:

- `Question` with one field, `question: str`.
- `Reply` with two fields, `answer: str` and `sources: list[str]`.
- `create_app(pipeline)` returns a `FastAPI` app with two routes:
  - `GET /health` answers 200 with `{"status": "ok"}`.
  - `POST /ask` takes a `Question` as its JSON body, awaits `pipeline(question)` and answers 200 with a `Reply`:
    `{"answer": ..., "sources": [...]}`. The pipeline gets the question with the whitespace at its ends removed.
    - A body without `question`, or one that is not a string, is answered 422 (FastAPI does this for you from the
      model).
    - A question that is empty or only whitespace is answered 422, and the pipeline is not called.
    - If the pipeline raises `PipelineDown`, the answer is 503 with `{"detail": "The pipeline is not available."}`.

```
POST /ask   {"question": "How long do I have to return an item?"}
200         {"answer": "You have 30 days from delivery.", "sources": ["returns.txt, page 1"]}

POST /ask   {"question": "   "}
422
```

The routes are defined inside `create_app`, so each call makes a separate app around the pipeline it was given;
that is what lets the tests pass a fake pipeline. To try yours by hand, add `app = create_app(demo_pipeline)` at the
bottom of the file, run `uv run fastapi dev exercises/47-endpoint/solution.py` and open
`http://localhost:8000/docs`.

You will use: `FastAPI()`, `@app.get`, `@app.post`, `async def` routes, a pydantic model as a route's parameter and
as its return value, `raise HTTPException(status_code=..., detail=...)`, `try` / `except`.
