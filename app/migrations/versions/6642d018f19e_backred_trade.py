"""backred trade

Revision ID: 6642d018f19e
Revises: 5f0247369176
Create Date: 2025-03-04 21:44:47.238769

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision: str = "6642d018f19e"
down_revision: Union[str, None] = "5f0247369176"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "trades_sale_code_id_fkey", "trades", type_="foreignkey"
    )
    op.create_foreign_key(
        None,
        "trades",
        "sale_codes",
        ["sale_code_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "trades", type_="foreignkey")
    op.create_foreign_key(
        "trades_sale_code_id_fkey",
        "trades",
        "sale_codes",
        ["sale_code_id"],
        ["id"],
    )
    # ### end Alembic commands ###
