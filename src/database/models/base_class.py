"""module for base class"""

from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr

from ..utils import _to_snake_case


@as_declarative()
class Base:
    """Produce a declarative base class.

    Model object with default attributes.

    Attributes:

      - id (Any): model identifier.
      - `__tablename__` (str): auto generated table name from model name

    """

    id: Any
    created_at: Any

    __name__: str

    # Generate __tablename__ automatically
    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return _to_snake_case(cls.__name__)
