"""
Add preferencias to usuario

Revision ID: 0013_add_usuario_preferencias
Revises: 0012_merge_heads
Create Date: 2026-02-05 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0013_add_usuario_preferencias'
down_revision = '0012_merge_heads'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [col['name'] for col in inspector.get_columns('usuario')]
    if 'preferencias' not in columns:
        op.add_column('usuario', sa.Column('preferencias', sa.Text(), nullable=True))


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [col['name'] for col in inspector.get_columns('usuario')]
    if 'preferencias' in columns:
        with op.batch_alter_table('usuario') as batch_op:
            batch_op.drop_column('preferencias')
