"""delete orphan

Revision ID: 2e3ef6a17a3b
Revises: 8a366f4e395c
Create Date: 2025-03-04 20:35:16.363656

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision: str = "2e3ef6a17a3b"
down_revision: Union[str, None] = "8a366f4e395c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
