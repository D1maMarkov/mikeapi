"""empty message

Revision ID: bae1a85b2940
Revises: 43f0eb1f65f6
Create Date: 2025-03-02 23:47:51.264182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bae1a85b2940'
down_revision: Union[str, None] = '43f0eb1f65f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alerts', sa.Column('pings_interval1', sa.Integer(), nullable=True))
    op.add_column('alerts', sa.Column('pings_interval2', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('alerts', 'pings_interval2')
    op.drop_column('alerts', 'pings_interval1')
    # ### end Alembic commands ###
