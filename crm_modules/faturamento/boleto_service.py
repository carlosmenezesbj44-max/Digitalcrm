from typing import Optional, List
from datetime import datetime, date
from sqlalchemy.orm import Session

from crm_modules.faturamento.carne_models import BoletoModel
from crm_modules.faturamento.models import FaturaModel
from crm_modules.faturamento.carne_schemas import BoletoCreate, BoletoResponse
from crm_modules.faturamento.gerencianet_client import GerencianetClient
from crm_modules.clientes.models import ClienteModel
from crm_core.utils.exceptions import NotFoundException, ValidationException


class BoletoService:
    """Service para gerenciar boletos"""
    
    def __init__(self, session: Session, gerencianet_client: Optional[GerencianetClient] = None):
        self.session = session
        self.gerencianet_client = gerencianet_client or GerencianetClient()
    
    def gerar_boleto_fatura(
        self,
        fatura_id: int,
        juros_dia: float = 0.0,
        multa_atraso: float = 0.0
    ) -> BoletoResponse:
        """
        Gera boleto para uma fatura existente
        
        Args:
            fatura_id: ID da fatura
            juros_dia: Juros de mora por dia (%)
            multa_atraso: Multa por atraso (%)
            
        Returns:
            BoletoResponse com dados do boleto gerado
        """
        
        # Buscar fatura
        fatura = self.session.query(FaturaModel).filter(
            FaturaModel.id == fatura_id
        ).first()
        
        if not fatura:
            raise NotFoundException("Fatura não encontrada")
        
        # Buscar cliente
        cliente = self.session.query(ClienteModel).filter(
            ClienteModel.id == fatura.cliente_id
        ).first()
        
        if not cliente:
            raise NotFoundException("Cliente não encontrado")
        
        # Validar dados necessários
        if not cliente.email:
            raise ValidationException("Cliente não possui email cadastrado")
        
        # Gerar número único para o boleto
        numero_boleto = self._gerar_numero_boleto(fatura.cliente_id)
        
        # Gerar boleto - se não estiver conectado ao Gerencianet, gera localmente
        if self.gerencianet_client.connected:
            try:
                resultado = self.gerencianet_client.gerar_boleto(
                    cliente_nome=cliente.nome,
                    cliente_cpf=cliente.cpf or "00000000000",
                    cliente_email=cliente.email,
                    valor=fatura.valor_total,
                    data_vencimento=fatura.data_vencimento,
                    numero_referencia=fatura.numero_fatura,
                    descricao=fatura.descricao or f"Fatura {fatura.numero_fatura}",
                    juros_dia=juros_dia,
                    multa_atraso=multa_atraso
                )
            except Exception as e:
                print(f"Aviso: Erro ao gerar boleto no Gerencianet - {e}")
                resultado = {}
        else:
            resultado = {}
        
        # Criar registro de boleto
        boleto = BoletoModel(
            cliente_id=fatura.cliente_id,
            fatura_id=fatura_id,
            numero_boleto=numero_boleto,
            valor=fatura.valor_total,
            data_vencimento=fatura.data_vencimento,
            codigo_barras=resultado.get("codigo_barras"),
            linha_digitavel=resultado.get("linha_digitavel"),
            url_boleto=resultado.get("url_boleto"),
            gerencianet_charge_id=str(resultado.get("charge_id")) if resultado.get("charge_id") else None,
            gerencianet_status="aberto" if resultado else None,
            status="pendente"
        )
        
        self.session.add(boleto)
        self.session.commit()
        self.session.refresh(boleto)
        
        return self._model_to_response(boleto)
    
    def gerar_boleto_direto(
        self,
        cliente_id: int,
        valor: float,
        data_vencimento: date,
        descricao: Optional[str] = None,
        juros_dia: float = 0.0,
        multa_atraso: float = 0.0
    ) -> BoletoResponse:
        """
        Gera um boleto diretamente sem estar vinculado a uma fatura
        
        Args:
            cliente_id: ID do cliente
            valor: Valor do boleto
            data_vencimento: Data de vencimento
            descricao: Descrição do boleto
            juros_dia: Juros de mora por dia (%)
            multa_atraso: Multa por atraso (%)
            
        Returns:
            BoletoResponse com dados do boleto gerado
        """
        
        # Buscar cliente
        cliente = self.session.query(ClienteModel).filter(
            ClienteModel.id == cliente_id
        ).first()
        
        if not cliente:
            raise NotFoundException("Cliente não encontrado")
        
        if not cliente.email:
            raise ValidationException("Cliente não possui email cadastrado")
        
        if valor <= 0:
            raise ValidationException("Valor deve ser maior que zero")
        
        # Gerar número único para o boleto
        numero_boleto = self._gerar_numero_boleto(cliente_id)
        
        # Gerar boleto - se não estiver conectado ao Gerencianet, gera localmente
        if self.gerencianet_client.connected:
            try:
                resultado = self.gerencianet_client.gerar_boleto(
                    cliente_nome=cliente.nome,
                    cliente_cpf=cliente.cpf or "00000000000",
                    cliente_email=cliente.email,
                    valor=valor,
                    data_vencimento=data_vencimento,
                    numero_referencia=numero_boleto,
                    descricao=descricao or f"Boleto {numero_boleto}",
                    juros_dia=juros_dia,
                    multa_atraso=multa_atraso
                )
            except Exception as e:
                print(f"Aviso: Erro ao gerar boleto no Gerencianet - {e}")
                resultado = {}
        else:
            resultado = {}
        
        # Criar registro de boleto
        boleto = BoletoModel(
            cliente_id=cliente_id,
            numero_boleto=numero_boleto,
            valor=valor,
            data_vencimento=data_vencimento,
            codigo_barras=resultado.get("codigo_barras"),
            linha_digitavel=resultado.get("linha_digitavel"),
            url_boleto=resultado.get("url_boleto"),
            gerencianet_charge_id=str(resultado.get("charge_id")) if resultado.get("charge_id") else None,
            gerencianet_status="aberto" if resultado else None,
            status="pendente"
        )
        
        self.session.add(boleto)
        self.session.commit()
        self.session.refresh(boleto)
        
        return self._model_to_response(boleto)
    
    def obter_boleto(self, boleto_id: int) -> BoletoResponse:
        """Obtém um boleto pelo ID"""
        
        boleto = self.session.query(BoletoModel).filter(
            BoletoModel.id == boleto_id
        ).first()
        
        if not boleto:
            raise NotFoundException("Boleto não encontrado")
        
        return self._model_to_response(boleto)
    
    def listar_boletos_cliente(self, cliente_id: int, status: Optional[str] = None) -> List[BoletoResponse]:
        """Lista boletos de um cliente"""
        
        query = self.session.query(BoletoModel).filter(
            BoletoModel.cliente_id == cliente_id,
            BoletoModel.ativo == True
        )
        
        if status:
            query = query.filter(BoletoModel.status == status)
        
        boletos = query.order_by(BoletoModel.data_vencimento).all()
        
        return [self._model_to_response(b) for b in boletos]
    
    def listar_todos_boletos(self, cliente_id: Optional[int] = None, status: Optional[str] = None) -> List[BoletoResponse]:
        """Lista todos os boletos ativos com filtros opcionais"""
        
        from sqlalchemy.orm import joinedload
        
        query = self.session.query(BoletoModel).options(
            joinedload(BoletoModel.cliente)
        ).filter(
            BoletoModel.ativo == True
        )
        
        if cliente_id:
            query = query.filter(BoletoModel.cliente_id == cliente_id)
        
        if status:
            query = query.filter(BoletoModel.status == status)
        
        boletos = query.order_by(BoletoModel.data_vencimento.desc()).all()
        
        return [self._model_to_response(b) for b in boletos]
    
    def listar_boletos_vencidos(self) -> List[BoletoResponse]:
        """Lista todos os boletos vencidos não pagos"""
        
        hoje = date.today()
        
        boletos = self.session.query(BoletoModel).filter(
            BoletoModel.data_vencimento < hoje,
            BoletoModel.status == "pendente",
            BoletoModel.ativo == True
        ).order_by(BoletoModel.data_vencimento).all()
        
        return [self._model_to_response(b) for b in boletos]
    
    def atualizar_status_boleto(self, boleto_id: int, novo_status: str) -> BoletoResponse:
        """Atualiza o status de um boleto"""
        
        boleto = self.session.query(BoletoModel).filter(
            BoletoModel.id == boleto_id
        ).first()
        
        if not boleto:
            raise NotFoundException("Boleto não encontrado")
        
        status_validos = ["pendente", "pago", "cancelado"]
        if novo_status not in status_validos:
            raise ValidationException(f"Status inválido. Deve ser um de: {status_validos}")
        
        boleto.status = novo_status
        boleto.data_atualizacao = datetime.utcnow()
        
        self.session.commit()
        self.session.refresh(boleto)
        
        return self._model_to_response(boleto)
    
    def cancelar_boleto(self, boleto_id: int) -> BoletoResponse:
        """Cancela um boleto"""
        
        boleto = self.session.query(BoletoModel).filter(
            BoletoModel.id == boleto_id
        ).first()
        
        if not boleto:
            raise NotFoundException("Boleto não encontrado")
        
        if boleto.status == "pago":
            raise ValidationException("Não é possível cancelar um boleto já pago")
        
        # Cancelar no Gerencianet
        if boleto.gerencianet_charge_id:
            try:
                self.gerencianet_client.cancelar_boleto(int(boleto.gerencianet_charge_id))
            except Exception as e:
                print(f"Aviso: Erro ao cancelar boleto no Gerencianet: {e}")
        
        boleto.status = "cancelado"
        boleto.gerencianet_status = "cancelado"
        boleto.ativo = False
        boleto.data_atualizacao = datetime.utcnow()
        
        self.session.commit()
        self.session.refresh(boleto)
        
        return self._model_to_response(boleto)
    
    def atualizar_status_gerencianet(self, boleto_id: int) -> BoletoResponse:
        """Atualiza o status do boleto consultando o Gerencianet"""
        
        boleto = self.session.query(BoletoModel).filter(
            BoletoModel.id == boleto_id
        ).first()
        
        if not boleto or not boleto.gerencianet_charge_id:
            raise NotFoundException("Boleto não encontrado ou sem ID do Gerencianet")
        
        try:
            # Consultar no Gerencianet
            resultado = self.gerencianet_client.consultar_boleto(
                int(boleto.gerencianet_charge_id)
            )
            
            # Mapear status do Gerencianet para nosso status
            gerencianet_status = resultado.get("status")
            
            if gerencianet_status == "paid":
                boleto.status = "pago"
                boleto.gerencianet_status = "pago"
            elif gerencianet_status == "canceled":
                boleto.status = "cancelado"
                boleto.gerencianet_status = "cancelado"
            else:
                boleto.gerencianet_status = gerencianet_status
            
            boleto.data_atualizacao = datetime.utcnow()
            self.session.commit()
            self.session.refresh(boleto)
            
        except Exception as e:
            print(f"Erro ao atualizar status do boleto: {e}")
        
        return self._model_to_response(boleto)
    
    def sincronizar_pagamentos_gerencianet(self) -> List[BoletoResponse]:
        """Sincroniza status de todos os boletos abertos com Gerencianet"""
        
        boletos_abertos = self.session.query(BoletoModel).filter(
            BoletoModel.status == "pendente",
            BoletoModel.gerencianet_charge_id.isnot(None),
            BoletoModel.ativo == True
        ).all()
        
        boletos_atualizados = []
        
        for boleto in boletos_abertos:
            try:
                resposta = self.atualizar_status_gerencianet(boleto.id)
                boletos_atualizados.append(resposta)
            except Exception as e:
                print(f"Erro ao sincronizar boleto {boleto.id}: {e}")
        
        return boletos_atualizados
    
    def _gerar_numero_boleto(self, cliente_id: int) -> str:
        """Gera número único para o boleto"""
        
        count = self.session.query(BoletoModel).filter(
            BoletoModel.cliente_id == cliente_id
        ).count()
        
        agora = datetime.utcnow()
        return f"BOL-{agora.year}{agora.month:02d}{agora.day:02d}-{cliente_id:04d}-{count + 1:04d}"
    
    def _model_to_response(self, boleto: BoletoModel) -> BoletoResponse:
        """Converte model para response schema"""
        
        cliente_nome = None
        if hasattr(boleto, 'cliente') and boleto.cliente:
            cliente_nome = boleto.cliente.nome
        
        return BoletoResponse(
            id=boleto.id,
            cliente_id=boleto.cliente_id,
            cliente_nome=cliente_nome,
            numero_boleto=boleto.numero_boleto,
            valor=boleto.valor,
            data_vencimento=boleto.data_vencimento,
            codigo_barras=boleto.codigo_barras,
            linha_digitavel=boleto.linha_digitavel,
            url_boleto=boleto.url_boleto,
            gerencianet_charge_id=boleto.gerencianet_charge_id,
            gerencianet_status=boleto.gerencianet_status,
            status=boleto.status,
            data_emissao=boleto.data_emissao,
            data_criacao=boleto.data_criacao
        )
