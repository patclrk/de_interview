"""create dw_weather.precipitation_readings table

Revision ID: 003
Revises: 002
Create Date: 2026-09-08

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "precipitation_readings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column("precipitation", sa.Float(), nullable=False),
        sa.Column(
            "recorded_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("flow_run_id", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="dw_weather",
    )


def downgrade() -> None:
    op.drop_table("precipitation_readings", schema="dw_weather")
