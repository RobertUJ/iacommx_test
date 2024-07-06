""" Router module for solicitudes. """
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.helpers import get_db
from src.tasks import asignar_grimorio

from .crud import solicitud_crud
from .models import EstatusSolicitud
from .schemas import (
    SolicitudCreate,
    SolicitudEstatusUpdate,
    SolicitudInDB,
    SolicitudUpdate,
)

router = APIRouter()


@router.post(
    "/",
    response_model=SolicitudInDB,
    status_code=status.HTTP_201_CREATED,
    summary="Registra una nueva solicitud.",
    description="Registra una nueva solicitud con los datos proporcionados."
)
def create_solicitud(obj_in: SolicitudCreate, db: Session = Depends(get_db)):
    # check if exist identification and email
    if solicitud_crud.exist_identification(db, obj_in.identification):
        raise HTTPException(status_code=400, detail="Identification already exists")
    if solicitud_crud.exist_email(db, obj_in.email):
        raise HTTPException(status_code=400, detail="Email already exists")

    try:
        print("magia", obj_in.magic_affinity)
        return solicitud_crud.create(db, obj_in=obj_in)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error creating solicitud: {e}"
        ) from e


@router.get("/{id}", response_model=SolicitudInDB)
def read_solicitud(id: int, db: Session = Depends(get_db)):
    if solicitud := solicitud_crud.get(db, id):
        return solicitud
    else:
        raise HTTPException(status_code=404, detail="Solicitud not found")


@router.put("/{id}", response_model=SolicitudInDB)
def update_solicitud(id: int, obj_in: SolicitudUpdate, db: Session = Depends(get_db)):
    if not (db_obj := solicitud_crud.get(db, id)):
        raise HTTPException(status_code=404, detail="Solicitud not found")

    # Check if exist identification or email
    if solicitud_crud.exist_identification(db, obj_in.identification, _id=id):
        raise HTTPException(status_code=400, detail="Identification already exists")
    if solicitud_crud.exist_email(db, obj_in.email, _id=id):
        raise HTTPException(status_code=400, detail="Email already exists")

    try:
        return solicitud_crud.update(db, db_obj=db_obj, obj_in=obj_in)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error updating solicitud: {e}"
        ) from e


@router.patch("/{id}/estatus", response_model=SolicitudInDB)
def update_solicitud_estatus(id: int, obj_in: SolicitudEstatusUpdate, db: Session = Depends(get_db)):  # noqa: E501
    try:
        obj_updated = solicitud_crud.update_status(db, _id=id, status=obj_in.status)

        if obj_in.status == EstatusSolicitud.APPROVED:
            asignar_grimorio.delay(obj_updated.id)
        return obj_updated
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error updating solicitud status: {e}"
        ) from e


@router.get("/", response_model=List[SolicitudInDB])
def read_solicitudes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return solicitud_crud.get_multi(db, skip=skip, limit=limit)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a solicitud by ID",
    description="Delete a solicitud by its ID"
)
def delete_solicitud(id: int, db: Session = Depends(get_db)):
    if not (solicitud := solicitud_crud.get(db, id)):
        return HTTPException(status_code=404, detail="Solicitud not found")

    try:
        solicitud_crud.remove(db, db_obj=solicitud)
    except Exception as e:
        return HTTPException(
            status_code=400,
            detail=f"Error deleting solicitud: {e}")

    return {"message": "Solicitud deleted successfully"}
