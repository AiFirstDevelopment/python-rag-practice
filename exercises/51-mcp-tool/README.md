# 51. An MCP tool

> **Your lesson:** [lessons/51-mcp-tool.md](../../lessons/51-mcp-tool.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

MCP (the Model Context Protocol) is how an AI app such as Claude Code connects to tools and data it does not have:
the app runs an MCP *server*, asks it what it offers, and its model calls those tools when a request needs them.
This module turns your pipeline's documents into an MCP server with FastMCP, one piece per exercise.

A **tool** is chosen by the model. It sees the tool's name, its description and its parameters, and calls it when a
request fits, so the description is written for the model: what the tool is for, and what it is not for.

Write `create_server()` in `solution.py`. It returns a `FastMCP` server named `"ferry-docs"` with one tool,
`search(query: str, k: int = 3) -> dict`:

- It searches the documents with the given `keyword_search` and returns `{"passages": [...]}`, each passage a
  `{"file", "text"}` dict, at most `k` of them.
- Its description (the function's docstring) says it searches Brackwater Ferry's documents, and mentions
  "documents".
- It is marked read-only for the host: the annotation `readOnlyHint` is `True`.
- A query shorter than 2 characters (after stripping spaces) is refused with a `ToolError` whose message contains
  "at least 2 characters". A `ToolError`'s message goes back to the model, so it can fix the call.

The tests call your server the way Claude Code would, through an MCP client, in memory:

```python
async with Client(create_server()) as client:
    result = await client.call_tool("search", {"query": "How much do children pay?"})
    result.data["passages"][0]["file"]      # "fares.txt"
```

You will use: `FastMCP(name)`, the `@server.tool(annotations={...})` decorator, a docstring, `ToolError`.
