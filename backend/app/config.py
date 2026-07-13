from __future__ import annotations

import os
from pathlib import Path
from typing import Any


def load_environment(env_path: str | os.PathLike[str] | None = None) -> None:
    """Load environment variables from a .env file if present."""
    env_file = Path(env_path or os.getenv("ENV_FILE", Path(__file__).resolve().parents[1] / ".env"))
    if not env_file.exists():
        return

    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def get_openai_api_key() -> str | None:
    """Return the configured OpenAI API key from the environment."""
    return os.getenv("OPENAI_API_KEY")


def get_openai_model() -> str:
    """Return the configured OpenAI model name."""
    return os.getenv("OPENAI_MODEL", "gpt-4o")


def get_openai_base_url() -> str:
    """Return the configured OpenAI base URL."""
    return os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")


load_environment()
