"""empty message

Revision ID: cd645c6a1a08
Revises: e3d62ec9e0ac
Create Date: 2024-12-13 17:08:27.241153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd645c6a1a08'
down_revision: Union[str, None] = 'e3d62ec9e0ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('book','user_id')


def downgrade() -> None:
    pass
