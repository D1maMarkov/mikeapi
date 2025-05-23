"""empty message

Revision ID: 4ae4d53cf102
Revises: 69a856acc69b
Create Date: 2025-03-26 12:31:52.344740

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ae4d53cf102'
down_revision: Union[str, None] = '69a856acc69b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('log', sa.Column('end_deal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'log', 'log', ['end_deal_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'log', type_='foreignkey')
    op.drop_column('log', 'end_deal_id')
    # ### end Alembic commands ###
