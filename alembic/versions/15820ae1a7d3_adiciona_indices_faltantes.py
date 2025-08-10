"""adiciona_indices_faltantes

Revision ID: 15820ae1a7d3
Revises: de3fd3ab5eab
Create Date: 2025-08-10 08:08:59.855606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15820ae1a7d3'
down_revision: Union[str, Sequence[str], None] = 'de3fd3ab5eab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
