"""change trades

Revision ID: 09cc45a59765
Revises: 5c17e372a612
Create Date: 2025-02-04 21:28:56.777011

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "09cc45a59765"
down_revision: Union[str, None] = "5c17e372a612"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "sale_codes_user_id_fkey", "sale_codes", type_="foreignkey"
    )
    op.drop_column("sale_codes", "user_id")
    op.drop_column("trades", "file_name")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "trades",
        sa.Column(
            "file_name", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "sale_codes",
        sa.Column(
            "user_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
    op.create_foreign_key(
        "sale_codes_user_id_fkey", "sale_codes", "users", ["user_id"], ["id"]
    )
    # ### end Alembic commands ###
