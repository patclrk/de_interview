"""create dw_weather and weather schemas

Revision ID: 001
Revises:
Create Date: 2026-06-05

"""

from typing import Sequence, Union

from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS dw_weather")
    op.execute("CREATE SCHEMA IF NOT EXISTS weather")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS weather CASCADE")
    op.execute("DROP SCHEMA IF EXISTS dw_weather CASCADE")
