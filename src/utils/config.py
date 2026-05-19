from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    openai_model: str
    app_env: str
    openai_embedding_model: str = "text-embedding-3-small"


def get_settings(env_path: Path | None = None) -> Settings:
    load_dotenv(dotenv_path=env_path)
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY") or None,
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        app_env=os.getenv("APP_ENV", "local"),
        openai_embedding_model=os.getenv(
            "OPENAI_EMBEDDING_MODEL",
            "text-embedding-3-small",
        ),
    )
