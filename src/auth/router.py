""" Module for the auth router. """
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth.helpers import authenticate_user
from src.auth.schemas import Token
from src.auth.utils import create_access_token
from src.config.helpers import get_settings
from src.database.helpers import get_db

router = APIRouter()

settings = get_settings()

ACCESS_TOKEN_EXPIRES = settings.auth.access_token_expire_minutes
db_dependency = Annotated[Session, Depends(get_db)]


@router.post(
    "/login/",
    tags=["auth"],
    summary="Login for access token",
    description="Login for access token",
    response_model=Token
)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    if _user := authenticate_user(db, form_data.username, form_data.password):
        # timedelta could be set by user type 
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES)
        access_token = create_access_token(
            data={
                "sub": _user.username,
                "roles": (
                    [x.id for x in _user.roles] if _user.roles else []
                ),
                "is_active": True,
            }
            , expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
