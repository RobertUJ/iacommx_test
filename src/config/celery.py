"""module to hold celery settings """

from .common import CommonSettings


class CelerySettings(CommonSettings):
    """Database settings"""

    worker: bool = False
    broker_url: str
    backend_url: str

    class Config:
        env_prefix = "CELERY_"
        extra = "ignore"
