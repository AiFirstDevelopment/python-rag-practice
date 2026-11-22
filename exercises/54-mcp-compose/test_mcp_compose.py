import asyncio
import importlib.util
from pathlib import Path

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)


def run(coro):
    return asyncio.run(coro)


async def session(server, work):
    async with Client(server) as client:
        return await work(client)


def test_the_server_is_named_brackwater_ferry():
    assert solution.create_server().name == "brackwater-ferry"


def test_the_tools_are_namespaced_by_domain():
    tools = run(session(solution.create_server(), lambda c: c.list_tools()))
    assert {t.name for t in tools} == {"docs_search", "bookings_get_booking"}


def test_the_instructions_reach_the_host():
    async def work(client):
        return client.instructions
    assert run(session(solution.create_server(), work)) == solution.INSTRUCTIONS


def test_a_mounted_tool_still_works():
    result = run(session(solution.create_server(), lambda c: c.call_tool("docs_search", {"query": "dogs on board"})))
    assert result.data["passages"]
    booking = run(session(solution.create_server(), lambda c: c.call_tool("bookings_get_booking", {"booking_id": "BK-1001"})))
    assert booking.data["owner"] == "ana"


def test_every_call_is_logged_by_its_namespaced_name():
    log = []
    async def work(client):
        await client.call_tool("docs_search", {"query": "fares"})
        await client.call_tool("bookings_get_booking", {"booking_id": "BK-1001"})
    run(session(solution.create_server(log), work))
    assert log == ["docs_search ok", "bookings_get_booking ok"]


def test_a_failed_call_is_logged_and_still_fails():
    log = []
    with pytest.raises(ToolError, match="No booking"):
        run(session(solution.create_server(log), lambda c: c.call_tool("bookings_get_booking", {"booking_id": "BK-9"})))
    assert log == ["bookings_get_booking error"]


def test_listing_tools_is_not_a_call():
    log = []
    run(session(solution.create_server(log), lambda c: c.list_tools()))
    assert log == []


def test_the_audit_log_is_middleware_you_can_reuse():
    log = []
    server = solution.FastMCP("solo")
    server.tool(lambda: "pong", name="ping")
    server.add_middleware(solution.AuditLog(log))
    run(session(server, lambda c: c.call_tool("ping", {})))
    assert log == ["ping ok"]


def test_no_log_given_is_fine():
    result = run(session(solution.create_server(), lambda c: c.call_tool("docs_search", {"query": "pets"})))
    assert result.data["passages"]
