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


async def calls(server, *steps):
    async with Client(server) as client:
        return [(await client.call_tool(name, args)).data for name, args in steps]


def tools():
    async def work():
        async with Client(solution.create_server()) as client:
            return {t.name: t for t in await client.list_tools()}
    return run(work())


def test_the_server_is_named_ferry_bookings():
    assert solution.create_server().name == "ferry-bookings"


def test_it_offers_the_two_tools():
    assert set(tools()) == {"get_booking", "cancel_booking"}


def test_get_booking_is_read_only():
    assert tools()["get_booking"].annotations.read_only_hint is True


def test_cancel_booking_is_marked_destructive_and_idempotent():
    a = tools()["cancel_booking"].annotations
    assert a.read_only_hint is False
    assert a.destructive_hint is True
    assert a.idempotent_hint is True


def test_get_booking_returns_the_record():
    [booking] = run(calls(solution.create_server(), ("get_booking", {"booking_id": "BK-1001"})))
    assert booking == solution.sample_store().bookings["BK-1001"].as_dict()


def test_the_id_is_matched_after_strip_and_upper():
    [booking] = run(calls(solution.create_server(), ("get_booking", {"booking_id": "  bk-1002 "})))
    assert booking["id"] == "BK-1002"


def test_cancel_changes_the_store_and_returns_the_booking():
    store = solution.sample_store()
    cancelled, after = run(calls(solution.create_server(store),
                                 ("cancel_booking", {"booking_id": "BK-1001"}),
                                 ("get_booking", {"booking_id": "BK-1001"})))
    assert cancelled["status"] == "cancelled" and after["status"] == "cancelled"
    assert store.bookings["BK-1001"].status == "cancelled"
    assert store.bookings["BK-1002"].status == "confirmed"


def test_cancelling_twice_is_safe():
    store = solution.sample_store()
    first, second = run(calls(solution.create_server(store),
                              ("cancel_booking", {"booking_id": "BK-1002"}),
                              ("cancel_booking", {"booking_id": "BK-1002"})))
    assert first == second
    assert second["status"] == "cancelled"


def test_an_already_cancelled_booking_is_returned_unchanged():
    store = solution.sample_store()
    before = store.bookings["BK-1003"]
    [result] = run(calls(solution.create_server(store), ("cancel_booking", {"booking_id": "BK-1003"})))
    assert result == before.as_dict()


def test_an_unknown_id_is_refused_with_a_message_for_the_model():
    with pytest.raises(ToolError, match="No booking BK-9"):
        run(calls(solution.create_server(), ("get_booking", {"booking_id": "BK-9"})))
    with pytest.raises(ToolError, match="No booking"):
        run(calls(solution.create_server(), ("cancel_booking", {"booking_id": "nope"})))


def test_each_server_uses_the_store_it_was_given():
    store = solution.Store({"X-1": solution.Booking("X-1", "kim", "09:00", 1)})
    [booking] = run(calls(solution.create_server(store), ("get_booking", {"booking_id": "x-1"})))
    assert booking["owner"] == "kim"
