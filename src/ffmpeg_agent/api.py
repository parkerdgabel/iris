import json
from typing import Optional
from pydantic import BaseModel

from ffmpeg_agent.settings import settings
from ffmpeg_agent.agent import build_agent
from ffmpeg_agent.providers_sync import (
 OpenAIClient, OpenRouterClient, AnthropicClient, OllamaClient
)

class FFmpegResult(BaseModel):
    session: str
    status: str
    steps: list[dict]
    verify: Optional[dict] = None
    elapsed_ms: int


def _client():
    match settings.provider.lower():
        case "openai":     return OpenAIClient()
        case "openrouter": return OpenRouterClient()
        case "anthropic":  return AnthropicClient()
        case "ollama":     return OllamaClient()
        case _: raise ValueError("Unsupported provider")

def run_prompt(prompt: str, *, output="json") -> FFmpegResult:
    agent = build_agent(_client())
    summary = agent.run({}, prompt)
    return FFmpegResult.parse_obj(json.loads(summary.model_dump_json()))
