"""create user table

Revision ID: f9f9c9dbc6fb
Revises: 
Create Date: 2024-06-29 15:54:58.463081

"""

from typing import Sequence, Union
import uuid
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f9f9c9dbc6fb"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
TABLE_NAME = "users"
EMAIL_LENGTH = 30
PWD_LENGTH = 64


def upgrade() -> None:
    op.create_table(
        TABLE_NAME,
        sa.Column("id", sa.UUID, primary_key=True, default=uuid.uuid4),
        sa.Column("email", sa.VARCHAR(EMAIL_LENGTH), unique=True, index=True),
        sa.Column("hashed_pwd", sa.VARCHAR(PWD_LENGTH)),
        sa.Column("battles", sa.ARRAY(sa.JSON), default=[]),
    )


def downgrade() -> None:
    op.drop_table(TABLE_NAME)
