"""add plano_id to clientes table

Revision ID: 0002_add_plano_id_to_clientes
Revises: 0001_add_cliente_address_and_files
Create Date: 2026-01-16 14:50:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_add_plano_id_to_clientes'
down_revision = '0001_add_cliente_address_and_files'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add plano_id column to clientes table
    op.add_column('clientes', sa.Column('plano_id', sa.Integer(), nullable=True))


def downgrade() -> None:
    # Drop plano_id column from clientes table
    op.drop_column('clientes', 'plano_id')