"""initial db models done

Revision ID: fd38ee535c83
Revises: 
Create Date: 2025-03-18 15:32:19.321338

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

from app.core.constants import NOTIFICATION_TYPE


# revision identifiers, used by Alembic.
revision: str = "fd38ee535c83"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "acces_codes",
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("limit", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "regions",
        sa.Column("ceo_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "points",
        sa.Column("addres", sa.String(), nullable=False),
        sa.Column("point_id", sa.Integer(), nullable=False),
        sa.Column("region_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("point_id"),
    )
    op.create_table(
        "users",
        sa.Column("telegram_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("ban", sa.BOOLEAN(), nullable=True),
        sa.Column("manager_id", sa.Integer(), nullable=False),
        sa.Column("point_id", sa.Integer(), nullable=True),
        sa.Column("timezone", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("manager_id"),
        sa.UniqueConstraint("telegram_id"),
    )
    op.create_table(
        "sale_codes",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.Date(), nullable=True),
        sa.Column("client_id", sa.String(), nullable=False),
        sa.Column("encoded_value", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("client_id"),
        sa.UniqueConstraint(
            "user_id", "client_id", name="unique_user_and_client_id"
        ),
    )
    op.create_table(
        "schedules",
        sa.Column(
            "notice_type",
            sqlalchemy_utils.types.choice.ChoiceType(NOTIFICATION_TYPE),
            nullable=True,
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("schedule", sa.ARRAY(sa.Date()), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "trades",
        sa.Column("sale_code_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("point_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.Date(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sale_code_id", "id", name="unique_sale_code_id"),
        sa.UniqueConstraint(
            "sale_code_id",
            "user_id",
            "point_id",
            name="unique_user_point_sale_code_id",
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("trades")
    op.drop_table("schedules")
    op.drop_table("sale_codes")
    op.drop_table("users")
    op.drop_table("regions")
    op.drop_table("points")
    op.drop_table("acces_codes")
    # ### end Alembic commands ###
