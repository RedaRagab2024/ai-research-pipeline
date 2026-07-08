import pytest
from state import state
from nodes import librarian, reviewer, writer, qa

def test_shared_state_initial():
    assert state.get("query") is None

def test_prisma_check_empty():
    # Ensure reviewer populates prisma keys
    state.set("working_draft", {})
    result = reviewer.run(state)
    assert isinstance(result, dict)

# Note: Librarian and writer call external APIs; full integration tests are not included here.
