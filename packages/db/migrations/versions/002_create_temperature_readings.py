"""create dw_weather.temperature_readings table

Revision ID: 002
Revises: 001
Create Date: 2026-06-05

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "temperature_readings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column("temperature_f", sa.Float(), nullable=False),
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
    op.drop_table("temperature_readings", schema="dw_weather")
