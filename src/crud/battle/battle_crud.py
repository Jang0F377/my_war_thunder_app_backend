from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.battle import battle_model
from schemas.battle import battle_schema


def get_all_battles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(battle_model.Battle).offset(skip).limit(limit).all()


def add_battle_for_user(
    db: Session, battle: battle_schema.Battle, user_id: str
) -> battle_schema.Battle:
    battle_item = battle_model.BattleType(**battle.model_dump(), user_id=user_id)
    db.add(battle_item)
    db.commit()
    db.refresh(battle_item)
    return battle_item
