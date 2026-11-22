"""Brackwater Ferry's MCP server: the documents and the live bookings in one server for Claude Code.

    uv run python examples/mcp-server/server.py            # stdio: Claude Code starts it as a subprocess
    uv run python examples/mcp-server/server.py --http     # Streamable HTTP on http://127.0.0.1:8000/mcp

What travels between Claude Code and this server is JSON-RPC 2.0: `initialize` (the two sides agree on a protocol
version and say what they support), then requests such as `tools/list`, `tools/call`, `resources/read`, each
answered with a result or an error. Two standard transports carry it:

- **stdio**: the host launches the server as a child process and exchanges messages over its stdin and stdout.
  Local, one user, nothing to deploy. Never print to stdout in a stdio server: stdout *is* the protocol.
- **Streamable HTTP**: each message is an HTTP POST to one endpoint. The server answers with JSON, or opens a
  Server-Sent Events stream when it has several messages to send (progress, then the result). One deployed server
  serves many users, which is when sign-in (below) matters.

The protocol is the same either way; the tools never know which transport carried the call.
"""

import argparse
import logging
import os
import sys
import time

from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
from fastmcp.server.middleware.response_limiting import ResponseLimitingMiddleware

import caller
from bookings_server import create_bookings_server
from docs_server import create_docs_server

log = logging.getLogger("ferry")

# Sent to the host in the initialize result. The host may add it to its model's context, but the system prompt
# itself belongs to the host (Claude Code, an IDE, an agent): the server never sees the conversation and cannot
# set the system prompt. It can only shape behaviour through this text, its tool descriptions, and its prompts.
INSTRUCTIONS = """Brackwater Ferry: its published rules (search) and live sailings and bookings (bookings tools).
Rules and prices come from search, cited by file and page. A sailing's status or a booking comes from the live
tools, never from the documents or from memory. Ask the user before changing a booking."""


class AuditLog(Middleware):
    """One line per call: who, what, how long, whether it failed.

    Middleware wraps every request, so logging, timing, limits and checks are written once instead of in each tool.
    The user is in every line, the same identity the tools used, which is what an audit needs. Logs go to stderr:
    over stdio, stdout belongs to the protocol.
    """

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        start, who, outcome = time.perf_counter(), caller.current().user, "ok"
        try:
            return await call_next(context)
        except Exception as error:
            outcome = f"error: {error}"
            raise
        finally:
            log.info("user=%s tool=%s ms=%.0f %s", who, context.message.name, (time.perf_counter() - start) * 1000, outcome)


def create_server(auth=None, staff_tools: bool = True) -> FastMCP:
    server = FastMCP("brackwater-ferry", instructions=INSTRUCTIONS, auth=auth)

    # Each domain is its own server, mounted under a namespace: tools become docs_search, bookings_move_booking and
    # so on. Namespaces keep similar tools from different domains distinct, each domain can be built and tested on
    # its own, and a host that only needs one domain can connect to that server alone. This is how a system with
    # hundreds of operations stays usable: split by domain, keep each domain's tools few, show each caller only what
    # their job needs.
    server.mount(create_docs_server(mounted_as="docs"), namespace="docs")
    server.mount(create_bookings_server(secured=auth is not None, mounted_as="bookings"), namespace="bookings")

    # Tags select components by role. A passenger-facing deployment hides staff tools from the list entirely, so
    # the model never sees them (scope checks in the tools still refuse a call that gets through anyway).
    if not staff_tools:
        server.disable(tags={"staff"})

    # Order matters: the first middleware added is the outermost.
    server.add_middleware(AuditLog())
    # Caps protect cost and the systems behind the tools from a model stuck in a loop or a client gone wrong.
    server.add_middleware(RateLimitingMiddleware(max_requests_per_second=5, burst_capacity=20))
    # A tool reply goes into the model's context. Cap it, so one oversized reply cannot crowd out the conversation.
    server.add_middleware(ResponseLimitingMiddleware(max_size=50_000))
    return server


def http_auth():
    """The token verifier for HTTP.

    In production this is a JWTVerifier pointed at the identity provider:

        JWTVerifier(jwks_uri="https://login.example.com/.well-known/jwks.json",
                    issuer="https://login.example.com/", audience="https://ferry.example.com/mcp")

    `audience` is what stops a token issued for another API being replayed here. For trying the server locally,
    two fixed tokens stand in for a passenger and a staff member.
    """
    from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

    return StaticTokenVerifier(tokens={
        os.environ.get("FERRY_PASSENGER_TOKEN", "passenger-ana"): {
            "client_id": "ana", "sub": "ana", "scopes": [caller.READ, caller.WRITE]},
        os.environ.get("FERRY_STAFF_TOKEN", "staff-kim"): {
            "client_id": "kim", "sub": "kim", "scopes": [caller.READ, caller.WRITE, caller.STAFF]},
    })


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--http", action="store_true", help="serve Streamable HTTP instead of stdio")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(asctime)s %(name)s %(message)s")

    if args.http:
        # stateless_http: no session is kept between requests. Each POST carries its token and everything the call
        # needs, so any copy of the server can answer any request, copies can be added or replaced freely, and a
        # crash loses nothing. The trade-off is that features which need a held session are not available.
        create_server(auth=http_auth()).run(transport="http", host="127.0.0.1", port=args.port, stateless_http=True)
    else:
        create_server().run(show_banner=False)


if __name__ == "__main__":
    main()
