""" Module for helper functions for authentication """

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt

from src.auth.constants import PermissionsList
from src.config.helpers import get_settings

settings = get_settings()

SECRET_KEY = settings.auth.secret_key.get_secret_value()
ALGORITHM = settings.auth.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.auth.access_token_expire_minutes


def hash_password(password: str) -> str:
    """Hash a password

    Args:
        password (str): Password to hash
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password

    Args:
        password (str): Password to verify
        hashed_password (str): Hashed password
    """

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create an access token

    Args:
        data (dict): Data to encode in the token
        expires_delta: timedelta | None: Expiry time for the token 
                       (default: ACCESS_TOKEN_EXPIRE_MINUTES) 
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # If no expiry time is provided, set the expiry time to the default
        expire = (
                datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_token_auth_header(credentials: HTTPAuthorizationCredentials) -> str:
    """Obtains the Access Token from the Authorization Header"""
    if not credentials:
        raise HTTPException(
            detail="Authorization header is expected",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            detail="Authorization header must start with Bearer",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return credentials.credentials


@dataclass
class Permissions:
    module_name: str

    @property
    def create(self) -> str:
        return self._set_name(PermissionsList.CREATE.value)

    @property
    def read(self) -> str:
        return self._set_name(PermissionsList.READ.value)

    @property
    def update(self) -> str:
        return self._set_name(PermissionsList.UPDATE.value)

    @property
    def delete(self) -> str:
        return self._set_name(PermissionsList.DELETE.value)

    def _set_name(self, permission: str):
        return f"{permission}:{self.module_name}"
