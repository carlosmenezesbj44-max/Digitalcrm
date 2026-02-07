"""Service para Contratos"""

from typing import Optional, List
from datetime import datetime, timedelta
from crm_modules.contratos.repository import ContratoRepository, ContratoHistoricoRepository
from crm_modules.contratos.domain import Contrato, StatusAssinatura
from crm_modules.contratos.schemas import ContratoCreate, ContratoUpdate
from crm_modules.contratos.pdf_generator import ContratosPDFGenerator
from crm_modules.clientes.service import ClienteService
from crm_core.utils.exceptions import NotFoundException, ValidationException
import hashlib
import os


class ContratoService:
    def __init__(self, repository: Optional[ContratoRepository] = None, repository_session=None, usuario_id: Optional[str] = None):
        if repository is not None:
            self.repository = repository
        else:
            self.repository = ContratoRepository(session=repository_session) if repository_session is not None else ContratoRepository()
        
        self.historico_repo = ContratoHistoricoRepository(session=self.repository.session)
        self.usuario_id = usuario_id or "SISTEMA"

    def criar_contrato(self, contrato_data: ContratoCreate, usuario_id: Optional[str] = None) -> Contrato:
        """Cria um novo contrato com geração de PDF, faturas automáticas e auditoria"""
        import logging
        logging.info(f"Criando contrato para cliente {contrato_data.cliente_id} por usuário {usuario_id}")
        usuario = usuario_id or self.usuario_id
        
        # Validar se cliente existe
        cliente_service = ClienteService(repository_session=self.repository.session)
        cliente = cliente_service.obter_cliente(contrato_data.cliente_id)
        if not cliente:
            raise NotFoundException("Cliente não encontrado")

        # Criar modelo ORM
        from crm_modules.contratos.models import ContratoModel, TipoContrato, StatusRenovacao
        
        # Calcular datas de pagamento
        data_inicio = contrato_data.data_vigencia_inicio or datetime.utcnow()
        data_primeiro_pagamento = contrato_data.data_primeiro_pagamento or self._calcular_data_primeiro_pagamento(
            data_inicio, 
            contrato_data.dia_pagamento
        )
        
        model = ContratoModel(
            cliente_id=contrato_data.cliente_id,
            titulo=contrato_data.titulo,
            descricao=contrato_data.descricao,
            tipo_contrato=contrato_data.tipo_contrato,
            data_vigencia_inicio=data_inicio,
            data_vigencia_fim=contrato_data.data_vigencia_fim,
            valor_contrato=contrato_data.valor_contrato,
            moeda=contrato_data.moeda,
            status_renovacao=contrato_data.status_renovacao,
            # Campos de pagamento
            data_primeiro_pagamento=data_primeiro_pagamento,
            data_proximo_pagamento=data_primeiro_pagamento,
            dia_pagamento=contrato_data.dia_pagamento,
            frequencia_pagamento=contrato_data.frequencia_pagamento,
            desconto_total=contrato_data.desconto_total,
            juros_atraso_percentual=contrato_data.juros_atraso_percentual,
            criado_por=usuario,
            atualizado_por=usuario
        )

        # Salvar primeiro para ter ID
        try:
            model = self.repository.create(model)
            logging.info(f"Contrato criado com ID {model.id}")
        except Exception as e:
            logging.error(f"Erro ao salvar contrato: {e}")
            raise

        # Gerar PDF se solicitado
        if contrato_data.incluir_pdf:
            try:
                arquivo_contrato = self._gerar_pdf_contrato(model)
                model.arquivo_contrato = arquivo_contrato
                model = self.repository.update(model)
            except Exception as e:
                print(f"Erro ao gerar PDF: {e}")
                # Continuar mesmo se PDF falhar

        # Registrar no histórico (não falhar se tabela não existir)
        try:
            self.historico_repo.registrar_alteracao(
                model.id,
                "status_assinatura",
                None,
                model.status_assinatura.value,
                usuario,
                "Contrato criado"
            )
        except Exception as e:
            print(f"Aviso: Não foi possível registrar histórico: {e}")

        # Gerar faturas automaticamente se valor está definido
        try:
            if model.valor_contrato and model.valor_contrato > 0:
                self._gerar_faturas_automaticas(model)
                logging.info(f"Faturas geradas automaticamente para contrato {model.id}")
        except Exception as e:
            logging.warning(f"Aviso: Não foi possível gerar faturas automáticas: {e}")

        # Atualizar status do cliente
        from crm_modules.clientes.models import ClienteModel
        cliente_model = self.repository.session.query(ClienteModel).filter(
            ClienteModel.id == contrato_data.cliente_id
        ).first()
        if cliente_model:
            cliente_model.status_contrato = "aguardando_assinatura"
            self.repository.session.add(cliente_model)
            self.repository.session.commit()

        return self._model_to_domain(model)

    def obter_contrato(self, contrato_id: int):
        """Busca contrato por ID"""
        model = self.repository.get_by_id(contrato_id)
        if not model:
            raise NotFoundException("Contrato não encontrado")

        return model

    def listar_contratos_por_cliente(self, cliente_id: int) -> List[Contrato]:
        """Lista todos os contratos de um cliente"""
        models = self.repository.get_contratos_by_cliente(cliente_id)
        return [self._model_to_domain(model) for model in models]

    def listar_todos_contratos(self, limite: int = 100, offset: int = 0) -> List[dict]:
        """Lista todos os contratos (com paginação) com dados do cliente"""
        models = self.repository.list(limit=limite, offset=offset)
        contratos = []
        for model in models:
            contrato_dict = self._model_to_dict(model)
            # Adicionar nome do cliente
            cliente_service = ClienteService(repository_session=self.repository.session)
            cliente = cliente_service.obter_cliente(model.cliente_id)
            contrato_dict['cliente_nome'] = cliente.nome if cliente else f'Cliente {model.cliente_id}'
            contratos.append(contrato_dict)
        return contratos

    def assinar_contrato(self, contrato_id: int, assinatura_base64: str, 
                        hash_documento: str, usuario_id: str = None, nome_signatario: str = None) -> Contrato:
        """Assina digitalmente um contrato com auditoria"""
        usuario = usuario_id or self.usuario_id
        
        model = self.repository.get_by_id(contrato_id)
        if not model:
            raise NotFoundException("Contrato não encontrado")

        if model.status_assinatura.value != "aguardando":
            raise ValidationException(f"Contrato não está aguardando assinatura (status: {model.status_assinatura.value})")

        # Validar hash do documento
        if model.arquivo_contrato and os.path.exists(model.arquivo_contrato):
            hash_calculado = self._calcular_hash_documento(model.arquivo_contrato)
            if hash_documento != hash_calculado:
                raise ValidationException("Hash do documento inválido - arquivo pode ter sido alterado")

        # Salvar assinatura
        assinatura_salva = self._salvar_assinatura(contrato_id, assinatura_base64)

        # Atualizar contrato
        from crm_modules.contratos.models import StatusAssinatura
        
        model.status_assinatura = StatusAssinatura.ASSINADO
        model.assinatura_digital = assinatura_salva
        model.data_assinatura = datetime.utcnow()
        model.hash_assinatura = hash_documento
        model.assinado_por = nome_signatario or usuario
        model.atualizado_por = usuario
        model.atualizado_em = datetime.utcnow()

        model = self.repository.update(model)

        # Registrar auditoria
        self.historico_repo.registrar_alteracao(
            contrato_id,
            "status_assinatura",
            "aguardando",
            "assinado",
            usuario,
            f"Contrato assinado digitalmente por {nome_signatario or usuario}"
        )

        return model

    def liberar_contrato(self, contrato_id: int, usuario_id: str = None, motivo: str = None) -> Contrato:
        """Libera contrato manualmente (admin) com auditoria"""
        usuario = usuario_id or self.usuario_id
        
        model = self.repository.get_by_id(contrato_id)
        if not model:
            raise NotFoundException("Contrato não encontrado")

        # Validar transição de status
        status_atual = model.status_assinatura.value
        if status_atual not in ["aguardando", "assinado"]:
            raise ValidationException(f"Não é possível liberar contrato em status {status_atual}")

        # Atualizar status
        from crm_modules.contratos.models import StatusAssinatura
        
        model.status_assinatura = StatusAssinatura.LIBERADO
        model.atualizado_por = usuario
        model.atualizado_em = datetime.utcnow()

        model = self.repository.update(model)

        # Registrar auditoria
        self.historico_repo.registrar_alteracao(
            contrato_id,
            "status_assinatura",
            status_atual,
            "liberado",
            usuario,
            motivo or "Contrato liberado manualmente por admin"
        )

        # Atualizar status do cliente
        from crm_modules.clientes.models import ClienteModel
        cliente_model = self.repository.session.query(ClienteModel).filter(
            ClienteModel.id == model.cliente_id
        ).first()
        if cliente_model:
            cliente_model.status_contrato = "assinado"
            self.repository.session.add(cliente_model)

        return self._model_to_domain(model)

    def obter_historico(self, contrato_id: int) -> list:
        """Obtém histórico de alterações do contrato"""
        historicos = self.historico_repo.get_historico_contrato(contrato_id)
        return [self._historico_to_dict(h) for h in historicos]

    def verificar_contratos_vencendo(self, dias: int = 30) -> List[Contrato]:
        """Verifica contratos que vencem em X dias"""
        models = self.repository.get_contratos_vencendo(dias)
        return [self._model_to_domain(model) for model in models]

    def verificar_contratos_vencidos(self) -> List[Contrato]:
        """Verifica contratos que já venceram"""
        models = self.repository.get_contratos_vencidos()
        return [self._model_to_domain(model) for model in models]

    def obter_estatisticas_contratos(self) -> dict:
        """Obtém estatísticas gerais dos contratos"""
        try:
            from sqlalchemy import func
            from crm_modules.contratos.models import ContratoModel, StatusAssinatura

            # Contar contratos por status
            status_counts = self.repository.session.query(
                ContratoModel.status_assinatura,
                func.count(ContratoModel.id).label('count')
            ).group_by(ContratoModel.status_assinatura).all()

            # Converter para dicionário
            stats = {
                'total': 0,
                'aguardando': 0,
                'assinado': 0,
                'liberado': 0,
                'vencendo_30_dias': len(self.verificar_contratos_vencendo(30)),
                'vencidos': len(self.verificar_contratos_vencidos())
            }

            for status, count in status_counts:
                # Usar o valor do enum como chave string
                status_key = status.value if hasattr(status, 'value') else str(status)
                stats[status_key] = count
                stats['total'] += count

            return stats
        except Exception as e:
            print(f"Erro ao obter estatísticas: {e}")
            return {
                'total': 0,
                'aguardando': 0,
                'assinado': 0,
                'liberado': 0,
                'vencendo_30_dias': 0,
                'vencidos': 0
            }

    def listar_contratos_filtrados(self, 
                                  data_inicio: Optional[datetime] = None,
                                  data_fim: Optional[datetime] = None,
                                  nome: Optional[str] = None,
                                  cpf: Optional[str] = None,
                                  status_assinatura: Optional[str] = None,
                                  status_cliente: Optional[str] = None) -> List[dict]:
        """Lista contratos com filtros e retorna como dicionários para a UI"""
        models = self.repository.listar_contratos_filtrados(
            data_inicio=data_inicio,
            data_fim=data_fim,
            nome=nome,
            cpf=cpf,
            status_assinatura=status_assinatura,
            status_cliente=status_cliente
        )
        
        result = []
        for model in models:
            # Buscar cliente para dados adicionais se necessário
            cliente_nome = "N/A"
            if hasattr(model, 'cliente') and model.cliente:
                cliente_nome = model.cliente.nome
            
            result.append({
                "id": model.id,
                "cliente_id": model.cliente_id,
                "cliente_nome": cliente_nome,
                "cliente_cpf": model.cliente.cpf if hasattr(model, 'cliente') and model.cliente else "N/A",
                "cliente_status": model.cliente.status_cliente if hasattr(model, 'cliente') and model.cliente else "N/A",
                "titulo": model.titulo,
                "tipo_contrato": model.tipo_contrato.value if hasattr(model.tipo_contrato, 'value') else (model.tipo_contrato or "Padrão"),
                "valor_contrato": model.valor_contrato or 0,
                "status_assinatura": model.status_assinatura.value if hasattr(model.status_assinatura, 'value') else (model.status_assinatura or "pendente"),
                "data_criacao": model.data_criacao,
                "data_vigencia_fim": model.data_vigencia_fim
            })
            
        return result

    def renovar_contrato_automatico(self, contrato_id: int, usuario_id: str = None) -> Contrato:
        """Renova automaticamente um contrato"""
        usuario = usuario_id or self.usuario_id
        
        contrato_atual = self.repository.get_by_id(contrato_id)
        if not contrato_atual:
            raise NotFoundException("Contrato não encontrado")

        from crm_modules.contratos.models import ContratoModel, StatusRenovacao
        
        # Verificar se está configurado para renovação automática
        if contrato_atual.status_renovacao.value != "renovacao_automatica":
            raise ValidationException("Contrato não está configurado para renovação automática")

        # Criar novo contrato baseado no anterior
        novo_contrato = ContratoModel(
            cliente_id=contrato_atual.cliente_id,
            titulo=f"{contrato_atual.titulo} (Renovação {datetime.now().year})",
            descricao=contrato_atual.descricao,
            tipo_contrato=contrato_atual.tipo_contrato,
            data_vigencia_inicio=contrato_atual.data_vigencia_fim + timedelta(days=1),
            data_vigencia_fim=contrato_atual.data_vigencia_fim + timedelta(days=365),
            valor_contrato=contrato_atual.valor_contrato,
            moeda=contrato_atual.moeda,
            status_renovacao=contrato_atual.status_renovacao,
            criado_por=usuario
        )

        novo_contrato = self.repository.create(novo_contrato)

        # Registrar relacionamento
        contrato_atual.proximo_contrato_id = novo_contrato.id
        self.repository.update(contrato_atual)

        # Registrar auditoria
        self.historico_repo.registrar_alteracao(
            contrato_id,
            "proximo_contrato_id",
            None,
            str(novo_contrato.id),
            usuario,
            f"Contrato renovado automaticamente (ID novo contrato: {novo_contrato.id})"
        )

        return self._model_to_domain(novo_contrato)

    def deletar_contrato(self, contrato_id: int, usuario_id: str = None, motivo: str = None) -> bool:
        """Deleta um contrato (soft delete) com auditoria"""
        usuario = usuario_id or self.usuario_id
        
        model = self.repository.get_by_id(contrato_id)
        if not model:
            raise NotFoundException("Contrato não encontrado")
        
        # Registrar auditoria antes de deletar
        try:
            self.historico_repo.registrar_alteracao(
                contrato_id,
                "status",
                model.status_assinatura.value,
                "deletado",
                usuario,
                motivo or "Contrato removido pelo usuário"
            )
        except Exception as e:
            print(f"Aviso: Não foi possível registrar histórico de exclusão: {e}")

        # Executar soft delete
        result = self.repository.soft_delete(contrato_id)
        
        # Se era o único contrato ativo, atualizar status do cliente?
        # Por enquanto vamos apenas deletar o contrato.
        
        return result is not None

    def _model_to_domain(self, model) -> Contrato:
        """Converte modelo ORM para domínio"""
        from crm_modules.contratos.models import TipoContrato
        return Contrato(
            id=model.id,
            cliente_id=model.cliente_id,
            titulo=model.titulo,
            descricao=model.descricao,
            status_assinatura=StatusAssinatura(model.status_assinatura.value),
            tipo_contrato=TipoContrato(model.tipo_contrato.value) if model.tipo_contrato else TipoContrato.SERVICO,
            data_criacao=model.data_criacao,
            data_assinatura=model.data_assinatura,
            arquivo_contrato=model.arquivo_contrato,
            hash_assinatura=model.hash_assinatura,
            assinatura_digital=model.assinatura_digital,
            observacoes=model.observacoes
        )

    def _model_to_dict(self, model) -> dict:
        """Converte modelo ORM para dicionário"""
        return {
            "id": model.id,
            "cliente_id": model.cliente_id,
            "titulo": model.titulo,
            "descricao": model.descricao,
            "status_assinatura": model.status_assinatura.value if model.status_assinatura else "aguardando",
            "tipo_contrato": model.tipo_contrato.value if model.tipo_contrato else "servico",
            "data_criacao": model.data_criacao.isoformat() if model.data_criacao else None,
            "data_assinatura": model.data_assinatura.isoformat() if model.data_assinatura else None,
            "arquivo_contrato": model.arquivo_contrato,
            "hash_assinatura": model.hash_assinatura,
            "assinatura_digital": model.assinatura_digital,
            "observacoes": model.observacoes,
            "data_vigencia_inicio": model.data_vigencia_inicio.isoformat() if model.data_vigencia_inicio else None,
            "data_vigencia_fim": model.data_vigencia_fim.isoformat() if model.data_vigencia_fim else None,
            "valor_contrato": model.valor_contrato,
            "moeda": model.moeda,
            "status_renovacao": model.status_renovacao.value if model.status_renovacao else "renovacao_manual",
            "dia_pagamento": model.dia_pagamento,
            "frequencia_pagamento": model.frequencia_pagamento,
            "desconto_total": model.desconto_total,
            "juros_atraso_percentual": model.juros_atraso_percentual,
            "data_primeiro_pagamento": model.data_primeiro_pagamento.isoformat() if model.data_primeiro_pagamento else None,
            "data_proximo_pagamento": model.data_proximo_pagamento.isoformat() if model.data_proximo_pagamento else None
        }

    def gerar_pdf_contrato(self, contrato_id: int, empresa_dados: Optional[dict] = None) -> bytes:
        """Gera PDF do contrato existente e retorna bytes"""
        try:
            # Buscar contrato
            model = self.repository.get_by_id(contrato_id)
            if not model:
                raise NotFoundException("Contrato não encontrado")

            # Usar o gerador de PDF padrão
            from crm_modules.contratos.pdf_generator import ContratosPDFGenerator

            generator = ContratosPDFGenerator(
                contrato=model,
                template_html=None
            )

            pdf_bytes = generator.gerar_pdf()
            return pdf_bytes
        except Exception as e:
            raise Exception(f"Erro ao gerar PDF: {str(e)}")

    def _gerar_pdf_contrato(self, model) -> str:
        """Gera PDF do contrato usando ReportLab ou template"""
        try:
            from crm_core.config.settings import settings
            template_html = settings.contract_template_html if settings.contract_template_html else None
            generator = ContratosPDFGenerator(model, template_html)
            pdf_bytes = generator.gerar_pdf()

            # Salvar arquivo
            os.makedirs("interfaces/web/static/contratos", exist_ok=True)
            filename = f"contrato_{model.id}_{model.cliente_id}.pdf"
            filepath = f"interfaces/web/static/contratos/{filename}"

            with open(filepath, 'wb') as f:
                f.write(pdf_bytes)

            print(f"[PDF] Arquivo salvo: {filepath}, retornando filename: {filename}")
            return filename
        except Exception as e:
            raise Exception(f"Erro ao gerar PDF: {str(e)}")

    def _salvar_assinatura(self, contrato_id: int, assinatura_base64: str) -> str:
        """Salva assinatura digital com validação"""
        try:
            import base64
            
            # Validar base64
            assinatura_bytes = base64.b64decode(assinatura_base64)
            
            # Salvar em arquivo
            os.makedirs("interfaces/web/static/assinaturas", exist_ok=True)
            filename = f"assinatura_{contrato_id}_{datetime.utcnow().timestamp()}.png"
            filepath = f"interfaces/web/static/assinaturas/{filename}"
            
            with open(filepath, 'wb') as f:
                f.write(assinatura_bytes)
            
            return filepath
        except Exception as e:
            raise Exception(f"Erro ao salvar assinatura: {str(e)}")

    def _calcular_hash_documento(self, filepath: str) -> str:
        """Calcula hash SHA256 do arquivo do contrato"""
        if not os.path.exists(filepath):
            return ""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return ""

    def _historico_to_dict(self, historico) -> dict:
        """Converte histórico para dicionário"""
        return {
            "id": historico.id,
            "campo_alterado": historico.campo_alterado,
            "valor_anterior": historico.valor_anterior,
            "valor_novo": historico.valor_novo,
            "alterado_por": historico.alterado_por,
            "alterado_em": historico.alterado_em.isoformat() if historico.alterado_em else None,
            "motivo": historico.motivo
        }

    def _calcular_data_primeiro_pagamento(self, data_inicio: datetime, dia_pagamento: int) -> datetime:
        """Calcula a data do primeiro pagamento baseado no dia de vencimento"""
        from datetime import date
        
        # Se o dia de pagamento já passou neste mês, primeiro pagamento é no próximo mês
        hoje = datetime.utcnow().date()
        primeiro_vencimento = data_inicio.date().replace(day=min(dia_pagamento, 28))
        
        # Se a data calculada é anterior ao início do contrato, move para o próximo mês
        if primeiro_vencimento < data_inicio.date():
            # Próximo mês
            if data_inicio.month == 12:
                primeiro_vencimento = primeiro_vencimento.replace(year=data_inicio.year + 1, month=1)
            else:
                primeiro_vencimento = primeiro_vencimento.replace(month=data_inicio.month + 1)
        
        return datetime.combine(primeiro_vencimento, datetime.min.time())

    def _gerar_cronograma_pagamentos_html(self, model) -> str:
        """Gera cronograma de pagamentos em HTML para o PDF"""
        from dateutil.relativedelta import relativedelta
        
        html_rows = ""
        data_vencimento = model.data_proximo_pagamento.date()
        
        # Gerar faturas mensalmente até a data de vigência fim ou por 12 meses
        num_faturas = 12
        if model.data_vigencia_fim:
            delta = relativedelta(model.data_vigencia_fim.date(), data_vencimento)
            num_faturas = max(delta.years * 12 + delta.months + 1, 1)
        
        valor_mensal = model.valor_contrato or 0
        desconto = model.desconto_total or 0
        valor_liquido = valor_mensal - desconto if desconto else valor_mensal
        
        for i in range(min(num_faturas, 12)):  # Limita a 12 linhas no cronograma
            # Aplicar frequência
            if model.frequencia_pagamento == "mensal":
                vencimento = data_vencimento + timedelta(days=30*i)
            elif model.frequencia_pagamento == "bimestral":
                vencimento = data_vencimento + timedelta(days=60*i)
            elif model.frequencia_pagamento == "trimestral":
                vencimento = data_vencimento + timedelta(days=90*i)
            elif model.frequencia_pagamento == "semestral":
                vencimento = data_vencimento + timedelta(days=180*i)
            elif model.frequencia_pagamento == "anual":
                vencimento = data_vencimento + timedelta(days=365*i)
            else:
                vencimento = data_vencimento + timedelta(days=30*i)
            
            # Não incluir faturas além da vigência
            if model.data_vigencia_fim and vencimento > model.data_vigencia_fim.date():
                break
            
            data_formatada = vencimento.strftime("%d/%m/%Y")
            valor_formatado = f"R$ {valor_liquido:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
            
            html_rows += f"""
            <tr>
                <td class="text-center">{i+1}</td>
                <td>{data_formatada}</td>
                <td class="text-right">{valor_formatado}</td>
                <td>Parcela {i+1}/{num_faturas}</td>
            </tr>
            """
        
        return html_rows

    def _gerar_faturas_automaticas(self, model):
        """Gera faturas automáticas para o contrato baseado na frequência de pagamento"""
        from crm_modules.faturamento.service import FaturaService
        from datetime import date
        from dateutil.relativedelta import relativedelta
        
        try:
            fatura_service = FaturaService(repository_session=self.repository.session)
            
            # Calcular quantas faturas devem ser geradas até a data de vigência fim
            data_vencimento = model.data_proximo_pagamento.date()
            
            # Gerar faturas mensalmente até a data de vigência fim ou por 12 meses (padrão)
            num_faturas = 12  # Padrão: 12 meses
            
            if model.data_vigencia_fim:
                # Calcular diferença em meses
                delta = relativedelta(model.data_vigencia_fim.date(), data_vencimento)
                num_faturas = delta.years * 12 + delta.months + 1
            
            valor_mensal = model.valor_contrato
            desconto = model.desconto_total
            
            for i in range(num_faturas):
                # Aplicar frequência de pagamento
                if model.frequencia_pagamento == "mensal":
                    vencimento = data_vencimento + timedelta(days=30*i)
                elif model.frequencia_pagamento == "bimestral":
                    vencimento = data_vencimento + timedelta(days=60*i)
                elif model.frequencia_pagamento == "trimestral":
                    vencimento = data_vencimento + timedelta(days=90*i)
                elif model.frequencia_pagamento == "semestral":
                    vencimento = data_vencimento + timedelta(days=180*i)
                elif model.frequencia_pagamento == "anual":
                    vencimento = data_vencimento + timedelta(days=365*i)
                else:
                    vencimento = data_vencimento + timedelta(days=30*i)
                
                # Não gerar faturas futuras além da vigência
                if model.data_vigencia_fim and vencimento > model.data_vigencia_fim.date():
                    break
                
                # Calcular valor com desconto
                valor_fatura = valor_mensal - desconto if desconto else valor_mensal
                
                # Gerar número único da fatura
                numero_fatura = f"FAT-{model.id:04d}-{i+1:02d}"
                
                # Criar fatura (simples)
                try:
                    from crm_modules.faturamento.models import FaturaModel
                    fatura = FaturaModel(
                        cliente_id=model.cliente_id,
                        numero_fatura=numero_fatura,
                        data_vencimento=vencimento,
                        valor_total=valor_fatura,
                        status="pendente",
                        descricao=f"Fatura referente ao contrato {model.titulo}"
                    )
                    self.repository.session.add(fatura)
                except Exception as e:
                    print(f"Aviso ao criar fatura {numero_fatura}: {e}")
            
            self.repository.session.commit()
        except ImportError:
            print("Aviso: FaturaService não disponível para gerar faturas automáticas")
        except Exception as e:
            print(f"Erro ao gerar faturas automáticas: {e}")
            self.repository.session.rollback()