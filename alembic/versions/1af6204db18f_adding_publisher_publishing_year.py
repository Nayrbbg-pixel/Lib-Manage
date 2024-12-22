"""Adding publisher, publishing year

Revision ID: 1af6204db18f
Revises: a0121caa3394
Create Date: 2024-12-22 21:08:05.787799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1af6204db18f'
down_revision: Union[str, None] = 'a0121caa3394'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('book', sa.Column('publisher', sa.String(), nullable=True))
    op.add_column('book', sa.Column('publishing_year', sa.Integer(), nullable=True))


def downgrade() -> None:
    pass
