import importlib.util
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

Chunk = solution.Chunk
A, B, C, D = (Chunk("f.txt", 1, seq, text) for seq, text in enumerate(["a", "b", "c", "d"]))


def test_scores_are_reciprocal_ranks_with_k_60():
    scores = solution.rrf_scores([[A, B, C]])
    assert scores == pytest.approx({("f.txt", 0): 1 / 61, ("f.txt", 1): 1 / 62, ("f.txt", 2): 1 / 63})


def test_scores_add_up_across_lists():
    scores = solution.rrf_scores([[A, B], [C, B]])
    assert scores[("f.txt", 1)] == pytest.approx(1 / 62 + 1 / 62)
    assert scores[("f.txt", 0)] == pytest.approx(1 / 61)
    assert ("f.txt", 3) not in scores


def test_chunks_with_the_same_seq_in_different_files_are_different_chunks():
    other = Chunk("g.txt", 1, 0, "a")
    scores = solution.rrf_scores([[A], [other]])
    assert scores == pytest.approx({("f.txt", 0): 1 / 61, ("g.txt", 0): 1 / 61})


def test_a_chunk_second_in_both_lists_beats_the_first_of_each():
    assert solution.fuse([[A, B], [C, B]], 3)[0] is B


def test_fuse_keeps_at_most_limit_and_each_chunk_once():
    fused = solution.fuse([[A, B, C], [B, A, D]], 3)
    assert len(fused) == 3
    assert fused == [A, B, C]          # A and B tie at 1/61 + 1/62, A was met first; C (1/63) ties D and was met first


def test_equal_scores_keep_the_order_first_met():
    # A and C both score 1/61, B and D both 1/62; A was met before C, B before D
    assert solution.fuse([[A, B], [C, D]], 4) == [A, C, B, D]


def test_one_list_keeps_its_order_and_none_gives_nothing():
    assert solution.fuse([[C, A, B]], 5) == [C, A, B]
    assert solution.fuse([], 5) == []
    assert solution.rrf_scores([]) == {}
