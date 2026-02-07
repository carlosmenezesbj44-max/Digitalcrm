"""Repositório para Contratos"""

from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
from crm_modules.contratos.models import ContratoModel, ContratoHistoricoModel, StatusAssinatura
from crm_core.db.repositories import BaseRepository
from crm_core.db.base import get_db_session


class ContratoRepository(BaseRepository):
    def __init__(self, session: Optional[Session] = None):
        if session is not None:
            super().__init__(session, ContratoModel)
        else:
            super().__init__(get_db_session(), ContratoModel)

    def get_contratos_by_cliente(self, cliente_id: int) -> List[ContratoModel]:
        """Busca todos os contratos de um cliente"""
        return self.session.query(ContratoModel).filter(
            ContratoModel.cliente_id == cliente_id,
            ContratoModel.deletado_em == None
        ).order_by(ContratoModel.data_criacao.desc()).all()

    def get_contrato_pendente_by_cliente(self, cliente_id: int) -> Optional[ContratoModel]:
        """Busca contrato aguardando assinatura de um cliente"""
        return self.session.query(ContratoModel).filter(
            ContratoModel.cliente_id == cliente_id,
            ContratoModel.status_assinatura == StatusAssinatura.AGUARDANDO,
            ContratoModel.deletado_em == None
        ).first()

    def get_contratos_vencendo(self, dias: int = 30) -> List[ContratoModel]:
        """Busca contratos que vencerão nos próximos N dias"""
        from sqlalchemy import and_
        data_limite = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        from datetime import timedelta
        data_limite = data_limite + timedelta(days=dias)
        
        return self.session.query(ContratoModel).filter(
            and_(
                ContratoModel.data_vigencia_fim <= data_limite,
                ContratoModel.status_assinatura == StatusAssinatura.LIBERADO,
                ContratoModel.deletado_em == None
            )
        ).order_by(ContratoModel.data_vigencia_fim.asc()).all()

    def list(self, limit: int = 100, offset: int = 0) -> List[ContratoModel]:
        """Lista contratos com paginação"""
        return self.session.query(ContratoModel).filter(
            ContratoModel.deletado_em == None
        ).order_by(ContratoModel.data_criacao.desc()).limit(limit).offset(offset).all()

    def listar_contratos_filtrados(self, 
                                  data_inicio: Optional[datetime] = None,
                                  data_fim: Optional[datetime] = None,
                                  nome: Optional[str] = None,
                                  cpf: Optional[str] = None,
                                  status_assinatura: Optional[str] = None,
                                  status_cliente: Optional[str] = None) -> List[ContratoModel]:
        """Lista contratos com diversos filtros"""
        from crm_modules.clientes.models import ClienteModel
        from sqlalchemy import and_, or_
        
        query = self.session.query(ContratoModel).join(ClienteModel, ContratoModel.cliente_id == ClienteModel.id)
        
        query = query.filter(ContratoModel.deletado_em == None)
        
        if data_inicio:
            query = query.filter(ContratoModel.data_criacao >= data_inicio)
        if data_fim:
            # Garantir que pegue até o final do dia
            if data_fim.hour == 0 and data_fim.minute == 0:
                from datetime import timedelta
                data_fim = data_fim + timedelta(days=1)
            query = query.filter(ContratoModel.data_criacao < data_fim)
            
        if nome:
            query = query.filter(ClienteModel.nome.ilike(f"%{nome}%"))
        if cpf:
            query = query.filter(ClienteModel.cpf.ilike(f"%{cpf}%"))
            
        if status_assinatura:
            query = query.filter(ContratoModel.status_assinatura == status_assinatura)
            
        if status_cliente:
            query = query.filter(ClienteModel.status_cliente == status_cliente)
            
        return query.order_by(ContratoModel.data_criacao.desc()).all()

    def get_contratos_vencidos(self) -> List[ContratoModel]:
        """Busca contratos que já venceram"""
        from sqlalchemy import and_
        data_atual = datetime.utcnow()
        
        return self.session.query(ContratoModel).filter(
            and_(
                ContratoModel.data_vigencia_fim < data_atual,
                ContratoModel.status_assinatura == StatusAssinatura.LIBERADO,
                ContratoModel.deletado_em == None
            )
        ).order_by(ContratoModel.data_vigencia_fim.desc()).all()

    def update_status_assinatura(self, contrato_id: int, status: StatusAssinatura,
                                hash_assinatura: Optional[str] = None,
                                assinatura_digital: Optional[str] = None):
        """Atualiza status de assinatura do contrato"""
        contrato = self.get_by_id(contrato_id)
        if contrato:
            contrato.status_assinatura = status
            if status == StatusAssinatura.ASSINADO:
                contrato.data_assinatura = datetime.utcnow()
                contrato.hash_assinatura = hash_assinatura
                if assinatura_digital:
                    contrato.assinatura_digital = assinatura_digital
            self.update(contrato)
            return contrato
        return None

    def soft_delete(self, contrato_id: int):
        """Soft delete (marca como deletado sem remover do BD)"""
        contrato = self.get_by_id(contrato_id)
        if contrato:
            contrato.deletado_em = datetime.utcnow()
            return self.update(contrato)
        return None


class ContratoHistoricoRepository(BaseRepository):
    """Repositório para histórico de alterações de contratos"""
    
    def __init__(self, session: Optional[Session] = None):
        if session is not None:
            super().__init__(session, ContratoHistoricoModel)
        else:
            super().__init__(get_db_session(), ContratoHistoricoModel)

    def get_historico_contrato(self, contrato_id: int) -> List[ContratoHistoricoModel]:
        """Busca histórico completo de um contrato"""
        return self.session.query(ContratoHistoricoModel).filter(
            ContratoHistoricoModel.contrato_id == contrato_id
        ).order_by(ContratoHistoricoModel.alterado_em.desc()).all()

    def registrar_alteracao(self, contrato_id: int, campo: str, valor_anterior: str,
                           valor_novo: str, usuario_id: str, motivo: str = None,
                           ip_address: str = None, user_agent: str = None) -> ContratoHistoricoModel:
        """Registra uma alteração no contrato"""
        historico = ContratoHistoricoModel(
            contrato_id=contrato_id,
            campo_alterado=campo,
            valor_anterior=valor_anterior,
            valor_novo=valor_novo,
            alterado_por=usuario_id,
            motivo=motivo,
            ip_address=ip_address,
            user_agent=user_agent,
            alterado_em=datetime.utcnow()
        )
        return self.create(historico)