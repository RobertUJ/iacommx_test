""" Module for manage helpers for auth module """
from functools import wraps

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.config.helpers import get_settings
from src.database.helpers import get_db
from src.users.crud import user
from src.users.schemas import User

from .constants import RolesList
from .schemas import TokenData
from .utils import verify_password

settings = get_settings()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

SECRET_KEY = settings.auth.secret_key.get_secret_value()
ALGORITHM = settings.auth.algorithm

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")


def authenticate_user(db, identifier: str, password: str) -> User | HTTPException | bool:  # noqa
    """
    Authenticate a user and verify if status is active.
    Return user if password is correct else return False

    Args:
        db: Database session
        identifier: Username
        password: Password
    """
    username, email = (None, identifier) if "@" in identifier else (identifier, None)

    if _user := user.get_by_username_or_email(db, username=username, email=email):
        if _user.is_active is False:
            return HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )
        return (
            _user if verify_password(
                password, _user.hashed_password
            ) else False
        )

    return False


async def get_current_user(
        token: str = Depends(oauth_scheme),
        db: Session = Depends(get_db)
):
    """
    Get current user from token

    Args:
        token: Token
        db: Session
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        raise credentials_exception from e
    except Exception as e:
        raise credentials_exception from e

    if _user := user.get_by_username(db, token_data.username):
        return _user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


def _check_user_roles(current_user: User, allowed_roles: list[RolesList]) -> bool:
    """
    Check if user has the required roles

    Args:
        current_user: User
        allowed_roles: List of roles
    """
    roles_list = {role.name for role in current_user.roles}
    _allowed_roles = {role.value for role in allowed_roles}
    return bool(roles_list.intersection(set(_allowed_roles)))


def _check_user_permissions(current_user: User, allowed_permission: str) -> bool:
    """
    Check if user has the required permissions

    Args:
        current_user: User
        allowed_permission: name of permission allowed
    """
    permissions_list = list(
        {
            permission.name for role in
            current_user.roles for permission in role.permissions
        }
    )
    return allowed_permission in permissions_list


def authorize(*, roles: list[RolesList] | None = None, permission: str | None = None):
    """
    Decorator to check if user has the required roles or permission
    roles: List of roles allowed
    permission: Permission allowed
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            _current_user = kwargs.get("current_user")

            param = ""
            if roles:
                param += f"Roles: { [role.name for role in roles] } "

            if permission:
                param += f"Permission: {permission}"

            if not _current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User is not authenticated",
                )
            # Check if user has the required roles or permission
            if (
                    (roles and _check_user_roles(_current_user, roles)) or
                    (permission and _check_user_permissions(_current_user, permission))
            ):
                return await func(*args, **kwargs)
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"User is not authorized to access this resource, {param} required", # noqa
                )

        return wrapper

    return decorator
