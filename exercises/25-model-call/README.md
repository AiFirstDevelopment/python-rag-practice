# 25. A first model call and its token counts

The last step of a RAG pipeline sends the question and the passages to a model and reads the reply. Every call is
billed by tokens (pieces of words): the ones you send and the ones that come back, at different prices. A pipeline
that does not count them cannot say what an answer costs.

The Anthropic SDK's call is `client.messages.create(model=..., max_tokens=..., messages=[...])`. The response has
the reply's text at `response.content[0].text` and the counts at `response.usage.input_tokens` and
`response.usage.output_tokens`. Your functions take the client as a parameter, so the tests can pass a fake one: no
key, no network, no cost.

`MODEL` and the `Reply` dataclass are given at the top of `solution.py`. Write three functions:

- `ask(client, question, model=MODEL, max_tokens=1024)` makes one call with these keyword arguments: `model`,
  `max_tokens`, and `messages` as a list holding one message, `{"role": "user", "content": question}`. It returns a
  `Reply` with the text and the two token counts.
- `cost(input_tokens, output_tokens, input_price, output_price)` returns the dollars one call cost. The prices are
  dollars per million tokens, as providers list them.
- `total_cost(replies, input_price, output_price)` returns the dollars for a list of `Reply`; `0.0` for an empty
  list.

```python
reply = ask(client, "How long do I have to return an item?")
reply.text                         # "30 days from delivery."
reply.input_tokens                 # 18
cost(1_000_000, 0, 5.0, 25.0)      # 5.0
cost(2_000, 500, 5.0, 25.0)        # 0.0225    (2,000 x $5 + 500 x $25) / 1,000,000
```

The prices in the examples are made up; a model's real prices are on its provider's pricing page.

You will use: keyword arguments, a list of dicts, attribute access (`response.usage.input_tokens`), a dataclass,
`sum` with a generator.
