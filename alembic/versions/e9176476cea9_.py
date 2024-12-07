"""empty message

Revision ID: e9176476cea9
Revises: 
Create Date: 2024-12-07 13:18:30.947608

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9176476cea9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('user','email')


def downgrade() -> None:
    pass
