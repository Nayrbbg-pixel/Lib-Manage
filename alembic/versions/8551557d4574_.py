"""Add username and role column to query table

Revision ID: 8551557d4574
Revises: 4cda9dced959
Create Date: 2025-01-06 21:51:12.651127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8551557d4574'
down_revision: Union[str, None] = '4cda9dced959'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('query', sa.Column('username', sa.String(), nullable=False))


def downgrade() -> None:
    pass
