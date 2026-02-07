"""Add tecnicos table with full info

Revision ID: 0004
Revises: d05b609a8955
Create Date: 2024-01-18 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0004'
down_revision = 'd05b609a8955'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tecnicos',
        sa.Column('id', sa.Integer(), nullable=False),
        # Básicas
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('telefone', sa.String(), nullable=False),
        sa.Column('telefone_secundario', sa.String(), nullable=True),
        sa.Column('cpf', sa.String(), nullable=True),
        sa.Column('data_nascimento', sa.DateTime(), nullable=True),
        # Foto
        sa.Column('foto_url', sa.String(), nullable=True),
        # Endereço
        sa.Column('endereco_rua', sa.String(), nullable=True),
        sa.Column('endereco_numero', sa.String(), nullable=True),
        sa.Column('endereco_complemento', sa.String(), nullable=True),
        sa.Column('endereco_bairro', sa.String(), nullable=True),
        sa.Column('endereco_cidade', sa.String(), nullable=True),
        sa.Column('endereco_estado', sa.String(), nullable=True),
        sa.Column('endereco_cep', sa.String(), nullable=True),
        # Profissional
        sa.Column('especialidades', sa.String(), nullable=True),
        sa.Column('crea', sa.String(), nullable=True),
        sa.Column('formacao', sa.String(), nullable=True),
        sa.Column('experiencia_anos', sa.Integer(), nullable=True),
        # Financeiro
        sa.Column('salario_taxa', sa.Float(), nullable=True),
        sa.Column('banco', sa.String(), nullable=True),
        sa.Column('agencia', sa.String(), nullable=True),
        sa.Column('conta', sa.String(), nullable=True),
        sa.Column('tipo_conta', sa.String(), nullable=True),
        # Emprego
        sa.Column('data_admissao', sa.DateTime(), nullable=True),
        sa.Column('data_demissao', sa.DateTime(), nullable=True),
        sa.Column('cargo', sa.String(), nullable=True),
        # Status
        sa.Column('status', sa.String(), server_default='ativo'),
        sa.Column('ativo', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('observacoes', sa.Text(), nullable=True),
        # Auditoria
        sa.Column('data_cadastro', sa.DateTime(), nullable=True),
        sa.Column('data_atualizacao', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('cpf')
    )
    op.create_index(op.f('ix_tecnicos_id'), 'tecnicos', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_tecnicos_id'), table_name='tecnicos')
    op.drop_table('tecnicos')
