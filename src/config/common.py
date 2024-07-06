"""Module for common base settings"""
from pydantic_settings import BaseSettings, SettingsConfigDict

CONFIG_FILE = ".env"


class CommonSettings(BaseSettings):
    """Common settings for the project"""

    model_config = SettingsConfigDict(
        env_file=CONFIG_FILE,
        env_prefix="PROJECT_",  # Prefix for environment variables
        env_file_encoding="utf-8",
        extra="ignore"
    )
