"""
Merge heads: 002 and efgh5678

Revision ID: 0012_merge_heads
Revises: 002, efgh5678
Create Date: 2026-02-05 00:00:00.000000
"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '0012_merge_heads'
down_revision = ('002', 'efgh5678')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
