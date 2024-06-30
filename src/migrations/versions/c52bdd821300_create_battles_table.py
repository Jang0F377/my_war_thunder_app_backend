"""create battles table

Revision ID: c52bdd821300
Revises: f9f9c9dbc6fb
Create Date: 2024-06-29 16:27:02.952298

"""

from typing import Sequence, Union
import uuid
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c52bdd821300"
down_revision: Union[str, None] = "f9f9c9dbc6fb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
TABLE_NAME = "battles"
BATTLE_MAP_LENGTH = 25


def upgrade() -> None:
    op.create_table(
        TABLE_NAME,
        sa.Column("id", sa.UUID, primary_key=True, default=uuid.uuid4()),
        sa.Column("date_time", sa.TIMESTAMP, default=sa.func.now()),
        sa.Column("battle_map", sa.VARCHAR(BATTLE_MAP_LENGTH), nullable=True),
        sa.Column("faction_played", sa.VARCHAR),
        sa.Column("battle_type", sa.VARCHAR),
        sa.Column("player_br", sa.REAL(1), default=0.0),
        sa.Column("ceiling_br", sa.REAL(1), default=0.0),
        sa.Column("battle_won", sa.BOOLEAN, nullable=True, default=None),
        sa.Column("user_id", sa.UUID, sa.ForeignKey("users.id")),
    )


def downgrade() -> None:
    op.drop_table(TABLE_NAME)
