"""empty message

Revision ID: 8d0f05d87c5e
Revises: ebfd0ac5e78a
Create Date: 2025-01-18 22:37:15.539665

"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8d0f05d87c5e"
down_revision: str | None = "ebfd0ac5e78a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "logsactivity",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("time", sa.Time(), nullable=True),
        sa.Column("last_hour", sa.Integer(), nullable=True),
        sa.Column("last_day", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_logsactivity_id"), "logsactivity", ["id"], unique=False)
    op.create_index(op.f("ix_log_created_at"), "log", ["created_at"], unique=False)
    op.drop_column("log", "text")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("log", sa.Column("text", sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f("ix_log_created_at"), table_name="log")
    op.drop_index(op.f("ix_logsactivity_id"), table_name="logsactivity")
    op.drop_table("logsactivity")
    # ### end Alembic commands ###