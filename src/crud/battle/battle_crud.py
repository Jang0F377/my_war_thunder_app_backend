from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.battle import battle_model
from schemas.battle import battle_schema






def add_battle_for_user(db: Session, battle: battle_schema.Battle, user_id: str) -> battle_schema.Battle:
    battle_item = battle_model.BattleType(**battle.model_dump(), user_id=user_id)
    db.add(battle_item)
    db.commit()
    db.refresh(battle_item)
    return battle_item