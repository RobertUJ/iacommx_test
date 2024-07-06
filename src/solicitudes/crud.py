""" Module for solicitudes crud operations. """
from fastapi import HTTPException

from src.database.crud import CRUDBase

# import models to interact with the database
from .models import EstatusSolicitud, Solicitud

# from .schemas import SolicitudCreate, SolicitudUpdate
from .schemas import SolicitudCreate, SolicitudUpdate


class CRUDSolicitud(CRUDBase[Solicitud, SolicitudCreate, SolicitudUpdate]):

    def update_status(self, db, _id: int, status: EstatusSolicitud):
        if not (solicitud := self.get(db, _id)):
            raise HTTPException(status_code=404, detail="Solicitud not found")

        # check if status is valid enum element
        print("status valor", status)

        # check if status is valid
        if status not in EstatusSolicitud:
            raise HTTPException(
                status_code=400, detail="Invalid status value"
            )

        solicitud.status = status

        # Save the changes to the database
        try:
            db.commit()
            db.refresh(solicitud)
            return solicitud
        except Exception as e:
            db.rollback()
            raise e

    def exist_email(self, db, email: str, _id: int | None = None) -> bool:
        """Check if name exists

        Args:
            db: (Session): Database session
            email: (str): email of solicitud
            _id: Optional[int]: Solicitud ID to exclude from the query
        """
        _field = "email"
        return self._exist_by_field(db, field_name=_field, value=email, exclude_id=_id)

    def exist_name(self, db, name: str, _id: int | None = None) -> bool:
        """Check if name exists

        Args:
            db: (Session): Database session
            name: (str): Name of solicitud
            _id: Optional[int]: Solicitud ID to exclude from the query
        """
        _field = "name"
        return self._exist_by_field(db, field_name=_field, value=name, exclude_id=_id)

    def exist_identification(self, db, name: str, _id: int | None = None) -> bool:
        """ Check if identification exists
        Args:
            db: (Session): Database session
            name: (str): Name of solicitud
            _id: Optional[int]: Solicitud ID to exclude from the query
        """
        _field = "identification"
        return self._exist_by_field(db, field_name=_field, value=name, exclude_id=_id)


solicitud_crud = CRUDSolicitud(Solicitud)
