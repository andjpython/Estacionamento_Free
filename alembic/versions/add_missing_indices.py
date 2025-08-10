"""Adiciona índices faltantes

Revision ID: add_missing_indices
Revises: 6b0ef88eec38
Create Date: 2024-03-09 21:00:00.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'add_missing_indices'
down_revision = '6b0ef88eec38'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Adicionar índice em cpf na tabela veiculos
    op.create_index(
        'ix_veiculos_cpf',
        'veiculos',
        ['cpf'],
        unique=False
    )

    # Adicionar índice em matricula na tabela historico
    op.create_index(
        'ix_historico_matricula',
        'historico',
        ['matricula'],
        unique=False
    )

def downgrade() -> None:
    op.drop_index('ix_historico_matricula', table_name='historico')
    op.drop_index('ix_veiculos_cpf', table_name='veiculos')

