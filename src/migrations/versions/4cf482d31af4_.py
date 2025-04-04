"""empty message

Revision ID: 4cf482d31af4
Revises: fd013c350e2e
Create Date: 2025-03-22 04:42:29.529013

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4cf482d31af4'
down_revision: Union[str, None] = 'fd013c350e2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('traderstatistics', sa.Column('cash_balance_degrees', sa.Float(), nullable=True))
    op.add_column('traderstatistics', sa.Column('stock_balance_degrees', sa.Float(), nullable=True))
    op.add_column('traderstatistics', sa.Column('active_lots_degrees', sa.Integer(), nullable=True))
    op.add_column('traderstatistics', sa.Column('deals_degrees', sa.Integer(), nullable=True))
    op.add_column('traderstatistics', sa.Column('trade_volume_degrees', sa.Float(), nullable=True))
    op.add_column('traderstatistics', sa.Column('income_degrees', sa.Float(), nullable=True))
    op.add_column('traderstatistics', sa.Column('yield_degrees', sa.Float(), nullable=True))
    op.add_column('traderstatistics', sa.Column('gain_degrees', sa.Float(), nullable=True))
    op.add_column('traderstatistics', sa.Column('tickers_degrees', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('traderstatistics', 'tickers_degrees')
    op.drop_column('traderstatistics', 'gain_degrees')
    op.drop_column('traderstatistics', 'yield_degrees')
    op.drop_column('traderstatistics', 'income_degrees')
    op.drop_column('traderstatistics', 'trade_volume_degrees')
    op.drop_column('traderstatistics', 'deals_degrees')
    op.drop_column('traderstatistics', 'active_lots_degrees')
    op.drop_column('traderstatistics', 'stock_balance_degrees')
    op.drop_column('traderstatistics', 'cash_balance_degrees')
    # ### end Alembic commands ###
