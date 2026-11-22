# Your task is in README.md in this folder. The code at the top is given; yours goes under "Yours" at line 37.
# Each EXERCISE-TODO comment below is one piece to write. Save, then type /check in the Claude chat.
from dataclasses import asdict, dataclass, field, replace

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

# ---- Given: the live booking records. Do not change. ----


@dataclass(frozen=True)
class Booking:
    id: str
    owner: str
    sailing: str
    passengers: int
    status: str = "confirmed"      # "confirmed" or "cancelled"

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class Store:
    bookings: dict[str, Booking] = field(default_factory=dict)


def sample_store() -> Store:
    rows = [
        Booking("BK-1001", "ana", "08:00 Port Ansel to Hollow Island", 2),
        Booking("BK-1002", "ana", "17:30 Hollow Island to Port Ansel", 1),
        Booking("BK-1003", "raj", "12:00 Port Ansel to Hollow Island", 4, status="cancelled"),
    ]
    return Store({b.id: b for b in rows})


# ---- Yours ----

# EXERCISE-TODO: create_server(store=None): return a FastMCP server named "ferry-bookings" over store (or
# sample_store() when store is None) with two tools:
# - get_booking(booking_id: str) -> dict: the booking's as_dict(). Annotation readOnlyHint True.
# - cancel_booking(booking_id: str) -> dict: set its status to "cancelled" in store.bookings and return its as_dict().
#   Annotations readOnlyHint False, destructiveHint True, idempotentHint True. Already cancelled: no change, no error.
# Both match the id after strip() and upper(); an unknown id raises ToolError with "No booking" and the id as given.
#   get_booking(booking_id=" bk-1001 ")  ->  {"id": "BK-1001", "owner": "ana", ..., "status": "confirmed"}
#   cancel_booking(booking_id="BK-1001")  ->  {"id": "BK-1001", ..., "status": "cancelled"}
#   get_booking(booking_id="BK-9")        ->  ToolError: "No booking BK-9 ..."
def create_server(store: Store | None = None) -> FastMCP:
    raise NotImplementedError
