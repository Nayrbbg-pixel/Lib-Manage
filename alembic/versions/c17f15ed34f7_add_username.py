"""Add username

Revision ID: c17f15ed34f7
Revises: b70ee3f08eee
Create Date: 2025-01-11 00:23:18.904926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c17f15ed34f7'
down_revision: Union[str, None] = 'b70ee3f08eee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('query_response',sa.Column('username',sa.String))


def downgrade() -> None:
    pass
