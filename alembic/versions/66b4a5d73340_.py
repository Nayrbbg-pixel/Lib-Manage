"""Add user_id to QueryResponse

Revision ID: 66b4a5d73340
Revises: 8551557d4574
Create Date: 2025-01-07 22:03:07.547741

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66b4a5d73340'
down_revision: Union[str, None] = '8551557d4574'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('query_response','user_id')
    op.add_column('query_response', sa.Column('user_id',sa.Integer,sa.ForeignKey('user.id')))

def downgrade() -> None:
    pass
