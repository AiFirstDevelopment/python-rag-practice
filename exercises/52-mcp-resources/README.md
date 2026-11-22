# 52. Resources and prompts

> **Your lesson:** [lessons/52-mcp-resources.md](../../lessons/52-mcp-resources.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

A tool is chosen by the model. MCP has two other kinds of component, chosen by someone else:

- A **resource** is chosen by the app or the user: read-only content with a URI, which the host lists and can attach
  to the conversation (in Claude Code, typing `@` and picking it). Nothing runs on the model's initiative.
- A **prompt** is chosen by the user: a template with arguments, which Claude Code shows as a slash command.

Write `create_server()` in `solution.py`. It returns a `FastMCP` server named `"ferry-docs"` with:

- one resource per document, at the URI `ferry://documents/<file name>` (for example `ferry://documents/fares.txt`),
  named after the file, with the MIME type `text/plain`, whose content is the document's full text;
- a resource `ferry://documents` (MIME type `application/json`) whose content is a JSON list of the file names,
  sorted: `["disruptions.txt", "fares.txt", ...]`;
- a prompt `answer_from_documents(question: str)` that returns the text the user's model is sent: it must contain
  the question, and tell the model to answer from the documents only and to cite the file.

```python
async with Client(create_server()) as client:
    (await client.read_resource("ferry://documents/fares.txt"))[0].text   # "Brackwater Ferry: fares and tickets ..."
    await client.get_prompt("answer_from_documents", {"question": "Can I bring my dog?"})
```

A resource function takes no arguments when its URI is fixed. To register one per document in a loop, call
`server.resource(uri, name=..., mime_type=...)` on a function made for that document.

You will use: `server.resource(...)`, `@server.prompt`, `json.dumps`, a closure (a function that returns a function).
