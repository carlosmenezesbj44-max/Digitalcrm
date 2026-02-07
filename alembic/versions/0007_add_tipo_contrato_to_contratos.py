"""Add missing columns to contratos table

Revision ID: 0007_add_missing_contratos_columns
Revises: 0006_create_usuario_tables
Create Date: 2026-01-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '0007_add_missing_contratos_columns'
down_revision = '0006'
branch_labels = None
depends_on = None


def upgrade():
    # Add missing columns to contratos table
    with op.batch_alter_table('contratos', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('tipo_contrato', sa.String(50), server_default='servico', nullable=False)
        )
        batch_op.add_column(
            sa.Column('data_vigencia_inicio', sa.DateTime, nullable=True)
        )
        batch_op.add_column(
            sa.Column('data_vigencia_fim', sa.DateTime, nullable=True)
        )
        batch_op.add_column(
            sa.Column('data_notificacao_renovacao', sa.DateTime, nullable=True)
        )
        batch_op.add_column(
            sa.Column('valor_contrato', sa.Float, nullable=True)
        )
        batch_op.add_column(
            sa.Column('moeda', sa.String(3), server_default='BRL', nullable=False)
        )
        batch_op.add_column(
            sa.Column('status_renovacao', sa.String(50), server_default='renovacao_manual', nullable=False)
        )
        batch_op.add_column(
            sa.Column('proximo_contrato_id', sa.Integer, sa.ForeignKey('contratos.id'), nullable=True)
        )
        batch_op.add_column(
            sa.Column('criado_por', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('criado_em', sa.DateTime, server_default=sa.func.now(), nullable=False)
        )
        batch_op.add_column(
            sa.Column('atualizado_por', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('atualizado_em', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
        )
        batch_op.add_column(
            sa.Column('deletado_em', sa.DateTime, nullable=True)
        )


def downgrade():
    with op.batch_alter_table('contratos', schema=None) as batch_op:
        batch_op.drop_column('tipo_contrato')
        batch_op.drop_column('data_vigencia_inicio')
        batch_op.drop_column('data_vigencia_fim')
        batch_op.drop_column('data_notificacao_renovacao')
        batch_op.drop_column('valor_contrato')
        batch_op.drop_column('moeda')
        batch_op.drop_column('status_renovacao')
        batch_op.drop_column('proximo_contrato_id')
        batch_op.drop_column('criado_por')
        batch_op.drop_column('criado_em')
        batch_op.drop_column('atualizado_por')
        batch_op.drop_column('atualizado_em')
        batch_op.drop_column('deletado_em')
