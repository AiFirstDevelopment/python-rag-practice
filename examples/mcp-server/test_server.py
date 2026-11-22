"""The server tested the way a host uses it: through an MCP client, in memory, with no subprocess and no network,
except the sign-in tests at the end, which serve real HTTP on a free port."""

import asyncio
import json
import socket
import threading
import time

import pytest
import uvicorn
from fastmcp import Client
from fastmcp.exceptions import ToolError

from server import create_server, http_auth


def client(**handlers):
    return Client(create_server(), **handlers)


async def test_every_tool_is_namespaced_and_writes_are_marked():
    async with client() as c:
        tools = {t.name: t for t in await c.list_tools()}
    assert {"docs_search", "docs_list_documents", "bookings_sailings", "bookings_move_booking"} <= set(tools)
    assert tools["docs_search"].annotations.read_only_hint is True
    assert tools["bookings_cancel_booking"].annotations.destructive_hint is True
    assert "live" in tools["docs_search"].description or "sailings" in tools["docs_search"].description


async def test_search_returns_cited_passages_grouped_by_document():
    async with client() as c:
        result = (await c.call_tool("docs_search", {"query": "How much do children pay?"})).data
    assert result["passages"][0]["file"] == "fares.txt"
    assert "half the adult fare" in " ".join(result["passages"][0]["text"].split())
    assert {"file": "fares.txt", "pages": [1]} in result["sources"]


async def test_list_documents_pages_and_refuses_a_bad_date():
    async with client() as c:
        first = (await c.call_tool("docs_list_documents", {})).data
        assert len(first["documents"]) == 4 and first["next_cursor"] is None
        listed = (await c.read_resource(first["documents"][0]["uri"]))[0].text
        assert listed.startswith("Brackwater Ferry")
        later = (await c.call_tool("docs_list_documents", {"changed_since": "2999-01-01"})).data
        assert later["documents"] == []
        with pytest.raises(ToolError, match="ISO 8601"):
            await c.call_tool("docs_list_documents", {"changed_since": "last Tuesday"})


async def test_documents_are_resources_with_their_last_change():
    async with client() as c:
        resources = {str(r.uri): r for r in await c.list_resources()}
        fares = next(r for uri, r in resources.items() if uri.endswith("fares.txt"))
        assert fares.annotations.last_modified
        text = (await c.read_resource(fares.uri))[0].text
    assert text.startswith("Brackwater Ferry: fares and tickets")


async def test_prompts_are_listed_for_the_user():
    async with client() as c:
        names = {p.name for p in await c.list_prompts()}
    assert {"docs_answer_from_documents", "bookings_rebook_after_cancellation"} <= names


async def test_a_passenger_sees_only_their_own_bookings():
    async with client() as c:
        mine = (await c.call_tool("bookings_find_bookings", {})).data["bookings"]
        assert {b["id"] for b in mine} == {"BK-1001", "BK-1002"}
        with pytest.raises(ToolError, match="No booking BK-1003 on your account"):
            await c.call_tool("bookings_get_booking", {"booking_id": "BK-1003"})


async def test_a_retried_move_is_applied_once():
    async with client() as c:
        sailings = (await c.call_tool("bookings_sailings", {})).data["sailings"]
        target = sailings[-1]["id"]
        args = {"booking_id": "BK-1002", "sailing_id": target, "idempotency_key": "move-0001"}
        first = (await c.call_tool("bookings_move_booking", args)).data
        again = (await c.call_tool("bookings_move_booking", args)).data
    assert first == again and first["moved"]["sailing_id"] == target


async def test_cancel_asks_the_user_and_respects_the_answer():
    async def decline(message, response_type, params, context):
        from fastmcp.client.elicitation import ElicitResult
        return ElicitResult(action="decline")

    async def accept(message, response_type, params, context):
        return response_type(confirm=True)

    async with client(elicitation_handler=decline) as c:
        kept = (await c.call_tool("bookings_cancel_booking", {"booking_id": "BK-1001"})).data
    assert kept["cancelled"] is None
    async with client(elicitation_handler=accept) as c:
        gone = (await c.call_tool("bookings_cancel_booking", {"booking_id": "BK-1001"})).data
    assert gone["cancelled"]["status"] == "cancelled"


async def test_a_long_export_returns_a_job_and_its_result_is_a_resource(monkeypatch):
    monkeypatch.setenv("FERRY_STAFF", "1")
    async with client() as c:
        sailing = (await c.call_tool("bookings_find_bookings", {})).data["bookings"][0]["sailing_id"]
        job = (await c.call_tool("bookings_export_manifest", {"sailing_id": sailing})).data
        assert job["status"] == "running"
        for _ in range(100):
            status = (await c.call_tool("bookings_job_status", {"job_id": job["job_id"]})).data
            if status["status"] == "done":
                break
            await asyncio.sleep(0.02)
        manifest = json.loads((await c.read_resource(job["result_uri"]))[0].text)
    assert manifest["sailing"] == sailing and manifest["bookings"]


async def test_rebuilding_the_index_reports_progress(monkeypatch):
    monkeypatch.setenv("FERRY_STAFF", "1")
    seen = []

    async def progress(done, total, message):
        seen.append((done, total))

    async with client(progress_handler=progress) as c:
        result = (await c.call_tool("docs_rebuild_index", {})).data
    assert seen and seen[-1] == (result["pages"], result["pages"])


async def test_a_passenger_deployment_hides_staff_tools():
    async with Client(create_server(staff_tools=False)) as c:
        names = {t.name for t in await c.list_tools()}
    assert "bookings_export_manifest" not in names and "docs_rebuild_index" not in names
    assert "bookings_find_bookings" in names


@pytest.fixture(scope="module")
def http_url():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    app = create_server(auth=http_auth()).http_app(stateless_http=True)
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    while not server.started:
        time.sleep(0.05)
    yield f"http://127.0.0.1:{port}/mcp"
    server.should_exit = True
    thread.join(5)


async def test_over_http_a_call_without_a_token_is_refused(http_url):
    with pytest.raises(Exception):
        async with Client(http_url) as c:
            await c.list_tools()


async def test_over_http_each_caller_sees_what_their_token_allows(http_url):
    async with Client(http_url, auth="passenger-ana") as c:
        passenger = {t.name for t in await c.list_tools()}
        mine = (await c.call_tool("bookings_find_bookings", {"status": "any"})).data["bookings"]
    async with Client(http_url, auth="staff-kim") as c:
        staff = {t.name for t in await c.list_tools()}
        everyone = (await c.call_tool("bookings_find_bookings", {"status": "any"})).data["bookings"]
    assert "bookings_export_manifest" not in passenger and "bookings_export_manifest" in staff
    assert {b["id"] for b in mine} == {"BK-1001", "BK-1002"}
    assert "BK-1003" in {b["id"] for b in everyone}
