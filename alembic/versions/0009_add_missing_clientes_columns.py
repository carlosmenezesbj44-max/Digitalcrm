"""Add missing columns to clientes table

Revision ID: 0009_add_missing_clientes_columns
Revises: 0008_add_payment_fields_to_contratos
Create Date: 2026-02-03 21:52:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0009_add_missing_clientes_columns'
down_revision = '0008_add_payment_fields_to_contratos'
branch_labels = None
depends_on = None


def upgrade():
    # Add missing columns to clientes table
    with op.batch_alter_table('clientes', schema=None) as batch_op:
        # Address and contact fields
        batch_op.add_column(
            sa.Column('cidade', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('rua', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('bairro', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('cep', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('condominio', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('bloco', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('estado', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('tipo_localidade', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('tipo_cliente', sa.String, nullable=False, server_default='fisico')
        )
        batch_op.add_column(
            sa.Column('nacionalidade', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('rg', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('orgao_emissor', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('naturalidade', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('data_nascimento', sa.Date, nullable=True)
        )
        batch_op.add_column(
            sa.Column('username', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('observacoes', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('instagram', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('numero', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('apartamento', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('complemento', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('moradia', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('latitude', sa.Float, nullable=True)
        )
        batch_op.add_column(
            sa.Column('longitude', sa.Float, nullable=True)
        )
        batch_op.add_column(
            sa.Column('plano_id', sa.Integer, nullable=True)
        )
        batch_op.add_column(
            sa.Column('velocidade', sa.Integer, nullable=True)
        )
        batch_op.add_column(
            sa.Column('data_instalacao', sa.Date, nullable=True)
        )
        batch_op.add_column(
            sa.Column('status_servico', sa.String, nullable=True, server_default='ativo')
        )
        batch_op.add_column(
            sa.Column('valor_mensal', sa.Float, nullable=True)
        )
        batch_op.add_column(
            sa.Column('valor_total', sa.Float, nullable=True)
        )
        batch_op.add_column(
            sa.Column('dia_vencimento', sa.Integer, nullable=True)
        )
        batch_op.add_column(
            sa.Column('servidor_id', sa.Integer, nullable=True)
        )
        batch_op.add_column(
            sa.Column('profile', sa.String, nullable=True)
        )
        batch_op.add_column(
            sa.Column('tipo_servico', sa.String, nullable=True, server_default='pppoe')
        )
        batch_op.add_column(
            sa.Column('comentario_login', sa.String, nullable=True)
        )
        
        # Serviços adicionais
        batch_op.add_column(
            sa.Column('servico_instalacao_equipamentos', sa.Boolean, nullable=False, server_default='0')
        )
        batch_op.add_column(
            sa.Column('servico_suporte_premium', sa.Boolean, nullable=False, server_default='0')
        )
        batch_op.add_column(
            sa.Column('servico_treinamentos', sa.Boolean, nullable=False, server_default='0')
        )
        batch_op.add_column(
            sa.Column('servico_cortesia', sa.Boolean, nullable=False, server_default='0')
        )
        batch_op.add_column(
            sa.Column('servico_wifi_publico', sa.Boolean, nullable=False, server_default='0')
        )
        batch_op.add_column(
            sa.Column('servico_apps_parceiros', sa.Boolean, nullable=False, server_default='0')
        )
        batch_op.add_column(
            sa.Column('servico_campanhas', sa.Boolean, nullable=False, server_default='0')
        )
        batch_op.add_column(
            sa.Column('servico_personalizados', sa.Boolean, nullable=False, server_default='0')
        )
        batch_op.add_column(
            sa.Column('servico_monitoramento', sa.Boolean, nullable=False, server_default='0')
        )
        batch_op.add_column(
            sa.Column('servico_hospedagem', sa.Boolean, nullable=False, server_default='0')
        )
        batch_op.add_column(
            sa.Column('servico_integracao', sa.Boolean, nullable=False, server_default='0')
        )
        batch_op.add_column(
            sa.Column('servico_vas', sa.Boolean, nullable=False, server_default='0')
        )
        batch_op.add_column(
            sa.Column('servico_streaming', sa.Boolean, nullable=False, server_default='0')
        )
        batch_op.add_column(
            sa.Column('servico_backup', sa.Boolean, nullable=False, server_default='0')
        )
        batch_op.add_column(
            sa.Column('servico_colaboracao', sa.Boolean, nullable=False, server_default='0')
        )
        
        # Histórico de serviços
        batch_op.add_column(
            sa.Column('historico_chamados', sa.Boolean, nullable=False, server_default='0')
        )
        batch_op.add_column(
            sa.Column('historico_instalacoes', sa.Boolean, nullable=False, server_default='0')
        )
        batch_op.add_column(
            sa.Column('historico_upgrades', sa.Boolean, nullable=False, server_default='0')
        )
        
        # Status do cliente
        batch_op.add_column(
            sa.Column('status_cliente', sa.String, nullable=False, server_default='conectado')
        )
        
        # Plano de bloqueio aplicado (opcional)
        batch_op.add_column(
            sa.Column('plano_bloqueio_id', sa.Integer, nullable=True)
        )
        
        # Foto da casa
        batch_op.add_column(
            sa.Column('foto_casa', sa.String, nullable=True)
        )


def downgrade():
    with op.batch_alter_table('clientes', schema=None) as batch_op:
        # Remove all the columns we added
        batch_op.drop_column('foto_casa')
        batch_op.drop_column('plano_bloqueio_id')
        batch_op.drop_column('status_cliente')
        batch_op.drop_column('historico_upgrades')
        batch_op.drop_column('historico_instalacoes')
        batch_op.drop_column('historico_chamados')
        batch_op.drop_column('servico_colaboracao')
        batch_op.drop_column('servico_backup')
        batch_op.drop_column('servico_streaming')
        batch_op.drop_column('servico_vas')
        batch_op.drop_column('servico_integracao')
        batch_op.drop_column('servico_hospedagem')
        batch_op.drop_column('servico_monitoramento')
        batch_op.drop_column('servico_personalizados')
        batch_op.drop_column('servico_campanhas')
        batch_op.drop_column('servico_apps_parceiros')
        batch_op.drop_column('servico_wifi_publico')
        batch_op.drop_column('servico_cortesia')
        batch_op.drop_column('servico_treinamentos')
        batch_op.drop_column('servico_suporte_premium')
        batch_op.drop_column('servico_instalacao_equipamentos')
        batch_op.drop_column('comentario_login')
        batch_op.drop_column('tipo_servico')
        batch_op.drop_column('profile')
        batch_op.drop_column('servidor_id')
        batch_op.drop_column('dia_vencimento')
        batch_op.drop_column('valor_total')
        batch_op.drop_column('valor_mensal')
        batch_op.drop_column('status_servico')
        batch_op.drop_column('data_instalacao')
        batch_op.drop_column('velocidade')
        batch_op.drop_column('plano_id')
        batch_op.drop_column('longitude')
        batch_op.drop_column('latitude')
        batch_op.drop_column('moradia')
        batch_op.drop_column('complemento')
        batch_op.drop_column('apartamento')
        batch_op.drop_column('numero')
        batch_op.drop_column('instagram')
        batch_op.drop_column('observacoes')
        batch_op.drop_column('username')
        batch_op.drop_column('data_nascimento')
        batch_op.drop_column('naturalidade')
        batch_op.drop_column('orgao_emissor')
        batch_op.drop_column('rg')
        batch_op.drop_column('nacionalidade')
        batch_op.drop_column('tipo_cliente')
        batch_op.drop_column('tipo_localidade')
        batch_op.drop_column('estado')
        batch_op.drop_column('bloco')
        batch_op.drop_column('condominio')
        batch_op.drop_column('cep')
        batch_op.drop_column('bairro')
        batch_op.drop_column('rua')
        batch_op.drop_column('cidade')