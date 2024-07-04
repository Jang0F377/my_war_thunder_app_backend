from pydantic import BaseModel
from schemas.battle import battle_schema
import uuid


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: uuid.UUID
    battles: list[battle_schema.Battle]

    class Config:
        from_attributes = True
