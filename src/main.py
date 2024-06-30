import datetime
from fastapi import Depends, FastAPI, Request, HTTPException
from database import provide_db
from sqlalchemy.orm import Session
from schemas.user import user_schema
from crud.user import user_crud
from services.hasher import PasswordHasher

app = FastAPI()
password_hasher = PasswordHasher()


@app.get("/healthcheck", response_model=None)
def healthcheck(request: Request) -> dict[str, any]:
    req_headers = request.headers
    user_agent = req_headers["user-agent"]
    referer = req_headers["referer"]
    host = request.client.host
    port = request.client.port
    time = datetime.datetime.now()
    response = {
        "healthy": True,
        "time": time,
        "req_host": f"{host}:{port}",
        "user_agent": user_agent,
        "referer": referer,
    }
    return response


@app.get("/users/", response_model=list[user_schema.User])
def get_all_users(
    db: Session = Depends(provide_db), skip: int = 0, limit: int = 100
) -> list[user_schema.User]:
    return user_crud.get_all_users(db=db, skip=skip, limit=limit)


@app.get("/users/{user_identifier}", response_model=user_schema.User)
def get_user(
    user_identifier: str, db: Session = Depends(provide_db)
) -> user_schema.User:
    user_found: user_schema.User
    if user_identifier.find("@") is not -1:
        # is email
        user_found = user_crud.get_user_by_email(db=db, user_email=user_identifier)
    else:
        # is uuid
        user_found = user_crud.get_user_by_id(user_id=user_identifier, db=db)

    if not user_found:
        raise HTTPException(status_code=404, detail="User not found.")

    return user_found


@app.post("/users/", response_model=user_schema.User)
def create_user(
    user: user_schema.UserCreate, db: Session = Depends(provide_db)
) -> user_schema.User:
    if not user.email or not user.password:
        raise HTTPException(
            status_code=400, detail="Cannot send empty values for email or password."
        )

    user_exists = user_crud.get_user_by_email(db=db, user_email=user.email)
    if user_exists:
        raise HTTPException(
            status_code=400, detail="Email is already registered, try logging in."
        )

    return user_crud.create_user(db=db, user=user, hasher=password_hasher)
