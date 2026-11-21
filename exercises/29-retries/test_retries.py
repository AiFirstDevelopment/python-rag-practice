import asyncio

import pytest

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

class Flaky:
    """A call that raises the errors it is given, one per call, then returns "ok"."""

    def __init__(self, errors):
        self.errors = list(errors)
        self.calls = 0

    async def __call__(self):
        self.calls += 1
        if self.errors:
            raise self.errors.pop(0)
        return "ok"


class Sleeper:
    """Passed as sleep: records the seconds asked for and returns at once."""

    def __init__(self):
        self.waits = []

    async def __call__(self, seconds):
        self.waits.append(seconds)


def test_backoff_doubles_from_the_base():
    assert [solution.backoff(n) for n in range(4)] == [1.0, 2.0, 4.0, 8.0]
    assert solution.backoff(2, base=0.5) == 2.0


def test_backoff_never_exceeds_the_cap():
    assert solution.backoff(10) == 30.0
    assert solution.backoff(3, base=1.0, cap=5.0) == 5.0


def test_a_call_that_works_is_made_once_with_no_sleep():
    call, sleep = Flaky([]), Sleeper()
    assert asyncio.run(solution.with_retries(call, sleep=sleep)) == "ok"
    assert call.calls == 1
    assert sleep.waits == []


def test_rate_limited_calls_are_retried_with_growing_waits():
    call, sleep = Flaky([solution.RateLimited(), solution.RateLimited()]), Sleeper()
    assert asyncio.run(solution.with_retries(call, sleep=sleep)) == "ok"
    assert call.calls == 3
    assert sleep.waits == [1.0, 2.0]


def test_base_and_cap_are_passed_on_to_the_waits():
    call, sleep = Flaky([solution.RateLimited()] * 3), Sleeper()
    assert asyncio.run(solution.with_retries(call, retries=3, sleep=sleep, base=2.0, cap=5.0)) == "ok"
    assert sleep.waits == [2.0, 4.0, 5.0]


def test_it_gives_up_after_the_retries_and_raises_rate_limited():
    call, sleep = Flaky([solution.RateLimited()] * 10), Sleeper()
    with pytest.raises(solution.RateLimited):
        asyncio.run(solution.with_retries(call, retries=2, sleep=sleep))
    assert call.calls == 3
    assert sleep.waits == [1.0, 2.0]


def test_no_retries_means_one_call():
    call, sleep = Flaky([solution.RateLimited()]), Sleeper()
    with pytest.raises(solution.RateLimited):
        asyncio.run(solution.with_retries(call, retries=0, sleep=sleep))
    assert call.calls == 1
    assert sleep.waits == []


def test_any_other_error_is_not_retried():
    call, sleep = Flaky([KeyError("content")]), Sleeper()
    with pytest.raises(KeyError):
        asyncio.run(solution.with_retries(call, sleep=sleep))
    assert call.calls == 1
    assert sleep.waits == []
