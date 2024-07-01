from typing import Union, Annotated
from database import provide_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, Security
from fastapi.security import SecurityScopes
from models.user import user_model
from schemas.user import user_schema
from schemas.token import token_schema
from services.jwt_service import JwtService, DecodeError
from pydantic import ValidationError
from services.hasher import PasswordHasher

jwt_service = JwtService()


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


def authenticate_user(
    db: Session, email: str, password: str, hasher: PasswordHasher
) -> Union[user_schema.User, bool]:
    user = db.query(user_model.User).filter(user_model.User.email == email).first()

    if user is None:
        return False

    if not hasher.compare_passwords(password, user.hashed_pwd):
        return False

    return user


def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(jwt_service.oauth2_scheme)],
    db: Annotated[any, Depends(provide_db)],
) -> user_schema.User:

    if security_scopes.scopes:
        authenticate_value = f"Bearer scope='{security_scopes.scope_str}'"
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt_service.decode_token(given_token=token)
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception

        token_scopes = payload.get("roles", [])
        token_data = token_schema.TokenData(roles=token_scopes, email=sub)
    except (DecodeError, ValidationError):
        raise credentials_exception

    user = get_user_by_email(db=db, user_email=sub)
    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.roles:
            raise HTTPException(status_code=401, detail="Insufficient Permissions")

    return user


def get_current_active_user(
    current_user: Annotated[
        user_model.User, Security(get_current_user, scopes=["basic"])
    ],
) -> user_schema.User:
    return current_user
