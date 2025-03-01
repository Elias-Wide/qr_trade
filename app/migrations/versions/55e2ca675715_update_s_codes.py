"""update s_codes

Revision ID: 55e2ca675715
Revises: c5cecba5f1d2
Create Date: 2025-02-28 22:16:46.517226

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision: str = "55e2ca675715"
down_revision: Union[str, None] = "c5cecba5f1d2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "sale_codes", sa.Column("client_id", sa.String(), nullable=False)
    )
    op.add_column(
        "sale_codes", sa.Column("encoded_value", sa.String(), nullable=False)
    )
    op.drop_constraint("sale_codes_value_key", "sale_codes", type_="unique")
    op.drop_constraint(
        "unique_user_id_and_value", "sale_codes", type_="unique"
    )
    op.create_unique_constraint(
        "unique_user_and_client_id", "sale_codes", ["user_id", "client_id"]
    )
    op.create_unique_constraint(None, "sale_codes", ["client_id"])
    op.drop_column("sale_codes", "value")
    op.drop_column("sale_codes", "file_name")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "sale_codes",
        sa.Column(
            "file_name", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "sale_codes",
        sa.Column("value", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "sale_codes", type_="unique")
    op.drop_constraint(
        "unique_user_and_client_id", "sale_codes", type_="unique"
    )
    op.create_unique_constraint(
        "unique_user_id_and_value", "sale_codes", ["user_id", "value"]
    )
    op.create_unique_constraint(
        "sale_codes_value_key", "sale_codes", ["value"]
    )
    op.drop_column("sale_codes", "encoded_value")
    op.drop_column("sale_codes", "client_id")
    # ### end Alembic commands ###
