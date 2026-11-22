# Your task is in README.md in this folder. Write your code here, save, then type /check in the Claude chat.
import asyncio

# ---- Given. Do not change. ----


class RateLimited(Exception):
    """Stands in for the SDK's "too many requests" error: the one worth retrying."""


# ---- Yours ----

# backoff(attempt, base, cap): return the seconds to wait after failed attempt number attempt, counted from 0: base
# doubled attempt times, and never more than cap.
#   backoff(0)   ->  1.0
#   backoff(10)  ->  30.0   capped
def backoff(attempt: int, base: float = 1.0, cap: float = 30.0) -> float:
    raise NotImplementedError


# with_retries(call, retries, sleep, base, cap): call takes no arguments and returns something to await. Await
# call() and return its result. If it raises RateLimited, await sleep(backoff(attempt, base, cap)) and call it again,
# at most retries more times (retries=3 means up to 4 calls and 3 sleeps). When the last allowed call also raises
# RateLimited, let that error out, without sleeping after it. Any other exception goes straight out: no sleep, no
# second call.
#   RateLimited twice, then a reply  ->  the reply; three calls, sleeps of 1.0 and 2.0 seconds
async def with_retries(call, retries: int = 3, sleep=asyncio.sleep, base: float = 1.0, cap: float = 30.0):
    raise NotImplementedError
