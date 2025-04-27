from pathlib import Path
from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict

class MemoryStrategy(str, Enum):
    EPHEMERAL = "ephemeral"
    WINDOW    = "window"
    SUMMARY   = "summary"
    VECTOR    = "vector"

class AppSettings(BaseSettings):
    provider: str = "openai"
    model: str | None = None

    openai_api_key: str | None = None
    openrouter_api_key: str | None = None
    anthropic_api_key: str | None = None

    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3"

    run_timeout_sec: int = 600
    max_tool_calls: int = 12
    db_path: Path = Path.home() / ".ffmpeg_agent.sqlite3"

    memory_strategy: MemoryStrategy = MemoryStrategy.EPHEMERAL
    vss_ext_path: str | None = None

    output: str = "plain"
    quiet: bool = False
    log_format: str = "text"
    progress_file: Path | None = None

    model_config = SettingsConfigDict(
        env_file=Path.home() / ".ffmpeg_agent.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = AppSettings()

