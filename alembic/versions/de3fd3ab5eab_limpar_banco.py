"""Limpar banco

Revision ID: de3fd3ab5eab
Revises: 6b0ef88eec38
Create Date: 2024-03-09 21:36:34.932267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de3fd3ab5eab'
down_revision = '6b0ef88eec38'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Limpar todas as tabelas
    op.execute('DELETE FROM historico')
    op.execute('DELETE FROM vagas')
    op.execute('DELETE FROM veiculos')
    op.execute('DELETE FROM funcionarios')


def downgrade() -> None:
    pass