"""unique login

Revision ID: c1646269115a
Revises: 021e505593cf
Create Date: 2025-05-04 19:01:20.696826

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c1646269115a"
down_revision: Union[str, None] = "021e505593cf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["login"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
