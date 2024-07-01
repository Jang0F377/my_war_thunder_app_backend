from pydantic import BaseModel
from typing import Union
from constants.battle import battle_constants
from datetime import datetime
import uuid


class BattleBase(BaseModel):
    pass


class BattleCreate(BattleBase):
    battle_map: Union[str, None] = None
    faction_played: battle_constants.Faction
    battle_type: battle_constants.BattleType
    player_br: float
    ceiling_br: float
    battle_won: Union[bool, None] = None


class Battle(BattleCreate):
    id: uuid.UUID
    user_id: uuid.UUID
    date_time: datetime

    class Config:
        orm_mode = True
