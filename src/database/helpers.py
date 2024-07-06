"""Module to handle the session creation and closing"""

from typing import Generator

from src.database.session import SessionLocal


def get_db() -> Generator:
    """Get a DB session

    Yields:
        Generator: A session maker instance
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
