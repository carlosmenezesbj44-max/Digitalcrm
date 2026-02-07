"""Create usuario tables

Revision ID: 0006
Revises: 0005
Create Date: 2026-01-18 16:52:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0006'
down_revision: Union[str, None] = '0005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criar tabela usuario
    op.create_table(
        'usuario',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('senha_hash', sa.String(length=255), nullable=False),
        sa.Column('nome_completo', sa.String(length=100), nullable=False),
        sa.Column('ativo', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('role', sa.String(length=20), nullable=True, server_default=sa.text("'cliente'")),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
        sa.Column('atualizado_em', sa.DateTime(), nullable=True),
        sa.Column('ultimo_acesso', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_usuario_id'), 'usuario', ['id'], unique=False)
    op.create_index(op.f('ix_usuario_username'), 'usuario', ['username'], unique=True)
    op.create_index(op.f('ix_usuario_email'), 'usuario', ['email'], unique=True)
    
    # Criar tabela permissao
    op.create_table(
        'permissao',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('descricao', sa.String(length=255), nullable=True),
        sa.Column('modulo', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nome')
    )
    op.create_index(op.f('ix_permissao_id'), 'permissao', ['id'], unique=False)
    
    # Criar tabela usuario_permissao
    op.create_table(
        'usuario_permissao',
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('permissao_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['permissao_id'], ['permissao.id'], ),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
        sa.PrimaryKeyConstraint('usuario_id', 'permissao_id')
    )
    
    # Criar tabela auditoria_log
    op.create_table(
        'auditoria_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('acao', sa.String(length=100), nullable=True),
        sa.Column('recurso', sa.String(length=100), nullable=True),
        sa.Column('detalhes', sa.String(length=500), nullable=True),
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_auditoria_log_id'), 'auditoria_log', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_auditoria_log_id'), table_name='auditoria_log')
    op.drop_table('auditoria_log')
    op.drop_table('usuario_permissao')
    op.drop_index(op.f('ix_permissao_id'), table_name='permissao')
    op.drop_table('permissao')
    op.drop_index(op.f('ix_usuario_email'), table_name='usuario')
    op.drop_index(op.f('ix_usuario_username'), table_name='usuario')
    op.drop_index(op.f('ix_usuario_id'), table_name='usuario')
    op.drop_table('usuario')
