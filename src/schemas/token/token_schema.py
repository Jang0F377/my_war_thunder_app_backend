from pydantic import BaseModel
from typing import Union


# Classes to define the JWT token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
    roles: str = []
