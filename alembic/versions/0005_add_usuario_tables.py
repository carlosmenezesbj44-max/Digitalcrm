"""Add usuario tables

Revision ID: 0005
Revises: 0003_add_ordens_servico_table, 0004
Create Date: 2026-01-18 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0005'
down_revision = ('0003_add_ordens_servico_table', '0004')
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create usuario table
    op.create_table(
        'usuario',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('senha_hash', sa.String(255), nullable=False),
        sa.Column('nome_completo', sa.String(100), nullable=False),
        sa.Column('ativo', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('role', sa.String(20), nullable=True, server_default='cliente'),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
        sa.Column('atualizado_em', sa.DateTime(), nullable=True),
        sa.Column('ultimo_acesso', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_usuario_id'), 'usuario', ['id'], unique=False)
    op.create_index(op.f('ix_usuario_username'), 'usuario', ['username'], unique=True)
    op.create_index(op.f('ix_usuario_email'), 'usuario', ['email'], unique=True)

    # Create permissao table
    op.create_table(
        'permissao',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(100), nullable=False),
        sa.Column('descricao', sa.String(255), nullable=True),
        sa.Column('modulo', sa.String(50), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nome')
    )
    op.create_index(op.f('ix_permissao_id'), 'permissao', ['id'], unique=False)

    # Create usuario_permissao table (many-to-many)
    op.create_table(
        'usuario_permissao',
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('permissao_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
        sa.ForeignKeyConstraint(['permissao_id'], ['permissao.id'], ),
        sa.PrimaryKeyConstraint('usuario_id', 'permissao_id')
    )

    # Create auditoria_log table
    op.create_table(
        'auditoria_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('acao', sa.String(100), nullable=True),
        sa.Column('recurso', sa.String(100), nullable=True),
        sa.Column('detalhes', sa.String(500), nullable=True),
        sa.Column('ip_address', sa.String(50), nullable=True),
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
