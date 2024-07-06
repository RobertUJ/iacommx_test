""" Module for managing authentication schemas """

from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    password: str
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
