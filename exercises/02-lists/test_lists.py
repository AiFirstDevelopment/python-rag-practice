import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

ITEMS = ["a", "b", "c", "d", "e"]


def test_middle():
    assert solution.window(ITEMS, 2, 1) == ["b", "c", "d"]


def test_start_is_clipped_not_wrapped():
    assert solution.window(ITEMS, 0, 2) == ["a", "b", "c"]


def test_end_is_clipped():
    assert solution.window(ITEMS, 4, 1) == ["d", "e"]


def test_radius_zero_is_just_the_item():
    assert solution.window(ITEMS, 3, 0) == ["d"]


def test_radius_larger_than_the_list():
    assert solution.window(ITEMS, 2, 10) == ITEMS


def test_returns_a_new_list_and_leaves_the_input_alone():
    items = list(ITEMS)
    result = solution.window(items, 2, 10)
    result.append("z")
    assert items == ITEMS
