""" Module for tasks related to products """
import logging

from sqlalchemy.orm import Session

from src.celery_worker import celery_app
from src.database.session import SessionLocal
from src.grimorios.helpers import GrimorioFactory
from src.solicitudes.crud import solicitud_crud


@celery_app.task
def asignar_grimorio(solicitud_id: int):
    db: Session = SessionLocal()

    if solicitud_obj := solicitud_crud.get(db, solicitud_id):
        grimorio = GrimorioFactory.asignar_grimorio()

        solicitud_obj.grimoire_type = grimorio.grimorio_tipo
        solicitud_obj.grimoire_description = grimorio.descripcion
        solicitud_obj.clover_leaves = grimorio.numero_hojas

        db.commit()
        db.refresh(solicitud_obj)
        logging.info(f"Assigned grimorio {grimorio} to solicitud {solicitud_obj}")
    else:
        logging.error(f"Solicitud with id {solicitud_id} not found")

    db.close()






@celery_app.task
def notify(user_id: int, message: str):
    print(f"Sending notification to user {user_id}: {message}")
