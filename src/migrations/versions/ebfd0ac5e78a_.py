"""empty message

Revision ID: ebfd0ac5e78a
Revises: 2121e0cf2d06
Create Date: 2025-01-12 23:48:11.119958

"""
from typing import Union
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ebfd0ac5e78a"
down_revision: str | None = "2121e0cf2d06"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("traders", sa.Column("app_id", sa.Integer(), nullable=True))
    op.alter_column("traders", "portfolio", existing_type=sa.INTEGER(), type_=sa.String(), existing_nullable=True)
    op.create_foreign_key(None, "traders", "vendors", ["app_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "traders", type_="foreignkey")
    op.alter_column("traders", "portfolio", existing_type=sa.String(), type_=sa.INTEGER(), existing_nullable=True)
    op.drop_column("traders", "app_id")
    # ### end Alembic commands ###