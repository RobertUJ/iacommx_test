"""Module for handling database engine and session"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from src.config.helpers import get_settings

settings = get_settings()
url_object = settings.database.get_url_object
engine = create_engine(url_object, isolation_level="REPEATABLE READ")

# Create a session factory
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# Create a base class for the models
Base = declarative_base()
