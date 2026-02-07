"""add checklist tables

Revision ID: 0016
Revises: 0015
Create Date: 2024-XX-XX

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0016'
down_revision = '0015'
branch_labels = None
depends_on = None


def upgrade():
    # Criar tabela checklist_items
    op.create_table(
        'checklist_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tipo_servico', sa.String(), nullable=False),
        sa.Column('nome_tarefa', sa.String(), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('ordem', sa.Integer(), default=0),
        sa.Column('ativo', sa.Boolean(), default=True),
        sa.Column('data_criacao', sa.DateTime(), default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_checklist_items_id', 'checklist_items', ['id'])

    # Criar tabela checklist_progress
    op.create_table(
        'checklist_progress',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ordem_servico_id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('completado', sa.Boolean(), default=False),
        sa.Column('data_completado', sa.DateTime(), nullable=True),
        sa.Column('completado_por', sa.String(), nullable=True),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.Column('criado_automaticamente', sa.Boolean(), default=True),
        sa.ForeignKeyConstraint(['ordem_servico_id'], ['ordens_servico.id'], ),
        sa.ForeignKeyConstraint(['item_id'], ['checklist_items.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_checklist_progress_id', 'checklist_progress', ['id'])

    # Popular checklist_items com templates padrão
    # Instalação
    op.execute("""
        INSERT INTO checklist_items (tipo_servico, nome_tarefa, descricao, ordem) VALUES
        ('instalacao', 'Verificar sinal', 'Testar nível de sinal no ponto de instalação', 1),
        ('instalacao', 'Configurar PPPoE', 'Criar e configurar conexão PPPoE no cliente', 2),
        ('instalacao', 'Testar velocidade', 'Realizar teste de velocidade e estabilidade', 3),
        ('instalacao', 'Orientar cliente', 'Explicar uso do serviço e Wi-Fi ao cliente', 4),
        ('instalacao', 'Finalizar', 'Finalizar instalação e coletar assinatura do cliente', 5)
    """)

    # Suporte
    op.execute("""
        INSERT INTO checklist_items (tipo_servico, nome_tarefa, descricao, ordem) VALUES
        ('suporte', 'Diagnosticar problema', 'Identificar causa raiz do problema reportado', 1),
        ('suporte', 'Verificar cabo', 'Inspecionar e substituir cabos danificados', 2),
        ('suporte', 'Reiniciar equipamento', 'Reiniciar roteador/ONU conforme procedimento', 3),
        ('suporte', 'Testar conectividade', 'Verificar conexão após intervenções', 4),
        ('suporte', 'Solucionar', 'Aplicar solução definitiva ou escalar', 5)
    """)

    # Manutenção
    op.execute("""
        INSERT INTO checklist_items (tipo_servico, nome_tarefa, descricao, ordem) VALUES
        ('manutencao', 'Inspecionar equipamentos', 'Verificar estado físico de equipamentos', 1),
        ('manutencao', 'Limpar conexões', 'Limpar conectores e terminais', 2),
        ('manutencao', 'Verificar redundância', 'Testar caminhos redundantes de rede', 3),
        ('manutencao', 'Documentar ações', 'Registrar todas as manutenções realizadas', 4),
        ('manutencao', 'Finalizar', 'Confirmar funcionamento e encerrar OS', 5)
    """)


def downgrade():
    op.drop_index('ix_checklist_progress_id')
    op.drop_table('checklist_progress')
    op.drop_index('ix_checklist_items_id')
    op.drop_table('checklist_items')
