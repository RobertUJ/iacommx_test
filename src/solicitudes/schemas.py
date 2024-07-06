# schemas.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints
from typing_extensions import Annotated

from .models import EstatusSolicitud, MagicAffinity


class SolicitudBase(BaseModel):
    name: str = Field(..., min_length=0, max_length=20)
    last_name: str = Field(..., min_length=0, max_length=20)
    identification: Annotated[
        str,
        StringConstraints(strip_whitespace=True, to_upper=False, pattern=r'^[a-zA-Z0-9]*$')
    ] = Field(..., min_length=0, max_length=10)
    age: int = Field(..., ge=1, le=99)
    magic_affinity: MagicAffinity
    email: EmailStr
    status: EstatusSolicitud = EstatusSolicitud.PENDING
    grimoire_type: Optional[str] = None
    grimoire_description: Optional[str] = None
    clover_leaves: Optional[int] = Field(0, ge=0)


class SolicitudCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=20)
    last_name: str = Field(..., min_length=2, max_length=20)
    identification: Annotated[
        str,
        StringConstraints(strip_whitespace=True, to_upper=False, pattern=r'^[a-zA-Z0-9]*$')
    ] = Field(None, min_length=0, max_length=10)
    age: int = Field(..., ge=1, le=99)
    magic_affinity: MagicAffinity
    email: EmailStr


class SolicitudUpdate(BaseModel):
    name: str | None = Field(None, min_length=0, max_length=20)
    last_name: str | None = Field(None, min_length=0, max_length=20)
    identification: Annotated[
        str,
        StringConstraints(strip_whitespace=True, to_upper=False, pattern=r'^[a-zA-Z0-9]*$')
    ] | None = Field(None, min_length=3, max_length=10)
    age: int | None = Field(None, ge=0, le=2)
    magic_affinity: MagicAffinity | None = None
    email: EmailStr | None = None


class SolicitudEstatusUpdate(BaseModel):
    status: EstatusSolicitud


class SolicitudInDBBase(SolicitudBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Solicitud(SolicitudBase):
    pass


class SolicitudInDB(SolicitudInDBBase):
    pass
