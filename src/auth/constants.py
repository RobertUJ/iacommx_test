""" Module for manage constants for auth module """
from enum import Enum


class RolesList(Enum):
    SUPER_ADMIN: str = "super_admin"
    ADMIN: str = "admin"
    USER: str = "user"


class PermissionsList(Enum):
    CREATE: str = "create"
    READ: str = "read"
    UPDATE: str = "update"
    DELETE: str = "delete"
