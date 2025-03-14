"""update points

Revision ID: 1480aefec514
Revises: 6a7e3d40850a
Create Date: 2025-03-14 23:54:52.947283

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision: str = "1480aefec514"
down_revision: Union[str, None] = "6a7e3d40850a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("points_name_key", "points", type_="unique")
    op.drop_column("points", "name")
    op.drop_constraint(
        "sale_codes_user_id_fkey", "sale_codes", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "sale_codes", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.create_unique_constraint(
        "unique_user_point_sale_code_id",
        "trades",
        ["sale_code_id", "user_id", "point_id"],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "unique_user_point_sale_code_id", "trades", type_="unique"
    )
    op.drop_constraint(None, "sale_codes", type_="foreignkey")
    op.create_foreign_key(
        "sale_codes_user_id_fkey", "sale_codes", "users", ["user_id"], ["id"]
    )
    op.add_column(
        "points",
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.create_unique_constraint("points_name_key", "points", ["name"])
    # ### end Alembic commands ###
