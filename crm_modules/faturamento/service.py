from typing import Optional, List
from datetime import datetime, date
from crm_modules.faturamento.repository import FaturamentoRepository
from crm_modules.faturamento.domain import Fatura, Pagamento
from crm_modules.faturamento.schemas import FaturaCreate, FaturaUpdate, PagamentoCreate, PagamentoUpdate
from crm_modules.faturamento.models import FaturaModel, PagamentoModel
from crm_modules.clientes.models import ClienteModel
from crm_modules.planos.models import PlanoModel
from crm_core.utils.exceptions import NotFoundException, ValidationException
from sqlalchemy.orm import Session


class FaturamentoService:
    def __init__(self, repository: Optional[FaturamentoRepository] = None, repository_session: Optional[Session] = None):
        if repository is not None:
            self.repository = repository
        else:
            self.repository = FaturamentoRepository(session=repository_session) if repository_session is not None else FaturamentoRepository()

    def criar_fatura(self, fatura_data: FaturaCreate) -> Fatura:
        # Validate
        if not fatura_data.numero_fatura or fatura_data.valor_total < 0:
            raise ValidationException("Número da fatura e valor total são obrigatórios")

        # Check if cliente exists
        cliente = self.repository.session.query(ClienteModel).filter(ClienteModel.id == fatura_data.cliente_id).first()
        if not cliente:
            raise NotFoundException("Cliente não encontrado")

        # Create model
        model = FaturaModel(
            cliente_id=fatura_data.cliente_id,
            numero_fatura=fatura_data.numero_fatura,
            data_vencimento=fatura_data.data_vencimento,
            valor_total=fatura_data.valor_total,
            descricao=fatura_data.descricao,
        )

        model = self.repository.create(model)

        return Fatura(
            id=model.id,
            cliente_id=model.cliente_id,
            numero_fatura=model.numero_fatura,
            data_emissao=model.data_emissao,
            data_vencimento=model.data_vencimento,
            valor_total=model.valor_total,
            status=model.status,
            valor_pago=model.valor_pago,
            descricao=model.descricao,
            ativo=model.ativo,
        )

    def obter_fatura(self, fatura_id: int) -> Fatura:
        model = self.repository.get_by_id(fatura_id)
        if not model:
            raise NotFoundException("Fatura não encontrada")
        return self._model_to_domain(model)

    def atualizar_fatura(self, fatura_id: int, update_data: FaturaUpdate) -> Fatura:
        model = self.repository.get_by_id(fatura_id)
        if not model:
            raise NotFoundException("Fatura não encontrada")

        # Update fields
        if update_data.numero_fatura:
            model.numero_fatura = update_data.numero_fatura
        if update_data.data_vencimento:
            model.data_vencimento = update_data.data_vencimento
        if update_data.valor_total is not None:
            model.valor_total = update_data.valor_total
        if update_data.status:
            model.status = update_data.status
        if update_data.descricao is not None:
            model.descricao = update_data.descricao
        if update_data.ativo is not None:
            model.ativo = update_data.ativo

        self.repository.update(model)
        return self._model_to_domain(model)

    def registrar_pagamento(self, pagamento_data: PagamentoCreate) -> Pagamento:
        # Validate
        if pagamento_data.valor_pago <= 0:
            raise ValidationException("Valor pago deve ser maior que zero")

        fatura = self.repository.get_by_id(pagamento_data.fatura_id)
        if not fatura:
            raise NotFoundException("Fatura não encontrada")

        # Create payment
        model = PagamentoModel(
            fatura_id=pagamento_data.fatura_id,
            valor_pago=pagamento_data.valor_pago,
            metodo_pagamento=pagamento_data.metodo_pagamento,
            referencia=pagamento_data.referencia,
            observacoes=pagamento_data.observacoes,
        )

        self.repository.session.add(model)
        self.repository.session.commit()
        self.repository.session.refresh(model)

        # Update fatura valor_pago and status
        total_pago = self.repository.calcular_total_pago_fatura(pagamento_data.fatura_id)
        fatura.valor_pago = total_pago
        if total_pago >= fatura.valor_total:
            fatura.status = "pago"
        self.repository.update(fatura)

        return Pagamento(
            id=model.id,
            fatura_id=model.fatura_id,
            valor_pago=model.valor_pago,
            data_pagamento=model.data_pagamento,
            metodo_pagamento=model.metodo_pagamento,
            referencia=model.referencia,
            observacoes=model.observacoes,
            ativo=model.ativo,
        )

    def gerar_faturas_mensais(self, mes: int, ano: int) -> List[Fatura]:
        # Get clients with plans
        clientes = self.repository.session.query(ClienteModel).filter(
            ClienteModel.plano_id.isnot(None),
            ClienteModel.valor_mensal.isnot(None),
            ClienteModel.dia_vencimento.isnot(None),
            ClienteModel.ativo == True
        ).all()

        faturas_criadas = []

        for cliente in clientes:
            # Check if fatura already exists for this month
            vencimento = date(ano, mes, cliente.dia_vencimento)
            existing = self.repository.session.query(FaturaModel).filter(
                FaturaModel.cliente_id == cliente.id,
                FaturaModel.data_vencimento == vencimento,
                FaturaModel.ativo == True
            ).first()

            if not existing:
                numero_fatura = f"FAT-{ano}-{mes:02d}-{cliente.id}"
                fatura_data = FaturaCreate(
                    cliente_id=cliente.id,
                    numero_fatura=numero_fatura,
                    data_vencimento=vencimento,
                    valor_total=cliente.valor_mensal,
                    descricao=f"Fatura mensal - Plano {cliente.plano_id}"
                )
                fatura = self.criar_fatura(fatura_data)
                faturas_criadas.append(fatura)

        return faturas_criadas

    def gerar_fatura_cliente(self, cliente_id: int, mes: int, ano: int) -> Optional[Fatura]:
        """Gera fatura mensal para um cliente específico"""
        cliente = self.repository.session.query(ClienteModel).filter(ClienteModel.id == cliente_id).first()

        if not cliente or not cliente.ativo or not cliente.valor_mensal or not cliente.dia_vencimento:
            return None

        try:
            # Verificar se já existe fatura para este mês/ano
            vencimento = date(ano, mes, cliente.dia_vencimento)
            fatura_existente = self.repository.session.query(FaturaModel).filter(
                FaturaModel.cliente_id == cliente.id,
                FaturaModel.data_vencimento == vencimento,
                FaturaModel.ativo == True
            ).first()

            if fatura_existente:
                return None  # Já existe fatura para este período

            # Criar nova fatura
            numero_fatura = f"FAT-{ano:04d}{mes:02d}-{cliente.id:04d}"
            fatura_data = FaturaCreate(
                cliente_id=cliente.id,
                numero_fatura=numero_fatura,
                data_vencimento=vencimento,
                valor_total=cliente.valor_mensal,
                descricao=f"Fatura mensal - {mes:02d}/{ano}"
            )

            return self.criar_fatura(fatura_data)

        except Exception as e:
            print(f"Erro ao gerar fatura para cliente {cliente_id}: {e}")
            return None

    def listar_faturas_cliente(self, cliente_id: int) -> List[Fatura]:
        models = self.repository.get_faturas_by_cliente(cliente_id)
        return [self._model_to_domain(model) for model in models]

    def listar_todas_faturas(self) -> List[Fatura]:
        models = self.repository.get_all_faturas()
        return [self._model_to_domain(model) for model in models]

    def listar_todos_pagamentos(self) -> List[PagamentoResponse]:
        from sqlalchemy.orm import joinedload
        models = self.repository.session.query(PagamentoModel)\
            .options(joinedload(PagamentoModel.fatura).joinedload(FaturaModel.cliente))\
            .filter(PagamentoModel.ativo == True)\
            .order_by(PagamentoModel.data_pagamento.desc())\
            .all()
        
        return [
            PagamentoResponse(
                id=m.id,
                fatura_id=m.fatura_id,
                numero_fatura=m.fatura.numero_fatura if m.fatura else "N/A",
                cliente_nome=m.fatura.cliente.nome if m.fatura and m.fatura.cliente else "N/A",
                cliente_id=m.fatura.cliente_id if m.fatura else None,
                valor_pago=m.valor_pago,
                data_pagamento=m.data_pagamento,
                metodo_pagamento=m.metodo_pagamento,
                referencia=m.referencia,
                observacoes=m.observacoes,
                ativo=m.ativo
            ) for m in models
        ]

    def marcar_fatura_paga(self, fatura_id: int) -> Fatura:
        model = self.repository.get_by_id(fatura_id)
        if not model:
            raise NotFoundException("Fatura não encontrada")
        
        model.status = "pago"
        model.valor_pago = model.valor_total
        
        # Registrar um pagamento se não houver nenhum pagamento registrado
        total_pago = self.repository.calcular_total_pago_fatura(fatura_id)
        if total_pago < model.valor_total:
            pagamento = PagamentoModel(
                fatura_id=fatura_id,
                valor_pago=model.valor_total - total_pago,
                metodo_pagamento="ajuste_manual",
                data_pagamento=datetime.now(),
                referencia="Marcado como pago manualmente"
            )
            self.repository.session.add(pagamento)
            
        self.repository.update(model)
        return self._model_to_domain(model)

    def obter_fatura_detalhada(self, fatura_id: int) -> dict:
        model = self.repository.get_by_id(fatura_id)
        if not model:
            raise NotFoundException("Fatura não encontrada")
        
        # Buscar cliente
        cliente = self.repository.session.query(ClienteModel).filter(ClienteModel.id == model.cliente_id).first()
        
        # Buscar pagamentos
        pagamentos = self.repository.get_pagamentos_by_fatura(fatura_id)
        
        return {
            "id": model.id,
            "numero_fatura": model.numero_fatura,
            "data_emissao": model.data_emissao,
            "data_vencimento": model.data_vencimento,
            "valor_total": model.valor_total,
            "status": model.status,
            "valor_pago": model.valor_pago,
            "descricao": model.descricao,
            "cliente_nome": cliente.nome if cliente else "N/A",
            "cliente_cpf_cnpj": cliente.cpf if cliente else "N/A",
            "cliente_email": cliente.email if cliente else "N/A",
            "cliente_telefone": cliente.telefone if cliente else "N/A",
            "cliente_endereco": (f"{cliente.rua}, {cliente.numero} - {cliente.bairro}, {cliente.cidade}" if cliente and cliente.rua else cliente.endereco) if cliente else "N/A",
            "pagamentos": [
                {
                    "data": p.data_pagamento,
                    "valor": p.valor_pago,
                    "metodo": p.metodo_pagamento,
                    "referencia": p.referencia
                } for p in pagamentos
            ]
        }

    def _model_to_domain(self, model: FaturaModel) -> Fatura:
        return Fatura(
            id=model.id,
            cliente_id=model.cliente_id,
            numero_fatura=model.numero_fatura,
            data_emissao=model.data_emissao,
            data_vencimento=model.data_vencimento,
            valor_total=model.valor_total,
            status=model.status,
            valor_pago=model.valor_pago,
            descricao=model.descricao,
            ativo=model.ativo,
        )