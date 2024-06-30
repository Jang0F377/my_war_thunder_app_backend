import os
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative

# Get the env_vars to put the db  uri together
DB_PREFIX = os.environ.get("DB_PREFIX")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DATABASE = os.environ.get("DB_DATABASE")
DB_HOST = os.environ.get("DB_HOST")
DB_URI = f"{DB_PREFIX}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"

engine = sqlalchemy.create_engine(DB_URI)

SessionLocal = sqlalchemy.orm.sessionmaker(autoflush=False, bind=engine)

Base = sqlalchemy.ext.declarative.declarative_base()


def provide_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
