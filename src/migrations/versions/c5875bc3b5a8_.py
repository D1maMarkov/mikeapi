"""empty message

Revision ID: c5875bc3b5a8
Revises: ff37b98a1d56
Create Date: 2025-01-20 02:07:51.480108

"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c5875bc3b5a8"
down_revision: str | None = "ff37b98a1d56"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("tickers", sa.Column("slug", sa.String(), nullable=True))
    op.create_index(op.f("ix_tickers_slug"), "tickers", ["slug"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_tickers_slug"), table_name="tickers")
    op.drop_column("tickers", "slug")
    # ### end Alembic commands ###
