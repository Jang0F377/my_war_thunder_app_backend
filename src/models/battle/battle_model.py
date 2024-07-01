import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from enum import Enum
import uuid
import datetime
from database import Base
from constants.battle.battle_constants import BattleType, Faction
from models.user import user_model


class BattleType(Base):
    __tablename__ = "battles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    date_time: Mapped[datetime.datetime] = mapped_column(
        sqlalchemy.DateTime(), default=datetime.datetime.now(), nullable=False
    )
    battle_map: Mapped[Optional[str]]
    faction_played: Mapped[Faction] = mapped_column(
        sqlalchemy.Enum(Faction), nullable=False
    )
    battle_type: Mapped[BattleType] = mapped_column(
        sqlalchemy.Enum(BattleType), nullable=False
    )
    player_br: Mapped[float] = mapped_column(
        sqlalchemy.Float(1), default=0.0, nullable=False
    )
    ceiling_br: Mapped[float] = mapped_column(
        sqlalchemy.Float(1), default=0.0, nullable=False
    )
    battle_won: Mapped[Optional[bool]] = mapped_column(
        sqlalchemy.Boolean(), default=None, nullable=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(sqlalchemy.ForeignKey("users.id"))

    user: Mapped["user_model.User"] = relationship(back_populates="battles")
