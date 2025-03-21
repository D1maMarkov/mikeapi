"""empty message

Revision ID: 2db64177002c
Revises: 56e5938a0783
Create Date: 2025-03-08 16:43:24.558400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2db64177002c'
down_revision: Union[str, None] = '56e5938a0783'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_traders_username', table_name='traders')
    op.create_unique_constraint(None, 'traders', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'traders', type_='unique')
    op.create_index('ix_traders_username', 'traders', ['username'], unique=True)
    # ### end Alembic commands ###
