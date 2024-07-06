""" Module for manage the models of solicitudes. """
import enum

from sqlalchemy import Column, Enum, Integer, String

from src.database.models import CommonModel


class EstatusSolicitud(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class MagicAffinity(enum.Enum):
    FIRE = "FIRE"
    WATER = "WATER"
    EARTH = "EARTH"
    AIR = "AIR"
    LIGHT = "LIGHT"
    DARK = "DARK"


class Solicitud(CommonModel):
    name = Column(String, index=True)
    last_name = Column(String, nullable=True)
    identification = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    magic_affinity = Column(Enum(MagicAffinity), nullable=False)
    email = Column(String, unique=True, index=True)
    status = Column(Enum(EstatusSolicitud), default=EstatusSolicitud.PENDING)
    grimoire_type = Column(String, nullable=True)
    grimoire_description = Column(String, nullable=True)
    clover_leaves = Column(Integer, default=0, nullable=True)
