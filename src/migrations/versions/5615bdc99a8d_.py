"""empty message

Revision ID: 5615bdc99a8d
Revises:
Create Date: 2025-01-08 22:28:18.109194

"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5615bdc99a8d"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "main_url",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("main_url", sa.String(), nullable=True),
        sa.Column(
            "main_url_status",
            sa.Enum("in_work", "unavailable", "error", "failure", name="urlenum", native_enum=False),
            nullable=True,
        ),
        sa.Column("reverse_url", sa.String(), nullable=True),
        sa.Column(
            "reverse_url_status",
            sa.Enum("in_work", "unavailable", "error", "failure", name="urlenum", native_enum=False),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_main_url_id"), "main_url", ["id"], unique=False)
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("hash_password", sa.String(), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_table(
        "vendors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("app_id", sa.String(), nullable=True),
        sa.Column("auth_token", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_vendors_id"), "vendors", ["id"], unique=False)
    op.create_table(
        "log",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("app_id", sa.Integer(), nullable=True),
        sa.Column("text", sa.String(), nullable=True),
        sa.Column("time", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("main_server", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["app_id"],
            ["vendors.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_log_id"), "log", ["id"], unique=False)
    #op.drop_index("ix_reverse_url_id", table_name="reverse_url")
    #op.drop_table("reverse_url")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "reverse_url",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("url", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="reverse_url_pkey"),
    )
    op.create_index("ix_reverse_url_id", "reverse_url", ["id"], unique=False)
    op.drop_index(op.f("ix_log_id"), table_name="log")
    op.drop_table("log")
    op.drop_index(op.f("ix_vendors_id"), table_name="vendors")
    op.drop_table("vendors")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_main_url_id"), table_name="main_url")
    op.drop_table("main_url")
    # ### end Alembic commands ###
