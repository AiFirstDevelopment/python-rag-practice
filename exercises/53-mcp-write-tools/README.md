# 53. Tools that change things

> **Your lesson:** [lessons/53-mcp-write-tools.md](../../lessons/53-mcp-write-tools.md), the worked example `/teach-me` writes for you (type `/teach-me` if the link doesn't open yet). When your code is written, type `/check`.

Documents answer questions about rules. A booking is live data, and a model must never answer about it from memory:
it reads the current record through a tool. Some tools also *change* things, and the host needs to know which ones.

Tools carry **annotations**, hints to the host about what a call does: `readOnlyHint` (it changes nothing),
`destructiveHint` (it cannot be undone, so hosts ask the user before running it) and `idempotentHint` (calling it
twice has the same effect as once, so a retry is safe). They are hints, not security: the checks that matter are in
your code.

Write `create_server(store=None)` in `solution.py`. It returns a `FastMCP` server named `"ferry-bookings"` over the
given `store` (or `sample_store()` when none is passed) with two tools:

- `get_booking(booking_id: str) -> dict`: the booking as `booking.as_dict()`. Read-only (`readOnlyHint` True).
- `cancel_booking(booking_id: str) -> dict`: sets the booking's status to `"cancelled"` in the store and returns it as
  a dict. Annotations: `readOnlyHint` False, `destructiveHint` True, `idempotentHint` True. Cancelling a booking that
  is already cancelled changes nothing and returns it, with no error.
- In both, the id is matched after stripping spaces and upper-casing (`" bk-1001 "` finds `BK-1001`), and an id with
  no booking raises a `ToolError` whose message contains `"No booking"` and the id as given, so the model can tell
  the user.

```python
async with Client(create_server()) as client:
    (await client.call_tool("get_booking", {"booking_id": "BK-1001"})).data
    # {"id": "BK-1001", "owner": "ana", "sailing": "08:00 Port Ansel to Hollow Island", "passengers": 2, "status": "confirmed"}
```

`Booking` is frozen: make the changed copy with `dataclasses.replace(booking, status="cancelled")` and put it back in
`store.bookings`.

You will use: tool annotations, `ToolError`, `dataclasses.replace`, `str.strip` and `str.upper`.
