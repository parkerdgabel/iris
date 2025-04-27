# Placeholder for summary memory
from typing import List, Dict
from ..providers_sync import BaseClient # Assuming synchronous for now

class SummaryMemory:
    def __init__(self, provider_client: BaseClient, max_tokens: int = 500):
        self.provider_client = provider_client
        self.max_tokens = max_tokens
        self.summary = ""

    def add_message(self, message: dict):
        # In a real implementation, we would add messages and summarize periodically
        pass

    def get_history(self) -> list[dict]:
        # In a real implementation, we would return the summary and recent messages
        return []

    def clear(self):
        self.summary = ""
