"""add cliente address fields and cliente_arquivos table

Revision ID: 0001_add_cliente_address_and_files
Revises: 
Create Date: 2026-01-15 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_add_cliente_address_and_files'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add address and coordinate columns to clientes
    op.add_column('clientes', sa.Column('cidade', sa.String(), nullable=True))
    op.add_column('clientes', sa.Column('rua', sa.String(), nullable=True))
    op.add_column('clientes', sa.Column('bairro', sa.String(), nullable=True))
    op.add_column('clientes', sa.Column('cep', sa.String(), nullable=True))
    op.add_column('clientes', sa.Column('condominio', sa.String(), nullable=True))
    op.add_column('clientes', sa.Column('bloco', sa.String(), nullable=True))
    op.add_column('clientes', sa.Column('estado', sa.String(), nullable=True))
    op.add_column('clientes', sa.Column('tipo_localidade', sa.String(), nullable=True))
    op.add_column('clientes', sa.Column('numero', sa.String(), nullable=True))
    op.add_column('clientes', sa.Column('apartamento', sa.String(), nullable=True))
    op.add_column('clientes', sa.Column('complemento', sa.String(), nullable=True))
    op.add_column('clientes', sa.Column('moradia', sa.String(), nullable=True))
    op.add_column('clientes', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('clientes', sa.Column('longitude', sa.Float(), nullable=True))
    # Add username/observacoes if not present
    op.add_column('clientes', sa.Column('username', sa.String(), nullable=True))
    op.add_column('clientes', sa.Column('observacoes', sa.String(), nullable=True))
    # Contact fields
    op.add_column('clientes', sa.Column('whatsapp', sa.String(), nullable=True))
    op.add_column('clientes', sa.Column('telefone_residencial', sa.String(), nullable=True))
    op.add_column('clientes', sa.Column('telefone_comercial', sa.String(), nullable=True))
    op.add_column('clientes', sa.Column('telefone_celular', sa.String(), nullable=True))
    op.add_column('clientes', sa.Column('instagram', sa.String(), nullable=True))

    # Create cliente_arquivos table
    op.create_table(
        'cliente_arquivos',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('cliente_id', sa.Integer(), sa.ForeignKey('clientes.id'), nullable=False, index=True),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('filepath', sa.String(), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    # Drop cliente_arquivos table
    op.drop_table('cliente_arquivos')

    # Drop added columns from clientes
    op.drop_column('clientes', 'observacoes')
    op.drop_column('clientes', 'username')
    op.drop_column('clientes', 'longitude')
    op.drop_column('clientes', 'latitude')
    op.drop_column('clientes', 'instagram')
    op.drop_column('clientes', 'telefone_celular')
    op.drop_column('clientes', 'telefone_comercial')
    op.drop_column('clientes', 'telefone_residencial')
    op.drop_column('clientes', 'whatsapp')
    op.drop_column('clientes', 'moradia')
    op.drop_column('clientes', 'complemento')
    op.drop_column('clientes', 'apartamento')
    op.drop_column('clientes', 'numero')
    op.drop_column('clientes', 'tipo_localidade')
    op.drop_column('clientes', 'estado')
    op.drop_column('clientes', 'bloco')
    op.drop_column('clientes', 'condominio')
    op.drop_column('clientes', 'cep')
    op.drop_column('clientes', 'bairro')
    op.drop_column('clientes', 'rua')
    op.drop_column('clientes', 'cidade')
