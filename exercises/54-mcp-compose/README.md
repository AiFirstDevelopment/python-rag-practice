# 54. One server from two, with an audit log

> **Your lesson:** [lessons/54-mcp-compose.md](../../lessons/54-mcp-compose.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

A real system has many operations. MCP servers stay usable by splitting them by domain, each its own small server,
and **mounting** them into one under a namespace: the docs server's `search` becomes `docs_search`, the bookings
server's `get_booking` becomes `bookings_get_booking`. Each domain is built and tested alone, and similar tools from
different domains cannot be confused.

**Middleware** wraps every request, so logging, timing and limits are written once instead of in each tool. And the
server's **instructions** are sent to the host when it connects: a few lines on what the server is for, which the
host may add to its model's context.

Write two things in `solution.py`:

- `class AuditLog(Middleware)`: made with a list, `AuditLog(log)`. Its `async def on_call_tool(self, context,
  call_next)` runs the call with `await call_next(context)` and appends one line to the list per call:
  `"<tool name> ok"`, or `"<tool name> error"` when the call raised (and then the error is raised again, unchanged).
  The tool's name is `context.message.name`.
- `create_server(log=None)`: a `FastMCP` server named `"brackwater-ferry"` with the given `INSTRUCTIONS`, the given
  docs server mounted under the namespace `"docs"` and the bookings server under `"bookings"`, and an `AuditLog`
  writing to `log` (a new list when `log` is None).

```python
log = []
async with Client(create_server(log)) as client:
    await client.call_tool("docs_search", {"query": "dogs"})
log    # ["docs_search ok"]
```

You will use: `server.mount(other, namespace=...)`, a `Middleware` subclass, `server.add_middleware(...)`,
`try` / `except` / `raise`.
