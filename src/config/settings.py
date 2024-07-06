""" Module for project settings """

from pydantic_settings import BaseSettings, SettingsConfigDict

from .apps.auth import AuthSettings
from .celery import CelerySettings
from .common import CONFIG_FILE, CommonSettings

# Imports settings for each module
from .database import DatabaseSettings


class Settings(CommonSettings):
    """Settings for the project"""
    name: str
    version: str
    host: str
    port: int

    # Modules settings
    database: BaseSettings = DatabaseSettings()
    auth: BaseSettings = AuthSettings()
    celery: BaseSettings = CelerySettings()

    model_config = SettingsConfigDict(
        env_file=CONFIG_FILE,
        env_prefix="PROJECT_",  # Prefix for environment variables
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
