import os, tempfile

from ffmpeg_agent.settings import AppSettings

def test_env_precedence(monkeypatch):
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write("provider=openrouter\n")
        f.flush()
        monkeypatch.setenv("PROVIDER", "openai")
        s = AppSettings(_env_file=f.name)
        assert s.provider == "openai"
