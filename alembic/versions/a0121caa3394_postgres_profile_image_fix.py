"""Postgres profile image fix

Revision ID: a0121caa3394
Revises: 3f6b625a23f1
Create Date: 2024-12-21 22:45:43.746537

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0121caa3394'
down_revision: Union[str, None] = '3f6b625a23f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('profile_image',sa.Column('image_data',sa.LargeBinary,nullable=True))


def downgrade() -> None:
    pass
