def parse_score(text: str) -> float:
    try:
        score = float(text)
    except ValueError:
        raise ValueError(f"not a score: {text!r}") from None
    if not (0 <= score):
        raise ValueError(f"not a score: {text!r}")
    return score
