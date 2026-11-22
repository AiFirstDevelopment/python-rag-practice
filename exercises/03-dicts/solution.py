# Your task is in README.md. Each EXERCISE-TODO comment below is one piece to write.
# Save, then type /check in the Claude chat.

# EXERCISE-TODO: count_by(records, key): each record is a dict; return a dict from each value of record[key] to how many
# records have it. A record without that key is counted under None.
#   count_by(runs, "category")  ->  {"absent": 1, "answerable": 2}
#   (runs = [{"category": "absent", "result": "pass"}, {"category": "answerable", "result": "fail"},
#            {"category": "answerable", "result": "pass"}])
def count_by(records: list[dict], key: str) -> dict:
    raise NotImplementedError


# EXERCISE-TODO: pass_rate(records): return the share of records whose "result" is "pass", as a float from 0 to 1,
# rounded to 2 places. An empty list gives 0.0.
#   pass_rate(runs)  ->  0.67   (runs as above)
def pass_rate(records: list[dict]) -> float:
    raise NotImplementedError
