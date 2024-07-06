""" Module to hold auth settings. """
from pydantic.types import SecretStr

from src.config.common import CommonSettings


class AuthSettings(CommonSettings):
    """Database settings"""

    secret_key: SecretStr
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_prefix = "AUTH_"
        extra = "ignore"
