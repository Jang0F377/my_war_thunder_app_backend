from jwt import decode, encode, exceptions
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidKeyError
from fastapi import HTTPException
from datetime import timedelta, datetime, timezone
from typing import Union
import os
from constants.user.user_constants import ROLES
from fastapi.security import OAuth2PasswordBearer


class JwtService:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes=ROLES)
    secret_key: str
    jwt_algorithm: str

    def __init__(self) -> None:
        self.secret_key = os.environ.get("SECRET_KEY")
        self.jwt_algorithm = os.environ.get("JWT_ALGORITHM")

    def create_access_token(
        self, data: dict[str, str], expires: Union[timedelta, None] = None
    ) -> str:
        to_encode = data.copy()

        if expires:
            expiration = datetime.now(timezone.utc) + expires
        else:
            expiration = datetime.now(timezone.utc) + timedelta(minutes=100)

        to_encode.update({"exp": expiration})

        encoded_jwt = encode(
            payload=to_encode, key=self.secret_key, algorithm=self.jwt_algorithm
        )
        return encoded_jwt

    def decode_token(self, given_token: str) -> dict[str, any]:
        try:
            payload = decode(
                jwt=given_token, key=self.secret_key, algorithms=self.jwt_algorithm
            )
        except (DecodeError, ExpiredSignatureError, InvalidKeyError):
            raise HTTPException(
                status_code=401, detail="JWT decoding error. JWT may be expired."
            )

        return payload
