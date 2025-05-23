"""empty message

Revision ID: 96557918d549
Revises: e74212f1e169
Create Date: 2025-01-31 00:40:58.036497

"""
from typing import Union
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "96557918d549"
down_revision: str | None = "e74212f1e169"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "tickers", "lot", existing_type=sa.DOUBLE_PRECISION(precision=53), type_=sa.Integer(), existing_nullable=True
    )
    op.alter_column("tickers", "last_trade_price", existing_type=sa.INTEGER(), type_=sa.Float(), existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("tickers", "last_trade_price", existing_type=sa.Float(), type_=sa.INTEGER(), existing_nullable=True)
    op.alter_column(
        "tickers", "lot", existing_type=sa.Integer(), type_=sa.DOUBLE_PRECISION(precision=53), existing_nullable=True
    )
    # ### end Alembic commands ###
