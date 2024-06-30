from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user import user_model
from schemas.user import user_schema
import jwt
from services.hasher import PasswordHasher


def get_user_by_id(db: Session, user_id: str) -> user_schema.User:
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()


def get_user_by_email(db: Session, user_email: str) -> user_schema.User:
    return db.query(user_model.User).filter(user_model.User.email == user_email).first()


def get_all_users(
    db: Session, skip: int = 0, limit: int = 100
) -> list[user_schema.User]:
    return db.query(user_model.User).offset(skip).limit(limit).all()


def create_user(
    db: Session, user: user_schema.UserCreate, hasher: PasswordHasher
) -> user_schema.User:
    hashed_password = hasher.hash_password(user.password)
    email = user.email.lower()
    user_to_create = user_model.User(email=email, hashed_pwd=hashed_password)
    db.add(user_to_create)
    db.commit()
    db.refresh(user_to_create)
    return user_to_create
