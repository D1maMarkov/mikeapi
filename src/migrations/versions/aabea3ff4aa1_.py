"""empty message

Revision ID: aabea3ff4aa1
Revises: 787a74ff1165
Create Date: 2025-02-11 22:57:35.271149

"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aabea3ff4aa1"
down_revision: str | None = "787a74ff1165"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("traders", sa.Column("scanned", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("traders", "scanned")
    # ### end Alembic commands ###
