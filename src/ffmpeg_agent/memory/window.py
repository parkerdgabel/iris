# Placeholder for window memory
from collections import deque

class WindowMemory:
    def __init__(self, max_size: int = 10):
        self.history = deque(maxlen=max_size)

    def add_message(self, message: dict):
        self.history.append(message)

    def get_history(self) -> list[dict]:
        return list(self.history)

    def clear(self):
        self.history.clear()
