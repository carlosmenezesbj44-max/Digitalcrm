"""
Add foto_url to usuario

Revision ID: 0011_add_usuario_foto_url
Revises: 0010_add_cliente_produtos_table
Create Date: 2026-02-04 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0011_add_usuario_foto_url'
down_revision = '0010_add_cliente_produtos_table'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [col['name'] for col in inspector.get_columns('usuario')]
    if 'foto_url' not in columns:
        op.add_column('usuario', sa.Column('foto_url', sa.String(length=255), nullable=True))


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [col['name'] for col in inspector.get_columns('usuario')]
    if 'foto_url' in columns:
        with op.batch_alter_table('usuario') as batch_op:
            batch_op.drop_column('foto_url')
