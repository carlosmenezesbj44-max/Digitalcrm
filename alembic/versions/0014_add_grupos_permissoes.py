"""
Add grupos e relacionamentos de permissoes

Revision ID: 0014_add_grupos_permissoes
Revises: 0013_add_usuario_preferencias
Create Date: 2026-02-05 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0014_add_grupos_permissoes'
down_revision = '0013_add_usuario_preferencias'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = inspector.get_table_names()

    if 'grupo' not in tables:
        op.create_table(
            'grupo',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('nome', sa.String(length=100), nullable=False, unique=True),
            sa.Column('descricao', sa.String(length=255), nullable=True),
            sa.Column('criado_em', sa.DateTime(), nullable=True),
        )

    if 'grupo_permissao' not in tables:
        op.create_table(
            'grupo_permissao',
            sa.Column('grupo_id', sa.Integer(), sa.ForeignKey('grupo.id')),
            sa.Column('permissao_id', sa.Integer(), sa.ForeignKey('permissao.id')),
        )

    if 'usuario_grupo' not in tables:
        op.create_table(
            'usuario_grupo',
            sa.Column('usuario_id', sa.Integer(), sa.ForeignKey('usuario.id')),
            sa.Column('grupo_id', sa.Integer(), sa.ForeignKey('grupo.id')),
        )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = inspector.get_table_names()

    if 'usuario_grupo' in tables:
        op.drop_table('usuario_grupo')
    if 'grupo_permissao' in tables:
        op.drop_table('grupo_permissao')
    if 'grupo' in tables:
        op.drop_table('grupo')
