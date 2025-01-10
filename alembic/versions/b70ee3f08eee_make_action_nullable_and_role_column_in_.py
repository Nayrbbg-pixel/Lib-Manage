"""Make action nullable and role column in action recorder

Revision ID: b70ee3f08eee
Revises: 
Create Date: 2025-01-10 20:54:28.363607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b70ee3f08eee'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from models import Role

def upgrade() -> None:
    op.add_column('user_record_details',sa.Column('method',sa.String,nullable=False))

def downgrade() -> None:
    pass
