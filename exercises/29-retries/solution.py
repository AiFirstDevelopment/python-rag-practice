import asyncio

# ---- Given. Do not change. ----


class RateLimited(Exception):
    """Stands in for the SDK's "too many requests" error: the one worth retrying."""


# ---- Yours ----

def backoff(attempt: int, base: float = 1.0, cap: float = 30.0) -> float:
    raise NotImplementedError


async def with_retries(call, retries: int = 3, sleep=asyncio.sleep, base: float = 1.0, cap: float = 30.0):
    raise NotImplementedError
