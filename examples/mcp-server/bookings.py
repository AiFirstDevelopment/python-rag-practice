"""The live side of the server: today's sailings and passengers' bookings.

This is the kind of data a document index must never answer from. A sailing's delay or a booking's seat changes
by the minute, and a model asked about either from memory or from a policy page will produce something plausible
and wrong. It lives behind tools that read the current record each time.

The store is an in-memory dict so the example runs anywhere. In production it is a database, and that matters
for scaling: the server keeps no state of its own between requests, so any number of copies can run behind a load
balancer and any one of them can serve any call.
"""

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

HARBOUR = ZoneInfo("America/Halifax")   # times are stored in UTC and shown in the harbour's own zone


@dataclass(frozen=True)
class Sailing:
    id: str
    departs: datetime           # aware, UTC
    route: str
    status: str = "on time"     # "on time", "delayed", "cancelled"
    delay_minutes: int = 0
    seats_left: int = 120

    def as_dict(self) -> dict:
        local = self.departs.astimezone(HARBOUR)
        return {"id": self.id, "route": self.route, "departs_local": local.strftime("%a %d %b %H:%M %Z"),
                "departs_utc": self.departs.isoformat(), "status": self.status,
                "delay_minutes": self.delay_minutes, "seats_left": self.seats_left}


@dataclass(frozen=True)
class Booking:
    id: str
    owner: str                  # the user the booking belongs to; every read and write is checked against it
    sailing_id: str
    passengers: int
    vehicle: str | None = None
    status: str = "confirmed"   # "confirmed", "cancelled"

    def as_dict(self) -> dict:
        return {"id": self.id, "sailing_id": self.sailing_id, "passengers": self.passengers,
                "vehicle": self.vehicle, "status": self.status}


@dataclass
class Store:
    sailings: dict[str, Sailing] = field(default_factory=dict)
    bookings: dict[str, Booking] = field(default_factory=dict)
    # Results of writes already applied, by idempotency key. A client that times out and retries the same move
    # gets the first result back instead of a second change.
    applied: dict[str, dict] = field(default_factory=dict)

    def visible_bookings(self, user: str, staff: bool) -> list[Booking]:
        """Bookings this caller may see: their own, or every one for staff. Filtering happens here, in code,
        never by asking the model to leave other people's records out."""
        return [b for b in self.bookings.values() if staff or b.owner == user]

    def move(self, booking_id: str, sailing_id: str) -> Booking:
        booking, sailing = self.bookings[booking_id], self.sailings[sailing_id]
        old = self.sailings[booking.sailing_id]
        self.sailings[old.id] = replace(old, seats_left=old.seats_left + booking.passengers)
        self.sailings[sailing.id] = replace(sailing, seats_left=sailing.seats_left - booking.passengers)
        self.bookings[booking_id] = replace(booking, sailing_id=sailing_id)
        return self.bookings[booking_id]

    def cancel(self, booking_id: str) -> Booking:
        booking = self.bookings[booking_id]
        sailing = self.sailings[booking.sailing_id]
        self.sailings[sailing.id] = replace(sailing, seats_left=sailing.seats_left + booking.passengers)
        self.bookings[booking_id] = replace(booking, status="cancelled")
        return self.bookings[booking_id]


def sample_store(now: datetime | None = None) -> Store:
    """Today's timetable and a handful of bookings, relative to `now` so the example never goes stale."""
    now = (now or datetime.now(UTC)).replace(minute=0, second=0, microsecond=0)
    store = Store()
    for hour in range(0, 12, 2):
        departs = now + timedelta(hours=hour + 1)
        for route, prefix in (("Port Ansel to Hollow Island", "PA"), ("Hollow Island to Port Ansel", "HI")):
            sailing = Sailing(f"{prefix}-{departs.astimezone(HARBOUR):%m%d-%H%M}", departs, route)
            store.sailings[sailing.id] = sailing
    first, second, *_ = sorted(store.sailings.values(), key=lambda s: s.departs)
    store.sailings[second.id] = replace(second, status="delayed", delay_minutes=35)
    store.bookings = {
        "BK-1001": Booking("BK-1001", "ana", first.id, 2, vehicle="car"),
        "BK-1002": Booking("BK-1002", "ana", second.id, 1),
        "BK-1003": Booking("BK-1003", "ben", first.id, 4),
    }
    return store
