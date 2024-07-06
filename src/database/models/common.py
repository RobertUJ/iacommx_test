""" Module for common database models """

from sqlalchemy import Column, Integer, text

from .base_class import Base
from .types import CustomDateTime


class CommonModel(Base):
    __abstract__ = True

    def __init__(self, **kwargs):
        """
           Constructor for the CommonModel class.

           This method accepts any number of keyword arguments and filters them to only 
           include those that are allowed.
           The allowed arguments are those that are in the SQLAlchemy mapper associated 
           with the class.
           The filtered arguments are then passed to the constructor of the superclass.

           :param kwargs: Any number of keyword arguments.
           """
        allowed_args = self.__mapper__.class_manager
        kwargs = {k: v for k, v in kwargs.items() if k in allowed_args}
        super().__init__(**kwargs)

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        CustomDateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
