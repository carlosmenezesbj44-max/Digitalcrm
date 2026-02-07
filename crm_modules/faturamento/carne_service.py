from typing import Optional, List
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session

from crm_modules.faturamento.carne_models import CarneModel, ParcelaModel, BoletoModel
from crm_modules.faturamento.carne_schemas import CarneCreate, CarneUpdate, CarneResponse, BoletoResponse
from crm_modules.faturamento.gerencianet_client import GerencianetClient
from crm_modules.clientes.models import ClienteModel
from crm_core.utils.exceptions import NotFoundException, ValidationException


class CarneService:
    """Service para gerenciar carnês (planos de pagamento parcelado)"""
    
    def __init__(self, session: Session, gerencianet_client: Optional[GerencianetClient] = None):
        self.session = session
        self.gerencianet_client = gerencianet_client

    def _get_gerencianet_client(self) -> GerencianetClient:
        if self.gerencianet_client is None:
            self.gerencianet_client = GerencianetClient()
        return self.gerencianet_client
    
    def criar_carne(self, carne_data: CarneCreate) -> CarneResponse:
        """
        Cria um novo carnê (plano de pagamento)
        
        Args:
            carne_data: Dados do carnê a criar
            
        Returns:
            CarneResponse com dados do carnê criado
        """
        
        # Validar cliente
        cliente = self.session.query(ClienteModel).filter(
            ClienteModel.id == carne_data.cliente_id
        ).first()
        
        if not cliente:
            raise NotFoundException("Cliente não encontrado")
        
        # Validações
        if carne_data.quantidade_parcelas <= 0:
            raise ValidationException("Quantidade de parcelas deve ser maior que zero")
        
        if carne_data.valor_total <= 0:
            raise ValidationException("Valor total deve ser maior que zero")
        
        if carne_data.quantidade_parcelas > 360:  # máx 30 anos
            raise ValidationException("Máximo 360 parcelas permitidas")
        
        # Calcular valor da parcela
        valor_parcela = carne_data.valor_total / carne_data.quantidade_parcelas
        
        # Gerar número único para o carnê
        numero_carne = self._gerar_numero_carne(carne_data.cliente_id)
        
        # Criar o carnê
        carne = CarneModel(
            cliente_id=carne_data.cliente_id,
            numero_carne=numero_carne,
            valor_total=carne_data.valor_total,
            quantidade_parcelas=carne_data.quantidade_parcelas,
            valor_parcela=valor_parcela,
            data_inicio=carne_data.data_inicio,
            data_primeiro_vencimento=carne_data.data_primeiro_vencimento,
            intervalo_dias=carne_data.intervalo_dias,
            descricao=carne_data.descricao,
            status="ativo"
        )
        
        self.session.add(carne)
        self.session.flush()  # Para obter o ID
        
        # Criar as parcelas
        parcelas = self._criar_parcelas(
            carne=carne,
            valor_parcela=valor_parcela,
            data_primeiro_vencimento=carne_data.data_primeiro_vencimento,
            intervalo_dias=carne_data.intervalo_dias,
            quantidade=carne_data.quantidade_parcelas
        )
        
        # Se solicitado, gerar boletos no Gerencianet
        if carne_data.gerar_boletos:
            try:
                self._gerar_boletos_gerencianet(carne, parcelas, cliente)
            except Exception as e:
                # Log do erro mas não falha a criação do carnê
                print(f"Aviso: Erro ao gerar boletos no Gerencianet: {e}")
        
        self.session.commit()
        self.session.refresh(carne)
        
        return self._model_to_response(carne)
    
    def _criar_parcelas(
        self,
        carne: CarneModel,
        valor_parcela: float,
        data_primeiro_vencimento: date,
        intervalo_dias: int,
        quantidade: int
    ) -> List[ParcelaModel]:
        """Cria todas as parcelas do carnê"""
        
        parcelas = []
        data_vencimento = data_primeiro_vencimento
        
        for numero in range(1, quantidade + 1):
            parcela = ParcelaModel(
                carne_id=carne.id,
                numero_parcela=numero,
                valor=valor_parcela,
                data_vencimento=data_vencimento,
                status="pendente"
            )
            
            self.session.add(parcela)
            parcelas.append(parcela)
            
            # Próximo vencimento
            data_vencimento = data_vencimento + timedelta(days=intervalo_dias)
        
        return parcelas
    
    def _gerar_boletos_gerencianet(
        self,
        carne: CarneModel,
        parcelas: List[ParcelaModel],
        cliente: ClienteModel
    ) -> None:
        """Gera boletos no Gerencianet para cada parcela"""
        
        # Validar dados necessários do cliente
        if not cliente.email:
            raise ValidationException("Cliente não possui email cadastrado")
        
        cpf = cliente.cpf or "00000000000"  # Fallback se não tiver CPF
        
        client = self._get_gerencianet_client()
        for parcela in parcelas:
            try:
                # Gerar boleto no Gerencianet
                resultado = client.gerar_boleto(
                    cliente_nome=cliente.nome,
                    cliente_cpf=cpf,
                    cliente_email=cliente.email,
                    valor=parcela.valor,
                    data_vencimento=parcela.data_vencimento,
                    numero_referencia=f"{carne.numero_carne}-{parcela.numero_parcela}",
                    descricao=f"Parcela {parcela.numero_parcela} de {carne.quantidade_parcelas}"
                )
                
                # Atualizar parcela com dados do boleto
                parcela.gerencianet_charge_id = resultado.get("charge_id")
                parcela.codigo_barras = resultado.get("codigo_barras")
                parcela.linha_digitavel = resultado.get("linha_digitavel")
                parcela.gerencianet_link_boleto = resultado.get("url_boleto")
                
            except Exception as e:
                print(f"Erro ao gerar boleto para parcela {parcela.numero_parcela}: {e}")
    
    def obter_carne(self, carne_id: int) -> CarneResponse:
        """Obtém um carnê pelo ID"""
        
        carne = self.session.query(CarneModel).filter(
            CarneModel.id == carne_id
        ).first()
        
        if not carne:
            raise NotFoundException("Carnê não encontrado")
        
        return self._model_to_response(carne)
    
    def listar_carnes_cliente(self, cliente_id: int) -> List[CarneResponse]:
        """Lista todos os carnês de um cliente"""
        
        carnes = self.session.query(CarneModel).filter(
            CarneModel.cliente_id == cliente_id,
            CarneModel.ativo == True
        ).order_by(CarneModel.data_criacao.desc()).all()
        
        return [self._model_to_response(c) for c in carnes]
    
    def atualizar_carne(self, carne_id: int, update_data: CarneUpdate) -> CarneResponse:
        """Atualiza um carnê"""
        
        carne = self.session.query(CarneModel).filter(
            CarneModel.id == carne_id
        ).first()
        
        if not carne:
            raise NotFoundException("Carnê não encontrado")
        
        # Não permitir atualizar certas informações se já tiver parcelas pagas
        parcelas_pagas = self.session.query(ParcelaModel).filter(
            ParcelaModel.carne_id == carne_id,
            ParcelaModel.status == "pago"
        ).count()
        
        if parcelas_pagas > 0 and update_data.valor_total is not None:
            raise ValidationException(
                "Não é possível alterar o valor total de um carnê com parcelas pagas"
            )
        
        # Atualizar campos
        if update_data.descricao is not None:
            carne.descricao = update_data.descricao
        
        if update_data.status is not None:
            carne.status = update_data.status
        
        if update_data.ativo is not None:
            carne.ativo = update_data.ativo
        
        carne.data_atualizacao = datetime.utcnow()
        
        self.session.commit()
        self.session.refresh(carne)
        
        return self._model_to_response(carne)
    
    def cancelar_carne(self, carne_id: int) -> CarneResponse:
        """
        Cancela um carnê e todas as suas parcelas pendentes
        """
        carne = self.session.query(CarneModel).filter(
            CarneModel.id == carne_id
        ).first()
        
        if not carne:
            raise NotFoundException("Carnê não encontrado")
        
        # Cancelar parcelas
        parcelas = self.session.query(ParcelaModel).filter(
            ParcelaModel.carne_id == carne_id
        ).all()
        
        for parcela in parcelas:
            # Cancelar no Gerencianet se houver charge_id
            if parcela.gerencianet_charge_id:
                try:
                    self._get_gerencianet_client().cancelar_boleto(
                        int(parcela.gerencianet_charge_id)
                    )
                except:
                    pass  # Log silencioso se falhar
            
            parcela.status = "cancelado"
        
        carne.status = "cancelado"
        carne.ativo = False
        carne.data_atualizacao = datetime.utcnow()
        
        self.session.commit()
        self.session.refresh(carne)
        
        return self._model_to_response(carne)

    def excluir_carne(self, carne_id: int) -> bool:
        """
        Exclui um carnê permanentemente se possível, ou faz soft delete (cancelar)
        """
        carne = self.session.query(CarneModel).filter(
            CarneModel.id == carne_id
        ).first()
        
        if not carne:
            raise NotFoundException("Carnê não encontrado")
            
        try:
            # Tenta cancelar no Gerencianet primeiro
            for parcela in carne.parcelas:
                if parcela.gerencianet_charge_id:
                    try:
                        self._get_gerencianet_client().cancelar_boleto(
                            int(parcela.gerencianet_charge_id)
                        )
                    except:
                        pass

            # Tenta exclusão física (hard delete)
            # Devido ao cascade="all, delete-orphan", as parcelas serão excluídas automaticamente
            self.session.delete(carne)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            # Se falhar a exclusão física (por exemplo, por chaves estrangeiras em pagamentos)
            # fazemos o soft delete (cancelar)
            self.cancelar_carne(carne_id)
            return True
    
    def registrar_pagamento_parcela(
        self,
        parcela_id: int,
        valor_pago: float
    ) -> None:
        """Registra o pagamento de uma parcela"""
        
        parcela = self.session.query(ParcelaModel).filter(
            ParcelaModel.id == parcela_id
        ).first()
        
        if not parcela:
            raise NotFoundException("Parcela não encontrada")
        
        if valor_pago <= 0:
            raise ValidationException("Valor pago deve ser maior que zero")
        
        # Registrar pagamento
        parcela.valor_pago = valor_pago
        parcela.data_pagamento = datetime.utcnow()
        
        if valor_pago >= parcela.valor:
            parcela.status = "pago"
        else:
            parcela.status = "parcial"
        
        # Verificar se todas as parcelas foram pagas
        carne = parcela.carne
        parcelas_pendentes = self.session.query(ParcelaModel).filter(
            ParcelaModel.carne_id == carne.id,
            ParcelaModel.status == "pendente"
        ).count()
        
        if parcelas_pendentes == 0:
            carne.status = "finalizado"
        
        self.session.commit()
    
    def listar_parcelas_carne(self, carne_id: int) -> List[dict]:
        """Lista todas as parcelas de um carnê"""
        
        parcelas = self.session.query(ParcelaModel).filter(
            ParcelaModel.carne_id == carne_id
        ).order_by(ParcelaModel.numero_parcela).all()
        
        return [
            {
                "id": p.id,
                "numero": p.numero_parcela,
                "valor": p.valor,
                "data_vencimento": p.data_vencimento,
                "status": p.status,
                "valor_pago": p.valor_pago,
                "codigo_barras": p.codigo_barras,
                "linha_digitavel": p.linha_digitavel,
                "link_boleto": p.gerencianet_link_boleto
            }
            for p in parcelas
        ]
    
    def _gerar_numero_carne(self, cliente_id: int) -> str:
        """Gera número único para o carnê"""
        
        count = self.session.query(CarneModel).filter(
            CarneModel.cliente_id == cliente_id
        ).count()
        
        agora = datetime.utcnow()
        return f"CARNE-{agora.year}{agora.month:02d}{agora.day:02d}-{cliente_id:04d}-{count + 1:03d}"
    
    def _model_to_response(self, carne: CarneModel) -> CarneResponse:
        """Converte model para response schema"""
        
        return CarneResponse(
            id=carne.id,
            cliente_id=carne.cliente_id,
            cliente_nome=carne.cliente.nome if carne.cliente else None,
            numero_carne=carne.numero_carne,
            valor_total=carne.valor_total,
            quantidade_parcelas=carne.quantidade_parcelas,
            valor_parcela=carne.valor_parcela,
            data_inicio=carne.data_inicio,
            data_primeiro_vencimento=carne.data_primeiro_vencimento,
            intervalo_dias=carne.intervalo_dias,
            descricao=carne.descricao,
            status=carne.status,
            gerencianet_subscription_id=carne.gerencianet_subscription_id,
            data_criacao=carne.data_criacao,
            data_atualizacao=carne.data_atualizacao,
            parcelas=[
                {
                    "id": p.id,
                    "numero_parcela": p.numero_parcela,
                    "valor": p.valor,
                    "data_vencimento": p.data_vencimento,
                    "status": p.status,
                    "valor_pago": p.valor_pago,
                    "data_pagamento": p.data_pagamento,
                    "codigo_barras": p.codigo_barras,
                    "linha_digitavel": p.linha_digitavel,
                    "gerencianet_charge_id": p.gerencianet_charge_id,
                    "gerencianet_link_boleto": p.gerencianet_link_boleto
                }
                for p in carne.parcelas
            ]
        )
