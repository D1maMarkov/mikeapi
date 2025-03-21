"""empty message

Revision ID: 631a90905d31
Revises: 2db64177002c
Create Date: 2025-03-17 18:49:09.801169

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '631a90905d31'
down_revision: Union[str, None] = '2db64177002c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('traderstatistics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('trader_id', sa.Integer(), nullable=True),
    sa.Column('cash_balance', sa.Float(), nullable=True),
    sa.Column('stock_balance', sa.Float(), nullable=True),
    sa.Column('active_lots', sa.Integer(), nullable=True),
    sa.Column('deals', sa.Integer(), nullable=True),
    sa.Column('trade_volume', sa.Float(), nullable=True),
    sa.Column('income', sa.Float(), nullable=True),
    sa.Column('yield_', sa.Float(), nullable=True),
    sa.Column('gain', sa.Float(), nullable=True),
    sa.Column('tickers', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['trader_id'], ['traders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_traderstatistics_id'), 'traderstatistics', ['id'], unique=False)
    op.add_column('settings', sa.Column('commission', sa.Float(), nullable=True))
    op.add_column('settings', sa.Column('start_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('settings', 'start_date')
    op.drop_column('settings', 'commission')
    op.drop_index(op.f('ix_traderstatistics_id'), table_name='traderstatistics')
    op.drop_table('traderstatistics')
    # ### end Alembic commands ###
