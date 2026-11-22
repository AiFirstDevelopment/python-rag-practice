# 50. Final project: a pipeline over new documents

> **Your lesson:** [lessons/50-final-project.md](../../lessons/50-final-project.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

Everything so far was one function at a time, with a starter. Here there is none. You build the pipeline of module
7 over a set of documents you have not seen, and the golden set of module 8 says whether it works. This is the job
as it arrives in practice: a folder of documents, a list of questions, and nothing else.

## What you are given

- `corpus/`: four text files about a ferry company (`fares.txt`, `vehicles.txt`, `onboard.txt`,
  `disruptions.txt`), about 7,000 characters together. A file has several pages; a line that is exactly
  `--- page break ---` ends one page and starts the next. The first page is page 1.
- `golden.jsonl`: ten cases in the format of exercise 40. Eight expect an answer, two expect "I don't know".
- `test_final_project.py`: runs every case through your pipeline and scores it by the rules of exercise 43.

## What to write

Create `pipeline.py` in this folder with one entry point:

```python
async def answer(question: str, client, embed) -> str:
```

It returns the model's reply to `question` as a string, answered from the corpus. Everything else in the file is
your design: copy your own functions from modules 7 and 8, or write them again.

- **The corpus** is read from the `corpus` folder beside your file (`Path(__file__).parent / "corpus"`), not from
  the current directory.
- **`embed`** is a function: `embed(texts)` takes a list of strings and returns a numpy array with one row per
  text, each row a vector of length 1 (a row of zeros for a text with no words). Use it for the vector search. The
  tests pass a small fake that needs no download.
- **`client`** is used like `AsyncAnthropic`: `response = await client.messages.create(model=..., max_tokens=...,
  system=..., messages=[{"role": "user", "content": ...}])`, and the reply is `response.content[0].text`. `system`
  and each message's `content` are plain strings.

The pipeline, as in module 7: split each file into pages, cut the pages into chunks at sentence ends, keep the file
and page with each chunk, search by keyword (BM25) and by vector, fuse the two rankings (reciprocal rank fusion, k =
60), and give the best chunks to the model as passages with the question. There is no reranking step here.

## The rules the tests hold you to

The tests use a fake model. It is strict in the ways a real one is costly or unreliable:

1. **One model call per question.** No reranker, no second try.
2. **The prompt has a budget.** The system prompt and the user message together may be at most 3,500 characters,
   about half the corpus; over that the fake raises `ValueError`. You cannot send every document: retrieval has to
   pick.
3. **The question goes in the user message, word for word,** with the passages.
4. **The fake answers only from what it was sent.** For each case it knows the one sentence of the corpus that
   answers the question. If that sentence is in your prompt, whole and unchanged apart from spacing and line breaks,
   it replies with it. If not, your retrieval missed (or a chunk cut the sentence in two), and the case fails.
5. **It falls back only if told to.** When it cannot answer and your system prompt tells it to say it doesn't know
   (the words "don't know" or "do not know" must be in the system prompt), it replies "I don't know." Without that
   instruction it makes an answer up, as a model would, and the two fallback cases do not pass.

A case passes as in exercise 43: an answer case when the reply holds every required fact, a fallback case when the
reply says it doesn't know.

## An example

```python
reply = await answer("How long do you keep lost property?", client, embed)
# "Lost property is kept at the Port Ansel ticket office for 30 days."

reply = await answer("Is there a cabin where I can sleep during the crossing?", client, embed)
# "I don't know."
```

## Working on it

Run `uv run pytest exercises/50-final-project` (or `/check`). Each golden case is its own test, named by the case id, so
a failure tells you which question, and the message shows the reply and the missing facts. When a case fails, find
out which half is wrong before changing anything: print the chunks your search returned for that question and look
for the sentence that answers it. A harness of your own from module 8 (`harness.py`, beside `pipeline.py`) that
prints retrieval per case is worth the ten minutes; the tests do not need it.

You will use: everything from modules 1 to 8.
