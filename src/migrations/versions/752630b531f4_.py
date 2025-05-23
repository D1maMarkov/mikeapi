"""empty message

Revision ID: 752630b531f4
Revises: 13c9f1fc78a8
Create Date: 2025-04-30 16:16:51.516046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '752630b531f4'
down_revision: Union[str, None] = '13c9f1fc78a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('packages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('signal_ids', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('device_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['vendors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_packages_id'), 'packages', ['id'], unique=False)
    op.add_column('log', sa.Column('adopted', sa.Boolean(), nullable=True))
    op.add_column('log', sa.Column('adopted_device_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'log', 'vendors', ['adopted_device_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'log', type_='foreignkey')
    op.drop_column('log', 'adopted_device_id')
    op.drop_column('log', 'adopted')
    op.drop_index(op.f('ix_packages_id'), table_name='packages')
    op.drop_table('packages')
    # ### end Alembic commands ###
