import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_database_url() -> str:
    if url := os.getenv("DATABASE_URL"):
        return url
    repo_root = Path(__file__).resolve().parents[2]
    for candidate in (
        repo_root / "backend" / "inmonexo.db",
        repo_root / "inmonexo.db",
        Path.cwd() / "inmonexo.db",
    ):
        if candidate.exists():
            return f"sqlite:///{candidate.as_posix()}"
    return "sqlite:///./inmonexo.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = Field(default_factory=_default_database_url)

    @property
    def sqlalchemy_url(self) -> str:
        url = self.database_url
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url
