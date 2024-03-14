"""role seeders

Revision ID: 19a7fc367206
Revises: 3a05bf9ea158
Create Date: 2024-03-14 15:35:16.498054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.api.models.role import Role


# revision identifiers, used by Alembic.
revision: str = '19a7fc367206'
down_revision: Union[str, None] = '3a05bf9ea158'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Seed the Role table
    op.bulk_insert(
        Role.__table__,
        [
            {'name': 'ROLE_USER', 'description': 'The default role for a new user'},
            {'name': 'ROLE_ADMIN', 'description': 'The role for the administrator'}
        ]
    )


def downgrade() -> None:
    # Remove the Role table data
    op.execute(Role.__table__.delete())