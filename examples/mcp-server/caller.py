"""Who is calling, and what they may do.

Over HTTP every request carries a bearer token. The server's token verifier has already checked it (signature,
expiry, issuer, and that its audience is this server, so a token issued for some other API is refused) before any
tool runs, and `get_access_token()` returns the verified token. The server reads the user and the scopes from it
and never forwards the token itself to another service: a downstream API gets its own token, obtained for the same
user (an OAuth token exchange), so every read and write still runs as that user under that API's permissions.

Over stdio there is no token. The host started this process on the user's own machine, so the caller is that user,
named by FERRY_USER, who may read and change their own bookings; FERRY_STAFF=1 makes them staff. A local process is
as trusted as the user who launched it, and no more.
"""

import os
from dataclasses import dataclass

from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_access_token

READ, WRITE, STAFF = "bookings:read", "bookings:write", "staff"


@dataclass(frozen=True)
class Caller:
    user: str
    scopes: frozenset[str]

    @property
    def staff(self) -> bool:
        return STAFF in self.scopes

    def require(self, scope: str) -> None:
        """Refuse in code, whatever the model was told. A prompt can be talked out of a rule; this cannot."""
        if scope not in self.scopes:
            raise ToolError(f"This needs the '{scope}' permission, which your sign-in does not have.")


def current() -> Caller:
    token = get_access_token()
    if token is None:
        staff = {STAFF} if os.environ.get("FERRY_STAFF") == "1" else set()
        return Caller(os.environ.get("FERRY_USER", "ana"), frozenset({READ, WRITE} | staff))
    user = token.claims.get("sub") or token.client_id
    return Caller(user, frozenset(token.scopes))
