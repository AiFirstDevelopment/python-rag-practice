import json

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("solution", Path(__file__).with_name("solution.py"))
solution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(solution)

BASELINE = {"returns-01": "pass", "returns-02": "pass", "shipping-01": "pass", "warranty-01": "fail", "absent-01": "pass"}
DROPPED = {**BASELINE, "returns-02": "fail", "shipping-01": "review"}
NOISY = {**BASELINE, "returns-02": "fail"}
GAINED = {"returns-01": "pass", "returns-02": "pass", "shipping-01": "pass", "warranty-01": "pass", "absent-01": "pass"}
LOWER_BASELINE = {**GAINED, "returns-01": "fail", "returns-02": "fail"}


def write(tmp_path, name, run, blank_lines=False):
    lines = [json.dumps({"id": i, "status": s}) for i, s in run.items()]
    path = tmp_path / name
    path.write_text(("\n\n" if blank_lines else "\n").join(lines) + "\n", encoding="utf-8")
    return path


def test_load_run_reads_ids_and_statuses_and_skips_blank_lines(tmp_path):
    assert solution.load_run(write(tmp_path, "run.jsonl", BASELINE, blank_lines=True)) == BASELINE


def test_a_drop_is_exit_code_1_and_names_the_lost_cases():
    code, message = solution.gate(BASELINE, DROPPED)
    assert code == 1
    assert "drop" in message
    assert "returns-02" in message and "shipping-01" in message


def test_noise_is_exit_code_0():
    code, message = solution.gate(BASELINE, NOISY)
    assert code == 0
    assert "noise" in message


def test_a_gain_is_exit_code_0():
    code, message = solution.gate(LOWER_BASELINE, GAINED)
    assert code == 0
    assert "gain" in message


def test_the_threshold_is_passed_on():
    assert solution.gate(BASELINE, NOISY, threshold=1)[0] == 1
    assert solution.gate(BASELINE, DROPPED, threshold=3)[0] == 0


def test_main_prints_the_message_and_returns_the_code(tmp_path, capsys):
    before, after = write(tmp_path, "main.jsonl", BASELINE), write(tmp_path, "new.jsonl", DROPPED)
    assert solution.main([str(before), str(after)]) == 1
    printed = capsys.readouterr().out
    assert "drop" in printed and "returns-02" in printed and "shipping-01" in printed


def test_main_returns_0_when_nothing_dropped(tmp_path, capsys):
    before, after = write(tmp_path, "main.jsonl", BASELINE), write(tmp_path, "new.jsonl", NOISY)
    assert solution.main([str(before), str(after)]) == 0
    assert "noise" in capsys.readouterr().out


def test_main_without_two_arguments_prints_usage_and_returns_2(tmp_path, capsys):
    assert solution.main([]) == 2
    assert "usage" in capsys.readouterr().out.lower()
    assert solution.main([str(write(tmp_path, "main.jsonl", BASELINE))]) == 2
    assert "usage" in capsys.readouterr().out.lower()


def test_main_with_a_missing_file_names_it_and_returns_2(tmp_path, capsys):
    before, missing = write(tmp_path, "main.jsonl", BASELINE), tmp_path / "nowhere.jsonl"
    assert solution.main([str(before), str(missing)]) == 2
    assert "nowhere.jsonl" in capsys.readouterr().out
