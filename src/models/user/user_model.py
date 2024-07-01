import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from database import Base
from models.battle import battle_model


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(sqlalchemy.String(30), unique=True, index=True)
    hashed_pwd: Mapped[str]
    battles: Mapped[list["battle_model.BattleType"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
