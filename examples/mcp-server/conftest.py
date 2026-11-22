import sys
from pathlib import Path

# The example's modules import each other by name (as they do when server.py runs as a script).
sys.path.insert(0, str(Path(__file__).parent))

import pytest


@pytest.fixture
def anyio_backend():
    return "asyncio"


def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker(pytest.mark.anyio)
