"""module to hold database settings"""
from pydantic.types import SecretStr
from sqlalchemy import URL

from src.config.common import CommonSettings


class DatabaseSettings(CommonSettings):
    """Database settings"""

    drivername: str
    username: str
    password: SecretStr
    db: str
    host: str
    port: int
    url: str

    @property
    def get_url_object(self) -> URL:
        """Create and Get the URL object from the database settings """
        return URL.create(
            drivername=self.drivername,
            username=self.username,
            password=self.password.get_secret_value(),
            host=self.host,
            database=self.db,
            port=self.port
        )

    class Config:
        env_prefix = "DATABASE_"
        extra = "ignore"
