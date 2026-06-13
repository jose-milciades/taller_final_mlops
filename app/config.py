from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_env: str = Field(default="dev", alias="APP_ENV")
    model_path: Path = Field(default=Path("artifacts/model.onnx"), alias="MODEL_PATH")
    predictions_log_path: Path = Field(
        default=Path("artifacts/predicciones_dev.txt"),
        alias="PREDICTIONS_LOG_PATH",
    )
    predictions_log_uri: str | None = Field(default=None, alias="PREDICTIONS_LOG_URI")


@lru_cache
def get_settings() -> Settings:
    return Settings()
