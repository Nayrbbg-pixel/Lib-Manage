"""Add cover image support to the database

Revision ID: 4cda9dced959
Revises: 1af6204db18f
Create Date: 2024-12-23 14:14:09.474435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4cda9dced959'
down_revision: Union[str, None] = '1af6204db18f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('book', sa.Column('cover_image', sa.LargeBinary(), nullable=True))


def downgrade() -> None:
    pass
