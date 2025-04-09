"""bigint for user-tg-id

Revision ID: c1687c6d3f1e
Revises: cb2f1d8e3312
Create Date: 2025-04-09 22:09:13.553094

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision: str = "c1687c6d3f1e"
down_revision: Union[str, None] = "cb2f1d8e3312"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "trades_sale_code_id_fkey", "trades", type_="foreignkey"
    )
    op.alter_column(
        "users",
        "telegram_id",
        existing_type=sa.INTEGER(),
        type_=sa.BigInteger(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "telegram_id",
        existing_type=sa.BigInteger(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.create_foreign_key(
        "trades_sale_code_id_fkey1",
        "trades",
        "sale_codes",
        ["sale_code_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###
