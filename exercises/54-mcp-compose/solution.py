# Your task is in README.md in this folder. The code at the top is given; yours goes under "Yours" at line 66.
# Each EXERCISE-TODO comment below is one piece to write. Save, then type /check in the Claude chat.
import re
from pathlib import Path

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.middleware import Middleware, MiddlewareContext

# ---- Given: the pipeline project's documents and a small keyword search. Do not change. ----

CORPUS = Path(__file__).resolve().parents[1] / "50-pipeline-project" / "corpus"
PAGE_BREAK = "--- page break ---"


def load_documents(folder: Path = CORPUS) -> dict[str, str]:
    """Each document's full text, by file name: {"fares.txt": "Brackwater Ferry: fares and tickets ...", ...}."""
    return {p.name: p.read_text() for p in sorted(folder.glob("*.txt"))}


def keyword_search(documents: dict[str, str], query: str, k: int) -> list[dict]:
    """The k paragraphs that share the most words with the query, best first, as {"file", "text"} dicts."""
    words = set(re.findall(r"[a-z0-9]+", query.lower()))
    scored = []
    for name, text in documents.items():
        for para in re.split(r"\n\s*\n", text.replace(PAGE_BREAK, "\n\n")):
            hits = len(words & set(re.findall(r"[a-z0-9]+", para.lower())))
            if hits:
                scored.append((-hits, name, " ".join(para.split())))
    return [{"file": name, "text": text} for _, name, text in sorted(scored)[:k]]


# ---- Given: the two domain servers and the instructions. Do not change. ----

INSTRUCTIONS = """Brackwater Ferry: its published rules (docs_search) and live bookings (bookings tools).
Rules and prices come from docs_search, cited by file. A booking comes from the bookings tools, never from memory."""

BOOKINGS = {"BK-1001": {"id": "BK-1001", "owner": "ana", "status": "confirmed"}}


def create_docs_server() -> FastMCP:
    server = FastMCP("ferry-docs")
    documents = load_documents()

    @server.tool(annotations={"readOnlyHint": True})
    def search(query: str, k: int = 3) -> dict:
        """Search Brackwater Ferry's documents and return matching passages, each with its file."""
        return {"passages": keyword_search(documents, query, k)}

    return server


def create_bookings_server() -> FastMCP:
    server = FastMCP("ferry-bookings")

    @server.tool(annotations={"readOnlyHint": True})
    def get_booking(booking_id: str) -> dict:
        """A passenger's booking, read live."""
        if booking_id not in BOOKINGS:
            raise ToolError(f"No booking {booking_id}.")
        return BOOKINGS[booking_id]

    return server


# ---- Yours ----

# EXERCISE-TODO: AuditLog(log): middleware that keeps the list it is made with. on_call_tool(self, context,
# call_next) awaits call_next(context) and appends "<tool name> ok" to the list, or "<tool name> error" when the
# call raised, and then raises the same error again. The tool's name is context.message.name.
#   after a docs_search call that works   ->  log == ["docs_search ok"]
#   after a bookings_get_booking that fails  ->  log == [..., "bookings_get_booking error"], and the call still fails
class AuditLog(Middleware):
    pass        # replace with __init__ and on_call_tool


# EXERCISE-TODO: create_server(log=None): return a FastMCP server named "brackwater-ferry" with
# instructions=INSTRUCTIONS, create_docs_server() mounted under the namespace "docs" and create_bookings_server()
# under "bookings", and an AuditLog writing to log (a new list when log is None).
#   tools listed  ->  {"docs_search", "bookings_get_booking"}
def create_server(log: list[str] | None = None) -> FastMCP:
    raise NotImplementedError
