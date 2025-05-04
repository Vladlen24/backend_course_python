"""add users

Revision ID: 021e505593cf
Revises: 5bb2b6e04233
Create Date: 2025-05-04 14:11:22.946851

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "021e505593cf"
down_revision: Union[str, None] = "5bb2b6e04233"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("login", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
