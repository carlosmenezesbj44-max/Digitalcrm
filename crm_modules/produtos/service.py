from typing import Optional
from crm_modules.produtos.repository import ProdutoRepository
from crm_modules.produtos.domain import Produto
from crm_modules.produtos.schemas import ProdutoCreate, ProdutoUpdate
from crm_modules.produtos.models import ProdutoModel
from crm_core.utils.exceptions import NotFoundException, ValidationException
from crm_core.events.bus import EventBus
from crm_core.events.events import ProdutoCreatedEvent


class ProdutoService:
    def __init__(self, repository: Optional[ProdutoRepository] = None, repository_session=None, event_bus: Optional[EventBus] = None):
        if repository is not None:
            self.repository = repository
        else:
            self.repository = ProdutoRepository(session=repository_session) if repository_session is not None else ProdutoRepository()
        self.event_bus = event_bus or EventBus()

    def criar_produto(self, produto_data: ProdutoCreate) -> Produto:
        # Validate
        if not produto_data.nome.strip():
            raise ValidationException("Nome é obrigatório")
        if not produto_data.tipo.strip():
            raise ValidationException("Tipo é obrigatório")
        if produto_data.preco <= 0:
            raise ValidationException("Preço deve ser positivo")
        if not produto_data.categoria.strip():
            raise ValidationException("Categoria é obrigatória")
        if not produto_data.unidade.strip():
            raise ValidationException("Unidade é obrigatória")

        # Check unique name
        existing = self.repository.get_by_nome(produto_data.nome)
        if existing:
            raise ValidationException("Já existe um produto com este nome")

        # Create ORM model instance and persist
        model = ProdutoModel(
            nome=produto_data.nome,
            tipo=produto_data.tipo,
            preco=produto_data.preco,
            categoria=produto_data.categoria,
            unidade=produto_data.unidade,
            descricao=produto_data.descricao,
            ativo=produto_data.ativo,
            preco_custo=produto_data.preco_custo,
            sku=produto_data.sku,
            codigo_barras=produto_data.codigo_barras,
            quantidade_estoque=produto_data.quantidade_estoque,
            estoque_minimo=produto_data.estoque_minimo,
            ncm=produto_data.ncm,
            cfop=produto_data.cfop,
            icms=produto_data.icms,
            fornecedor=produto_data.fornecedor,
            imagem_url=produto_data.imagem_url,
        )

        model = self.repository.create(model)

        # Create domain object to return
        produto = Produto(
            id=model.id,
            nome=model.nome,
            tipo=model.tipo,
            preco=model.preco,
            categoria=model.categoria,
            unidade=model.unidade,
            descricao=model.descricao,
            ativo=model.ativo,
            preco_custo=model.preco_custo,
            sku=model.sku,
            codigo_barras=model.codigo_barras,
            quantidade_estoque=model.quantidade_estoque,
            estoque_minimo=model.estoque_minimo,
            ncm=model.ncm,
            cfop=model.cfop,
            icms=model.icms,
            fornecedor=model.fornecedor,
            imagem_url=model.imagem_url,
            created_at=model.created_at,
            updated_at=model.updated_at,
            created_by=model.created_by,
        )

        # Publish event
        self.event_bus.publish(ProdutoCreatedEvent(produto.id, produto.nome))
        return produto

    def obter_produto(self, produto_id: int) -> Produto:
        model = self.repository.get_by_id(produto_id)
        if not model:
            raise NotFoundException("Produto não encontrado")
        return Produto(
            id=model.id,
            nome=model.nome,
            tipo=model.tipo,
            preco=model.preco,
            categoria=model.categoria,
            unidade=model.unidade,
            descricao=model.descricao,
            ativo=model.ativo,
            preco_custo=model.preco_custo,
            sku=model.sku,
            codigo_barras=model.codigo_barras,
            quantidade_estoque=model.quantidade_estoque,
            estoque_minimo=model.estoque_minimo,
            ncm=model.ncm,
            cfop=model.cfop,
            icms=model.icms,
            fornecedor=model.fornecedor,
            imagem_url=model.imagem_url,
            created_at=model.created_at,
            updated_at=model.updated_at,
            created_by=model.created_by,
        )

    def atualizar_produto(self, produto_id: int, update_data: ProdutoUpdate) -> Produto:
        model = self.repository.get_by_id(produto_id)
        if not model:
            raise NotFoundException("Produto não encontrado")

        # Update fields
        if update_data.nome:
            # Check unique name if changing
            if update_data.nome != model.nome:
                existing = self.repository.get_by_nome(update_data.nome)
                if existing:
                    raise ValidationException("Já existe um produto com este nome")
            model.nome = update_data.nome
        if update_data.tipo:
            model.tipo = update_data.tipo
        if update_data.preco is not None:
            if update_data.preco <= 0:
                raise ValidationException("Preço deve ser positivo")
            model.preco = update_data.preco
        if update_data.categoria:
            if not update_data.categoria.strip():
                raise ValidationException("Categoria não pode ser vazia")
            model.categoria = update_data.categoria
        if update_data.unidade:
            if not update_data.unidade.strip():
                raise ValidationException("Unidade não pode ser vazia")
            model.unidade = update_data.unidade
        if update_data.descricao is not None:
            model.descricao = update_data.descricao
        if update_data.ativo is not None:
            model.ativo = update_data.ativo
        if update_data.preco_custo is not None:
            model.preco_custo = update_data.preco_custo
        if update_data.sku is not None:
            model.sku = update_data.sku
        if update_data.ncm is not None:
            model.ncm = update_data.ncm
        if update_data.cfop is not None:
            model.cfop = update_data.cfop
        if update_data.codigo_barras is not None:
            model.codigo_barras = update_data.codigo_barras
        if update_data.quantidade_estoque is not None:
            model.quantidade_estoque = update_data.quantidade_estoque
        if update_data.estoque_minimo is not None:
            model.estoque_minimo = update_data.estoque_minimo
        if update_data.icms is not None:
            model.icms = update_data.icms
        if update_data.fornecedor is not None:
            model.fornecedor = update_data.fornecedor
        if update_data.imagem_url is not None:
            model.imagem_url = update_data.imagem_url

        self.repository.update(model)

        return self.obter_produto(produto_id)

    def desativar_produto(self, produto_id: int) -> Produto:
        model = self.repository.get_by_id(produto_id)
        if not model:
            raise NotFoundException("Produto não encontrado")
        model.ativo = False
        self.repository.update(model)
        return self.obter_produto(produto_id)

    def excluir_produto(self, produto_id: int) -> bool:
        model = self.repository.get_by_id(produto_id)
        if not model:
            raise NotFoundException("Produto não encontrado")
        
        # Verificar se o produto está vinculado a algum cliente
        # (Isso é uma simplificação, idealmente teríamos uma verificação de integridade referencial)
        try:
            self.repository.delete(model)
            return True
        except Exception as e:
            # Se falhar a exclusão física (ex: restrição de chave estrangeira), inativa o produto
            model.ativo = False
            self.repository.update(model)
            raise ValidationException(f"Não foi possível excluir fisicamente o produto (pode estar vinculado a outros registros). O produto foi inativado. Detalhe: {str(e)}")

    def listar_produtos_ativos(self):
        models = self.repository.get_active_produtos()
        return [self.obter_produto(model.id) for model in models]

    def listar_produtos_com_filtros(
        self,
        tipo: Optional[str] = None,
        categoria: Optional[str] = None,
        ativo: Optional[bool] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = "nome",
        sort_order: Optional[str] = "asc",
        page: int = 1,
        per_page: int = 10
    ):
        models, total = self.repository.get_produtos_com_filtros(
            tipo=tipo,
            categoria=categoria,
            ativo=ativo,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            per_page=per_page
        )
        produtos = [self.obter_produto(model.id) for model in models]

        # Adicionar informações de paginação
        result = {
            "produtos": produtos,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page
        }
        return result