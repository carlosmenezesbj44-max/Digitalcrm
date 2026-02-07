"""Create carnes, parcelas, and boletos tables

Revision ID: 002
Revises: 0011_add_usuario_foto_url
Create Date: 2024-01-18 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '0011_add_usuario_foto_url'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create carnes table
    op.create_table(
        'carnes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cliente_id', sa.Integer(), nullable=False),
        sa.Column('numero_carne', sa.String(), nullable=False),
        sa.Column('valor_total', sa.Float(), nullable=False),
        sa.Column('quantidade_parcelas', sa.Integer(), nullable=False),
        sa.Column('valor_parcela', sa.Float(), nullable=False),
        sa.Column('data_inicio', sa.Date(), nullable=False),
        sa.Column('data_primeiro_vencimento', sa.Date(), nullable=False),
        sa.Column('intervalo_dias', sa.Integer(), nullable=False, server_default='30'),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='ativo'),
        sa.Column('gerencianet_subscription_id', sa.String(), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('data_criacao', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('data_atualizacao', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('numero_carne')
    )
    op.create_index(op.f('ix_carnes_cliente_id'), 'carnes', ['cliente_id'], unique=False)
    op.create_index(op.f('ix_carnes_id'), 'carnes', ['id'], unique=False)

    # Create parcelas table
    op.create_table(
        'parcelas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('carne_id', sa.Integer(), nullable=False),
        sa.Column('numero_parcela', sa.Integer(), nullable=False),
        sa.Column('valor', sa.Float(), nullable=False),
        sa.Column('data_vencimento', sa.Date(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='pendente'),
        sa.Column('valor_pago', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('data_pagamento', sa.DateTime(), nullable=True),
        sa.Column('gerencianet_charge_id', sa.String(), nullable=True),
        sa.Column('gerencianet_link_boleto', sa.String(), nullable=True),
        sa.Column('codigo_barras', sa.String(), nullable=True),
        sa.Column('linha_digitavel', sa.String(), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('data_criacao', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['carne_id'], ['carnes.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_parcelas_carne_id'), 'parcelas', ['carne_id'], unique=False)
    op.create_index(op.f('ix_parcelas_id'), 'parcelas', ['id'], unique=False)

    # Create boletos table
    op.create_table(
        'boletos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cliente_id', sa.Integer(), nullable=False),
        sa.Column('fatura_id', sa.Integer(), nullable=True),
        sa.Column('parcela_id', sa.Integer(), nullable=True),
        sa.Column('numero_boleto', sa.String(), nullable=False),
        sa.Column('valor', sa.Float(), nullable=False),
        sa.Column('data_vencimento', sa.Date(), nullable=False),
        sa.Column('data_emissao', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('codigo_barras', sa.String(), nullable=True),
        sa.Column('linha_digitavel', sa.String(), nullable=True),
        sa.Column('url_boleto', sa.String(), nullable=True),
        sa.Column('gerencianet_charge_id', sa.String(), nullable=True),
        sa.Column('gerencianet_status', sa.String(), nullable=False, server_default='aberto'),
        sa.Column('status', sa.String(), nullable=False, server_default='pendente'),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('data_criacao', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('data_atualizacao', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id'], ),
        sa.ForeignKeyConstraint(['fatura_id'], ['faturas.id'], ),
        sa.ForeignKeyConstraint(['parcela_id'], ['parcelas.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('numero_boleto'),
        sa.UniqueConstraint('gerencianet_charge_id')
    )
    op.create_index(op.f('ix_boletos_cliente_id'), 'boletos', ['cliente_id'], unique=False)
    op.create_index(op.f('ix_boletos_fatura_id'), 'boletos', ['fatura_id'], unique=False)
    op.create_index(op.f('ix_boletos_id'), 'boletos', ['id'], unique=False)
    op.create_index(op.f('ix_boletos_parcela_id'), 'boletos', ['parcela_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_boletos_parcela_id'), table_name='boletos')
    op.drop_index(op.f('ix_boletos_id'), table_name='boletos')
    op.drop_index(op.f('ix_boletos_fatura_id'), table_name='boletos')
    op.drop_index(op.f('ix_boletos_cliente_id'), table_name='boletos')
    op.drop_table('boletos')
    op.drop_index(op.f('ix_parcelas_id'), table_name='parcelas')
    op.drop_index(op.f('ix_parcelas_carne_id'), table_name='parcelas')
    op.drop_table('parcelas')
    op.drop_index(op.f('ix_carnes_id'), table_name='carnes')
    op.drop_index(op.f('ix_carnes_cliente_id'), table_name='carnes')
    op.drop_table('carnes')
