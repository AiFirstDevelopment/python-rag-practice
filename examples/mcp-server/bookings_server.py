"""Live data as MCP: today's sailings, a passenger's bookings, and the writes that change them.

How the tools are shaped:

- **Task-shaped, not one tool per endpoint.** A booking system's API might have dozens of routes. The model gets
  the handful of things a passenger or an agent actually does: see sailings, find bookings, move one, cancel one.
  `find_bookings` takes filters instead of there being a tool per query, which keeps the list short. A short list
  of distinct tools is chosen correctly more often, costs fewer tokens in every request, and is faster.
- **Reads and writes are separate tools,** with annotations that say which is which. `readOnlyHint` tells the host
  a tool changes nothing; `destructiveHint` marks one that cannot be undone, which hosts use to ask the user before
  running it. Annotations are hints to the host, not security: the checks that matter are in the code below.
- **Every call is checked against the caller** (caller.py): a passenger sees and changes only their own bookings,
  staff see all. The filter is code, so no wording in a prompt or a document can widen it.
- **Errors tell the model what to do next** ("that sailing is full; these have seats"), so it can recover in one
  more call instead of guessing.
- **Long work does not hold the connection open.** `export_manifest` starts a job and returns at once; the result
  is fetched later as a resource. A client that disconnects loses nothing, and a retry does not redo the work.
"""

import asyncio
import json
import time
import uuid
from datetime import UTC, datetime, timedelta
from typing import Annotated, Literal

from fastmcp import Context, FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.auth import require_scopes
from mcp_types import ElicitRequest, ElicitRequestFormParams, InputRequiredResult
from mcp_types.version import MODERN_PROTOCOL_VERSIONS
from pydantic import Field

import caller
from bookings import Store, sample_store
from documents import page_of

SAILINGS_TTL = 30.0     # seconds a timetable read is reused


async def ask_user(ctx: Context, key: str, question: str) -> bool | InputRequiredResult:
    """Ask the user a yes/no question through the host, on either protocol revision.

    Up to 2025-11-25 the server sends the host an elicitation request in the middle of the call and waits for the
    answer (`ctx.elicit`). From 2026-07-28 there is no server-to-client request: the tool *returns* an
    InputRequiredResult naming what it needs, the host asks the user, and the host calls the tool again with the
    answer in `input_responses`. The tool runs from the top again, so everything before the question must be safe
    to repeat (here it only reads).

    Returns True or False once the user has answered, or the InputRequiredResult to return while they have not.
    """
    request = ctx.request_context
    if request is not None and request.protocol_version in MODERN_PROTOCOL_VERSIONS:
        answers = ctx.input_responses or {}
        if key not in answers:
            schema = {"type": "object", "properties": {"confirm": {"type": "boolean", "title": "Confirm"}},
                      "required": ["confirm"]}
            return InputRequiredResult(input_requests={key: ElicitRequest(
                params=ElicitRequestFormParams(message=question, requested_schema=schema))})
        answer = answers[key]
        return answer.action == "accept" and bool((answer.content or {}).get("confirm"))
    result = await ctx.elicit(question, response_type=bool)
    return result.action == "accept" and result.data is True


