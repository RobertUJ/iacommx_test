""" Module for base LAD CRUD operations """

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder

# Base class and Base Schema for Type hinting
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.database.models.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        Args:

        `model`: A SQLAlchemy model class
        """
        self.model = model  # type: ModelType

    def get(self, db: Session, id: Any) -> ModelType | None:
        """ Get a single ModelType filtered by id

        Args:
            db: (Session): SQLAlchemy Session object.
            id: (Any): The ID of the object to retrieve.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
            self,
            db: Session,
            *,
            skip: Optional[int] = 0,
            limit: Optional[int] = 100
    ) -> List[ModelType]:
        """ Get all ModelType object

        Args:
            db (Session): SQLAlchemy Session object.
            skip (Optional[int]): The number of records to skip.
            limit (Optional[int]): The number of records to return.
        """

        return db.query(self.model).offset(skip).limit(limit).all()

    def get_multi_by_ids(self, db: Session, *, ids: List[int]) -> List[ModelType]:
        """ Get multiple ModelType objects by their IDs

        Args:
            db (Session): SQLAlchemy Session object.
            ids (List[int]): The list of IDs to retrieve.
        """
        return db.query(self.model).filter(self.model.id.in_(ids)).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """ Create a ModelType object
        Args:
            db (Session): SQLAlchemy Session object.
            obj_in (CreateSchemaType): The data to create the object as a Pydantic model.
        Returns:
            ModelType: The created database object.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore

        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except SQLAlchemyError as e:
            db.rollback()
            raise e

        return db_obj

    @staticmethod
    def update(
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update a ModelType object.

        Args:
            db (Session): SQLAlchemy Session object.
            db_obj (ModelType): The database object to update.
            obj_in (Union[UpdateSchemaType, Dict[str, Any]]): The update data as a Pydantic model or dictionary.

        Returns:
            ModelType: The updated database object.
        """  # noqa: E501
        # Convert Pydantic model to dictionary
        update_data = obj_in \
            if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)

        # Update the database object with the new data
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        try:
            db.commit()
            db.refresh(db_obj)
        except SQLAlchemyError as e:
            db.rollback()
            raise e

        return db_obj

    @staticmethod
    def remove(db: Session, *, db_obj: ModelType) -> None:
        """
        Delete a model instance by ID.

        Args:
            db: SQLAlchemy Session object.
            db_obj: The database object to delete.
        """
        try:
            db.delete(db_obj)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    def _exist_by_field(
            self, 
            db: Session,
            *, 
            field_name: str, 
            value: str, 
            exclude_id: int | None = None
    ) -> bool:
        """
        Check if field exists and exclude by ID if this is provided
        
        Args:
            db: (Session): Database session
            field_name: (str): Field name
            value: (str): Field value
            exclude_id: Optional[int]: User ID to exclude from the query
        """
        query = db.query(self.model).filter(
            getattr(self.model, field_name) == value
        )
        if exclude_id:
            query = query.filter(
                getattr(self.model, 'id') != exclude_id
            )
            
        # return a true result if the query has a result else false
        return bool(query.first())
