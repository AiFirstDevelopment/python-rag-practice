# 48. An app you can test

> **Your lesson:** [lessons/48-test-client.md](../../lessons/48-test-client.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

The real app does two things a test must not: it loads and embeds every document when it starts (slow), and it
calls a model for each question (money, and a key). FastAPI has an answer to each. Work done once at startup goes in
a `lifespan` function. Anything a route needs from outside (here, the model client) is declared with `Depends`, and
a test swaps it for a fake with `app.dependency_overrides`. `TestClient` then drives the app in memory: no server,
no network.

Given at the top of `solution.py`:

- `load_chunks()` returns the documents' chunks. Imagine it takes a minute; it counts its calls in `LOADS`.
- `get_client()` returns the model client. Here it raises: the real one needs an API key, and no test may reach it.
- `async def pipeline(question, chunks, client)` returns `(answer, sources)`, calling the model through `client`.
- `Question` and `Reply`, the request and response models.

Write `create_app()`. It returns a `FastAPI` app where:

- A `lifespan` calls `load_chunks()` once when the app starts and keeps the result (on `app.state`, for example).
  No route calls `load_chunks()`.
- `GET /health` answers 200 with `{"status": "ok", "chunks": <the number of chunks loaded>}`.
- `POST /ask` takes a `Question`, gets the model client from `Depends(get_client)` (not by calling `get_client()`
  itself), awaits `pipeline(question, chunks, client)` with the chunks loaded at startup, and answers 200 with a
  `Reply`. A body without `question` is answered 422.

```python
app = create_app()
app.dependency_overrides[get_client] = lambda: fake_client     # the test's swap

with TestClient(app) as client:          # "with" runs the lifespan: startup on entry, shutdown on exit
    client.get("/health").json()         # {"status": "ok", "chunks": 3}
    client.post("/ask", json={"question": "Can I return a sale item?"}).json()
    # {"answer": "...", "sources": ["returns.txt, page 1", ...]}
```

The two FastAPI shapes this needs, on other names:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.prices = read_prices()     # runs once, when the app starts
    yield                                # the app serves requests while the function waits here
    # anything after yield runs once, when the app stops


app = FastAPI(lifespan=lifespan)


@app.get("/price")
async def price(db=Depends(get_db)):     # FastAPI calls get_db() for each request and passes the result in
    ...
```

Read `test_test_client.py` after you pass: it is the shape of the tests you will write for your own service.

You will use: `@asynccontextmanager` and `FastAPI(lifespan=...)`, `yield`, `app.state`, `Depends`, `async def`
routes, a pydantic model as a route's parameter and return value.
