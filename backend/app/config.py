"""
LexSentry Backend Configuration
Loads settings from environment variables / .env file.
"""
from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    _APP_DIR = Path(sys.executable).resolve().parent
else:
    _APP_DIR = Path(__file__).resolve().parent.parent

_DB_FILE = _APP_DIR / "lexsentry.db"
DEFAULT_DB_URL = f"sqlite+aiosqlite:///{_DB_FILE.as_posix()}"
_ENV_FILE = _APP_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE) if _ENV_FILE.exists() else ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Application ────────────────────────────────────────
    app_name: str = "Cyber Law Watch Agent"
    app_version: str = "0.1.0"
    app_env: str = "development"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 1440  # 24h

    # ── Database ───────────────────────────────────────────
    database_url: str = DEFAULT_DB_URL

    # ── LLM (Gemini) ───────────────────────────────────────
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.5-flash-lite"

    # ── Storage ────────────────────────────────────────────
    storage_dir: str = str(_APP_DIR / "storage")

    # ── CORS ───────────────────────────────────────────────
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    def get_cors_origins(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
