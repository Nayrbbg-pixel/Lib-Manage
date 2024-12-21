"""Description and Language

Revision ID: 3f6b625a23f1
Revises: cd645c6a1a08
Create Date: 2024-12-21 14:05:00.734560

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f6b625a23f1'
down_revision: Union[str, None] = 'cd645c6a1a08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('book',sa.Column('description',sa.String))
    op.add_column('book',sa.Column('language',sa.String))

def downgrade() -> None:
    pass
