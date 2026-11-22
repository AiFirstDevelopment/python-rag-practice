# An MCP server for the pipeline

A complete MCP server, built with [FastMCP](https://gofastmcp.com), that makes a document search and a live booking
system available to Claude Code. It runs over the final project's documents (Brackwater Ferry's fares, vehicles, pets
and weather rules) and a small in-memory booking store, so it works offline with no key.

It is a worked example to read and run, not an exercise. The comments explain the reasons behind the code as much
as the code itself.

## Run it in Claude Code

From the repository root:

```bash
claude mcp add ferry -- uv run --directory "$PWD" python examples/mcp-server/server.py
claude
```

Then ask: "Can I take my dog on the ferry?" (documents), "Which sailings are delayed?" (live data), "Move my
booking BK-1002 to the last sailing today" (a write), or type `/` to see the server's prompts and `@` to attach a
document as a resource. `/mcp` in Claude Code shows the server, its tools and their status.

## Run it over HTTP

```bash
uv run python examples/mcp-server/server.py --http      # http://127.0.0.1:8000/mcp
claude mcp add --transport http ferry-http http://127.0.0.1:8000/mcp --header "Authorization: Bearer passenger-ana"
```

Two test tokens stand in for real sign-in: `passenger-ana` (her own bookings) and `staff-kim` (every booking, plus
the staff tools). A request without a token is refused.

## What it shows

| File | What is in it |
|---|---|
| `server.py` | JSON-RPC over stdio and Streamable HTTP; stateless HTTP; server instructions and where the system prompt really lives; one server per domain, mounted under a namespace; middleware for an audit log, rate limits and reply size; sign-in with a token verifier and the audience check |
| `docs_server.py` | Tools, resources and prompts, and who chooses each; a search tool whose description is written for the model; retrieval as a tool beside live-data tools; cited passages treated as data, not instructions; documents as resources with their last-modified time; cursor paging; progress on a long call |
| `bookings_server.py` | Task-shaped tools instead of one per endpoint; read and write tools kept apart, with annotations; per-user access checked in code; idempotent retries; asking the user to confirm a destructive change (on both protocol revisions); a long job that returns at once and hands its result over as a resource; a cache that trades freshness for speed; hiding tools a caller's role cannot use |
| `caller.py` | Who is calling: the verified token over HTTP, the local user over stdio; scopes checked in code |
| `documents.py` | The retrieval itself, free of MCP: BM25 search, `groupby` for sources, `islice` for paging, `batched` for re-indexing, timezone-aware `datetime` for document times and index age |
| `bookings.py` | The live records: times stored in UTC and shown in the harbour's zone with `zoneinfo` |
| `test_server.py` | Testing an MCP server through a real client: in memory for the tools, real HTTP for sign-in |

## Test it

```bash
uv run pytest examples/mcp-server
```
