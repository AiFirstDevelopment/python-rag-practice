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


async def tools():
    async with Client(solution.create_server()) as client:
        return {t.name: t for t in await client.list_tools()}


async def call(args):
    async with Client(solution.create_server()) as client:
        return (await client.call_tool("search", args)).data


def test_the_server_is_named_ferry_docs():
    assert solution.create_server().name == "ferry-docs"


def test_it_offers_one_tool_named_search():
    assert set(run(tools())) == {"search"}


def test_the_description_tells_the_model_what_it_searches():
    description = run(tools())["search"].description or ""
    assert "documents" in description.lower()


def test_search_is_marked_read_only():
    annotations = run(tools())["search"].annotations
    assert annotations is not None and annotations.read_only_hint is True


def test_k_defaults_to_3():
    schema = run(tools())["search"].input_schema
    assert schema["properties"]["k"].get("default") == 3
    assert schema["required"] == ["query"]


def test_search_returns_passages_with_their_file():
    result = run(call({"query": "How much do children pay?"}))
    assert result["passages"][0]["file"] == "fares.txt"
    assert "half the adult fare" in result["passages"][0]["text"]
    assert len(result["passages"]) <= 3


def test_k_limits_the_passages():
    assert len(run(call({"query": "ferry dog bicycle fare", "k": 1}))["passages"]) == 1
    assert len(run(call({"query": "ferry dog bicycle fare", "k": 5}))["passages"]) == 5


def test_a_query_too_short_is_refused_with_a_message_for_the_model():
    with pytest.raises(ToolError, match="at least 2 characters"):
        run(call({"query": " a "}))
