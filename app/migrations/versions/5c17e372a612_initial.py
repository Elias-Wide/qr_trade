"""Initial

Revision ID: 5c17e372a612
Revises: 
Create Date: 2025-02-04 21:24:15.366703

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5c17e372a612"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "sale_codes", "user_id", existing_type=sa.INTEGER(), nullable=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "sale_codes", "user_id", existing_type=sa.INTEGER(), nullable=True
    )
    # ### end Alembic commands ###
