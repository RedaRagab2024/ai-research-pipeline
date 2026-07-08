from typing import Dict, Any
import threading

class SharedState:
    def __init__(self):
        self.lock = threading.Lock()
        self.state: Dict[str, Any] = {
            "query": None,
            "working_draft": {},
            "verified_bibliography": [],
            "prisma": {},
            "nodes": {},
        }

    def get(self, key, default=None):
        with self.lock:
            return self.state.get(key, default)

    def set(self, key, value):
        with self.lock:
            self.state[key] = value

    def update(self, key, partial: dict):
        with self.lock:
            self.state.setdefault(key, {}).update(partial)

state = SharedState()
