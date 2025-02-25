"""add schedule to notificitions

Revision ID: 4d7af0302f5e
Revises: 42298138ccdd
Create Date: 2025-02-25 10:49:11.156874

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

from app.bot.constants import NOTIFICATION_TYPE

# revision identifiers, used by Alembic.
revision: str = "4d7af0302f5e"
down_revision: Union[str, None] = "42298138ccdd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "schedules",
        sa.Column(
            "notice_type",
            sqlalchemy_utils.types.choice.ChoiceType(NOTIFICATION_TYPE),
            nullable=False,
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("schedule", sa.JSON(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("notifications")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "notifications",
        sa.Column(
            "notice_type",
            sa.VARCHAR(length=255),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "user_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="notifications_user_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="notifications_pkey"),
    )
    op.drop_table("schedules")
    # ### end Alembic commands ###
