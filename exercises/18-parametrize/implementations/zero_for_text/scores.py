def parse_score(text: str) -> float:
    try:
        score = float(text)
    except ValueError:
        return 0.0
    if not (0 <= score <= 1):
        raise ValueError(f"not a score: {text!r}")
    return score
