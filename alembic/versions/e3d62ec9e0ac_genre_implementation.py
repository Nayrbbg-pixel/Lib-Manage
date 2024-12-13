"""Genre implementation

Revision ID: e3d62ec9e0ac
Revises: 54584ee2a786
Create Date: 2024-12-13 13:24:42.654973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3d62ec9e0ac'
down_revision: Union[str, None] = '54584ee2a786'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('book',sa.Column('genre',sa.String))


def downgrade() -> None:
    pass
