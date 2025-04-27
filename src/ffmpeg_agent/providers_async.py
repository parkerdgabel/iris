import httpx
from typing import Any, Dict
from .settings import settings, AppSettings

class BaseAsyncClient:
    def __init__(self, s: AppSettings = settings):
        self.s = s
        self.session = httpx.AsyncClient(timeout=s.run_timeout_sec)

class OpenAIAsyncClient(BaseAsyncClient):
    async def chat(self, messages: list[dict[str, str]], **params) -> str:
        body: Dict[str, Any] = {
            "model": self.s.model or "gpt-4o-mini",
            "messages": messages,
            **params,
        }
        r = await self.session.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.s.openai_api_key}"
            },
            json=body,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

class OpenRouterAsyncClient(BaseAsyncClient):
    async def chat(self, messages: list[dict[str, str]], **params) -> str:
        body = {
            "model": self.s.model or "openrouter/auto",
            "messages": messages,
            **params,
        }
        r = await self.session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.s.openrouter_api_key}"
            },
            json=body,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

class AnthropicAsyncClient(BaseAsyncClient):
    async def chat(self, messages: list[dict[str, str]], **params) -> str:
        body = {
            "model": self.s.model or "claude-3-haiku-20240307",
            "messages": messages,
            **params,
        }
        r = await self.session.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.s.anthropic_api_key
            },
            json=body,
        )
        r.raise_for_status()
        return r.json()["content"][0]["text"]

class OllamaAsyncClient(BaseAsyncClient):
    def __init__(self, s: AppSettings = settings):
        super().__init__(s)
        self.host = s.ollama_host.rstrip("/")

    async def chat(self, messages: list[dict[str, str]], **params) -> str:
        body = {
            "model": self.s.model or self.s.ollama_model,
            "messages": messages,
            "stream": False,
            **params,
        }
        r = await self.session.post(f"{self.host}/api/chat", json=body)
        r.raise_for_status()
        return r.json()["message"]["content"]

