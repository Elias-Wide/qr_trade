"""add value into sale_codes model

Revision ID: 3cc50383497e
Revises: 980819cd0ea1
Create Date: 2025-02-11 16:16:54.353148

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3cc50383497e"
down_revision: Union[str, None] = "980819cd0ea1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "sale_codes", sa.Column("value", sa.String(), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("sale_codes", "value")
    # ### end Alembic commands ###
