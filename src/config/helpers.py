"""Module to manage helper functions for the settings"""
from functools import lru_cache

# from functools import lru_cache
from .settings import settings


@lru_cache
def get_settings() -> settings:
    return settings
