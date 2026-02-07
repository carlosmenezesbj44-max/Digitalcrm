"""add timeline fields to ordens servico

Revision ID: 0015
Revises: 0014
Create Date: 2024-XX-XX

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0015'
down_revision = '0014'
branch_labels = None
depends_on = None


def upgrade():
    # Adicionar campos data_inicio e data_aguardando_peca
    op.add_column('ordens_servico', sa.Column('data_inicio', sa.DateTime(), nullable=True))
    op.add_column('ordens_servico', sa.Column('data_aguardando_peca', sa.DateTime(), nullable=True))
    
    # Atualizar status para incluir aguardando_peca
    op.execute("UPDATE ordens_servico SET status = 'aguardando_peca' WHERE status = 'aguardando_peca'")


def downgrade():
    op.drop_column('ordens_servico', 'data_aguardando_peca')
    op.drop_column('ordens_servico', 'data_inicio')