def create_bookings_server(store: Store | None = None, secured: bool = False, mounted_as: str | None = None) -> FastMCP:
    """`secured` is true when the server runs over HTTP with a token verifier. Then tools a caller's token has no
    scope for are hidden from that caller altogether (`auth=require_scopes`), so a passenger's model is never shown
    staff tools at all: fewer tools in its context, and nothing to be talked into calling.

    `mounted_as` is the namespace the parent server mounts this one under. Mounting rewrites resource URIs
    (ferry://exports/x becomes ferry://bookings/exports/x), so links this server hands out must use the public form."""
    server = FastMCP("bookings")
    store = store or sample_store()
    jobs: dict[str, dict] = {}
    cache: dict[str, tuple[float, list]] = {}

    def public_uri(path: str) -> str:
        return f"ferry://{mounted_as}/{path}" if mounted_as else f"ferry://{path}"

    def scoped(scope: str):
        return require_scopes(scope) if secured else None

    def own_booking(booking_id: str):
        who = caller.current()
        booking = store.bookings.get(booking_id.strip().upper())
        # The same answer whether the booking does not exist or belongs to someone else, so ids cannot be probed.
        if booking is None or not (who.staff or booking.owner == who.user):
            raise ToolError(f"No booking {booking_id} on your account. find_bookings lists yours.")
        return who, booking

    @server.tool(annotations={"readOnlyHint": True, "openWorldHint": False})
    def sailings(
        hours_ahead: Annotated[int, Field(description="How far ahead to look, in hours.", ge=1, le=24)] = 12,
    ) -> dict:
        """Today's sailings with their live status (on time, delayed, cancelled), delay and seats left. Use this for
        anything about a sailing's time or status right now; never answer that from the documents or from memory.
        Times are given in the harbour's local time and in UTC."""
        # A short cache trades a few seconds of freshness for speed on the most common question. The trade is set
        # per kind of data: a timetable can be 30 seconds old; a booking (below) is always read fresh.
        hit = cache.get("sailings")
        if hit is None or time.monotonic() - hit[0] > SAILINGS_TTL:
            hit = (time.monotonic(), sorted(store.sailings.values(), key=lambda s: s.departs))
            cache["sailings"] = hit
        until = datetime.now(UTC) + timedelta(hours=hours_ahead)
        return {"sailings": [s.as_dict() for s in hit[1] if s.departs <= until]}

    @server.tool(annotations={"readOnlyHint": True})
    def find_bookings(
        status: Annotated[Literal["confirmed", "cancelled", "any"], Field(description="Which bookings to list.")] = "confirmed",
        sailing_id: Annotated[str | None, Field(description="Only bookings on this sailing.")] = None,
        cursor: Annotated[str | None, Field(description="next_cursor from the previous page.")] = None,
    ) -> dict:
        """The caller's bookings (every booking, for staff), filtered, a page at a time."""
        who = caller.current()
        rows = [b for b in store.visible_bookings(who.user, who.staff)
                if (status == "any" or b.status == status) and (sailing_id is None or b.sailing_id == sailing_id)]
        page, next_cursor = page_of(rows, cursor, size=25)
        return {"bookings": [b.as_dict() for b in page], "next_cursor": next_cursor}

    @server.tool(annotations={"readOnlyHint": True})
    def get_booking(booking_id: Annotated[str, Field(description="A booking id such as BK-1001.")]) -> dict:
        """One booking with its sailing's live status."""
        _, booking = own_booking(booking_id)
        return {**booking.as_dict(), "sailing": store.sailings[booking.sailing_id].as_dict()}

    @server.tool(annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": True},
                 auth=scoped(caller.WRITE))
    def move_booking(
        booking_id: Annotated[str, Field(description="The booking to move.")],
        sailing_id: Annotated[str, Field(description="The sailing to move it to, from the sailings tool.")],
        idempotency_key: Annotated[str, Field(description="Any unique string for this one change, e.g. a UUID. Send the same key when retrying the same change.", min_length=8)],
    ) -> dict:
        """Move a confirmed booking to another sailing with enough seats. Safe to retry with the same key."""
        who, booking = own_booking(booking_id)
        who.require(caller.WRITE)
        # A retried write (the client timed out, the network dropped the reply) returns the first result instead of
        # applying the change twice. The key is scoped to the user so one user cannot replay another's.
        key = f"{who.user}:{idempotency_key}"
        if key in store.applied:
            return store.applied[key]
        target = store.sailings.get(sailing_id)
        if target is None or target.status == "cancelled":
            raise ToolError(f"Sailing {sailing_id} is not available. Call sailings for the current list.")
        if booking.status != "confirmed":
            raise ToolError(f"Booking {booking.id} is {booking.status} and cannot be moved.")
        if target.seats_left < booking.passengers:
            open_ = [s.id for s in store.sailings.values() if s.seats_left >= booking.passengers and s.status != "cancelled"][:3]
            raise ToolError(f"Sailing {sailing_id} has {target.seats_left} seats left; the booking needs "
                            f"{booking.passengers}. Sailings with room: {', '.join(open_) or 'none today'}.")
        result = {"moved": store.move(booking.id, target.id).as_dict()}
        store.applied[key] = result
        return result

    @server.tool(annotations={"readOnlyHint": False, "destructiveHint": True, "idempotentHint": True},
                 auth=scoped(caller.WRITE))
    async def cancel_booking(
        booking_id: Annotated[str, Field(description="The booking to cancel.")],
        ctx: Context,
    ) -> dict:
        """Cancel a booking. This cannot be undone; the user is asked to confirm before it happens."""
        who, booking = own_booking(booking_id)
        who.require(caller.WRITE)
        if booking.status == "cancelled":
            return {"cancelled": booking.as_dict(), "note": "It was already cancelled."}
        # Elicitation: the server asks the *user*, through the host. The confirmation comes from the person, not
        # from the model, so a model that was misled by something it read cannot confirm on its own.
        try:
            answer = await ask_user(ctx, f"cancel:{booking.id}", f"Cancel booking {booking.id} ({booking.passengers} "
                                    f"on sailing {booking.sailing_id})? This cannot be undone.")
        except Exception:
            raise ToolError("This client cannot ask the user to confirm, so the booking was not cancelled. "
                            "Ask the user to cancel it on the website.") from None
        if isinstance(answer, InputRequiredResult):
            return answer
        if not answer:
            return {"cancelled": None, "note": "The user did not confirm. Nothing changed."}
        return {"cancelled": store.cancel(booking.id).as_dict()}

    @server.tool(annotations={"readOnlyHint": True}, tags={"staff"}, auth=scoped(caller.STAFF))
    async def export_manifest(sailing_id: Annotated[str, Field(description="The sailing to export.")]) -> dict:
        """Start building a sailing's passenger manifest. Returns a job id at once; call job_status with it, then
        read the resource it names. Staff only."""
        caller.current().require(caller.STAFF)
        if sailing_id not in store.sailings:
            raise ToolError(f"No sailing {sailing_id}. Call sailings for the current list.")
        job_id = uuid.uuid4().hex[:12]
        jobs[job_id] = {"status": "running", "done": 0, "total": 0, "started": datetime.now(UTC).isoformat()}

        async def build():
            rows = [b.as_dict() for b in store.bookings.values() if b.sailing_id == sailing_id and b.status == "confirmed"]
            jobs[job_id]["total"] = len(rows)
            for n, _ in enumerate(rows, start=1):
                await asyncio.sleep(0.01)       # stands in for slow work: lookups, a PDF, a large query
                jobs[job_id]["done"] = n
            jobs[job_id].update(status="done", manifest={"sailing": sailing_id, "bookings": rows})

        # The work runs after this call returns. In production it goes on a queue and its result into storage, so it
        # survives a restart and any copy of the server can answer job_status. The MCP specification also defines a
        # task mechanism for this; a job id and a status tool work with every client today.
        jobs[job_id]["task"] = asyncio.create_task(build())
        return {"job_id": job_id, "status": "running", "result_uri": public_uri(f"exports/{job_id}")}

    @server.tool(annotations={"readOnlyHint": True}, tags={"staff"}, auth=scoped(caller.STAFF))
    def job_status(job_id: str) -> dict:
        """Where an export job stands: running (with progress) or done (read its result_uri)."""
        job = jobs.get(job_id)
        if job is None:
            raise ToolError(f"No job {job_id}.")
        return {k: v for k, v in job.items() if k not in ("task", "manifest")} | {"result_uri": public_uri(f"exports/{job_id}")}

    # A resource template: one URI pattern, any number of resources. A large result is handed over as a resource
    # instead of being pasted into the tool's reply, so the model's context holds a summary and a handle, and the
    # client fetches the bulk only if it needs it.
    @server.resource("ferry://exports/{job_id}", mime_type="application/json", auth=scoped(caller.STAFF))
    def export(job_id: str) -> str:
        job = jobs.get(job_id)
        if job is None or job["status"] != "done":
            raise ToolError(f"Export {job_id} is not ready. Check job_status.")
        return json.dumps(job["manifest"], indent=2)

    @server.prompt
    def rebook_after_cancellation(booking_id: str) -> str:
        """Find a booking hit by a cancelled or delayed sailing and offer the passenger the next sailings with room."""
        return (f"Look up booking {booking_id} with get_booking. If its sailing is cancelled or delayed, use sailings "
                f"to find the next three with enough seats, use search to find what the passenger is entitled to "
                f"when the company cancels, and present the options. Move the booking only after the user picks one.")

    return server
