"""Add user id

Revision ID: 54584ee2a786
Revises: e9176476cea9
Create Date: 2024-12-13 12:56:23.446665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54584ee2a786'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('book',sa.Column('user_id',sa.Integer,sa.ForeignKey('user.id')))

def downgrade() -> None:
    pass
