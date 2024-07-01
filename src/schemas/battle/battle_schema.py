from pydantic import BaseModel
from typing import Union
from constants.battle import battle_constants
from datetime import datetime


class BattleBase(BaseModel):
    battle_map: Union[str, None] = None
    faction_played: battle_constants.Faction
    batlle_type: battle_constants.BattleType
    player_br: float
    ceiling_br: float
    battle_won: Union[bool, None] = None


class BattleCreate(BattleBase):
    pass


class Battle(BattleBase):
    id: str
    user_id: str
    date_time: datetime

    class Config:
        orm_mode = True
