"""Add payment-related fields to contratos table

Revision ID: 0008_add_payment_fields_to_contratos
Revises: 0007_add_missing_contratos_columns
Create Date: 2026-01-23 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0008_add_payment_fields_to_contratos'
down_revision = '0007_add_missing_contratos_columns'
branch_labels = None
depends_on = None


def upgrade():
    # Add payment-related columns to contratos table
    with op.batch_alter_table('contratos', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('data_primeiro_pagamento', sa.DateTime, nullable=True)
        )
        batch_op.add_column(
            sa.Column('data_proximo_pagamento', sa.DateTime, nullable=True)
        )
        batch_op.add_column(
            sa.Column('dia_pagamento', sa.Integer, server_default='10', nullable=False)
        )
        batch_op.add_column(
            sa.Column('frequencia_pagamento', sa.String(50), server_default='mensal', nullable=False)
        )
        batch_op.add_column(
            sa.Column('desconto_total', sa.Float, server_default='0', nullable=False)
        )
        batch_op.add_column(
            sa.Column('juros_atraso_percentual', sa.Float, server_default='1', nullable=False)
        )


def downgrade():
    with op.batch_alter_table('contratos', schema=None) as batch_op:
        batch_op.drop_column('data_primeiro_pagamento')
        batch_op.drop_column('data_proximo_pagamento')
        batch_op.drop_column('dia_pagamento')
        batch_op.drop_column('frequencia_pagamento')
        batch_op.drop_column('desconto_total')
        batch_op.drop_column('juros_atraso_percentual')
