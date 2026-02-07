"""Add cliente_produtos table for many-to-many relationship

Revision ID: 0010_add_cliente_produtos_table
Revises: 0009_add_missing_clientes_columns
Create Date: 2026-02-03 21:58:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0010_add_cliente_produtos_table'
down_revision = '0009_add_missing_clientes_columns'
branch_labels = None
depends_on = None


def upgrade():
    # Create cliente_produtos table for many-to-many relationship
    op.create_table(
        'cliente_produtos',
        sa.Column('cliente_id', sa.Integer, sa.ForeignKey('clientes.id'), primary_key=True),
        sa.Column('produto_id', sa.Integer, sa.ForeignKey('produtos.id'), primary_key=True),
        sa.Column('data_vinculo', sa.DateTime, default=sa.text('CURRENT_TIMESTAMP'))
    )


def downgrade():
    op.drop_table('cliente_produtos')