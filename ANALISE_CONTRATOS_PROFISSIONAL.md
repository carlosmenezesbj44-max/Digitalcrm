# Análise Completa da Área de Contratos - CRM Profissional

## 1. STATUS ATUAL DO MÓDULO

### ✅ O que está implementado:
- **Estrutura de dados básica** (models, schemas, domain, repository)
- **API REST** com endpoints para CRUD
- **Interface básica** em HTML para visualização
- **Fluxo de assinatura** (aguardando → assinado → liberado)
- **Relacionamentos** com cliente

### ⚠️ Problemas Identificados:

#### 1.1 **Falta de Funcionalidades Críticas para Profissionalismo**

| Funcionalidade | Status | Impacto |
|---|---|---|
| Geração de PDF automática | ❌ Não implementado | Alto - Essencial para contratos |
| Assinatura Digital Real | ❌ Apenas mock | Alto - Segurança jurídica |
| Versionamento de contratos | ❌ Não existe | Alto - Rastreabilidade |
| Histórico de alterações | ❌ Não existe | Alto - Auditoria |
| Notificações por email | ❌ Não implementado | Alto - UX do cliente |
| Pesquisa e filtros avançados | ❌ Não existe | Médio |
| Bulk actions | ❌ Não existe | Médio |
| Dashboard com métricas | ❌ Não existe | Médio |
| Integração com assinatura digital | ❌ Apenas local | Alto - Validação legal |
| Renovação automática de contratos | ❌ Não existe | Alto |
| Templates customizáveis | ❌ Não existe | Médio |

#### 1.2 **Problemas de Segurança**

```python
# API atual (crm_modules/contratos/api.py)
@router.post("/{contrato_id}/liberar")
def liberar_contrato(contrato_id: int, db: Session = Depends(get_db)):
    # ❌ Não há validação de permissão aqui
    # ❌ Falta auditoria de quem liberou
    verificar_permissao("manage", "contratos")  # Genérica demais
```

**Recomendações de segurança:**
- Implementar auditoria detalhada (quem, quando, por quê)
- Registrar todas as mudanças de status
- Validação de assinatura digital com certificado
- Encrypt de dados sensíveis
- Limitar acesso por perfil de usuário

#### 1.3 **Problemas de UX**

**Frontend:**
- ❌ Formulário de criação não existe (rota existe mas sem implementação)
- ❌ Detalhes de contrato com TODO (não implementado)
- ❌ Sem validação de formulário
- ❌ Sem upload de arquivo (apenas campo de texto)
- ❌ Sem preview de PDF
- ❌ Sem assinatura digital visual (desenhar assinatura)

**Backend:**
- ❌ Sem tratamento de erros detalhado
- ❌ Respostas genéricas de erro
- ❌ Sem paginação na listagem
- ❌ Sem cache de dados

#### 1.4 **Problemas de Banco de Dados**

```python
# Modelo atual - Faltas importantes
class ContratoModel(Base):
    # ❌ Sem data de expiração
    # ❌ Sem valor do contrato (financeiro)
    # ❌ Sem tipo de contrato
    # ❌ Sem período de vigência
    # ❌ Sem campo de assinante (nome)
    # ❌ Sem status de renovação
    # ❌ Sem relacionamento com planos/produtos
    # ❌ Sem soft delete
    # ❌ Sem campos de auditoria (criado_por, atualizado_por, atualizado_em)
```

#### 1.5 **Problemas de Fluxo de Negócio**

- ❌ Sem integração com planos/produtos
- ❌ Sem ciclo de renovação automática
- ❌ Sem aviso de expiração
- ❌ Sem relatórios de contratos vencidos
- ❌ Sem histórico de versões
- ❌ Sem template de contrato padrão

---

## 2. PLANO DE MELHORIA - PROFISSIONALIZAÇÃO

### **FASE 1: Melhorias Críticas (Prioridade ALTA)**

#### 2.1.1 Expandir Modelo de Dados

```python
# crm_modules/contratos/models.py
from enum import Enum
from datetime import datetime, timedelta

class TipoContrato(str, Enum):
    SERVICO = "servico"          # Contrato de prestação de serviço
    ASSINATURA = "assinatura"    # Contrato de assinatura/plano
    MANUTENCAO = "manutencao"    # Contrato de manutenção
    SUPORTE = "suporte"          # Contrato de suporte
    OUTRO = "outro"

class StatusRenovacao(str, Enum):
    NAO_RENOVAVEL = "nao_renovavel"
    RENOVACAO_AUTOMATICA = "renovacao_automatica"
    RENOVACAO_MANUAL = "renovacao_manual"
    EXPIRADO = "expirado"

class ContratoModel(Base):
    __tablename__ = "contratos"

    # Campos existentes
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text)
    status_assinatura = Column(Enum(StatusAssinatura), default=StatusAssinatura.AGUARDANDO)
    
    # ✨ NOVOS CAMPOS
    tipo_contrato = Column(Enum(TipoContrato), default=TipoContrato.SERVICO)
    
    # Datas críticas
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_assinatura = Column(DateTime, nullable=True)
    data_vigencia_inicio = Column(DateTime, nullable=False)  # Quando começa a valer
    data_vigencia_fim = Column(DateTime, nullable=False)     # Quando expira
    data_notificacao_renovacao = Column(DateTime, nullable=True)  # Data para avisar renovação
    
    # Financeiro
    valor_contrato = Column(Float, nullable=True)  # Valor total do contrato
    moeda = Column(String(3), default="BRL")       # Moeda
    
    # Assinatura e auditoria
    arquivo_contrato = Column(String)
    hash_assinatura = Column(String, nullable=True)
    assinatura_digital = Column(Text, nullable=True)
    assinado_por = Column(String, nullable=True)   # Nome do signatário
    
    # Renovação
    status_renovacao = Column(Enum(StatusRenovacao), default=StatusRenovacao.RENOVACAO_MANUAL)
    proximo_contrato_id = Column(Integer, ForeignKey("contratos.id"), nullable=True)  # Contrato de renovação
    
    # Relacionamentos com outros dados
    plano_id = Column(Integer, ForeignKey("planos.id"), nullable=True)  # Se for plano
    produto_ids = Column(String, nullable=True)  # JSON com IDs de produtos
    
    # Observações
    observacoes = Column(Text)
    
    # ✨ CAMPOS DE AUDITORIA
    criado_por = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_por = Column(String, nullable=True)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deletado_em = Column(DateTime, nullable=True)  # Soft delete
    
    # Relacionamentos
    cliente = relationship("ClienteModel", back_populates="contratos")
    plano = relationship("PlanoModel", foreign_keys=[plano_id])
    historiador = relationship("ContratoHistoricoModel", back_populates="contrato", cascade="all, delete-orphan")
```

#### 2.1.2 Tabela de Histórico e Auditoria

```python
class ContratoHistoricoModel(Base):
    __tablename__ = "contratos_historico"
    
    id = Column(Integer, primary_key=True, index=True)
    contrato_id = Column(Integer, ForeignKey("contratos.id"), nullable=False)
    
    # O que mudou
    campo_alterado = Column(String(100), nullable=False)  # "status_assinatura", "data_vigencia_fim", etc
    valor_anterior = Column(String, nullable=True)
    valor_novo = Column(String, nullable=True)
    
    # Quem e quando
    alterado_por = Column(String, nullable=False)
    alterado_em = Column(DateTime, default=datetime.utcnow)
    
    # Contexto
    motivo = Column(String(500), nullable=True)  # Por que mudou?
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    # Relacionamento
    contrato = relationship("ContratoModel", back_populates="historiador")
```

#### 2.1.3 Geração de PDF com ReportLab

```python
# crm_modules/contratos/pdf_generator.py
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from datetime import datetime
import io

class ContratosPDFGenerator:
    def __init__(self, contrato):
        self.contrato = contrato
        self.styles = getSampleStyleSheet()
    
    def gerar_pdf(self) -> bytes:
        """Gera PDF do contrato"""
        # Buffer em memória
        buffer = io.BytesIO()
        
        # Criar documento
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        # Cabeçalho com logo
        story.append(self._criar_cabecalho())
        story.append(Spacer(1, 0.3*inch))
        
        # Título
        titulo = Paragraph(
            f"<b>{self.contrato.titulo}</b>",
            self.styles['Heading1']
        )
        story.append(titulo)
        story.append(Spacer(1, 0.2*inch))
        
        # Dados principais
        story.append(self._criar_dados_principais())
        story.append(Spacer(1, 0.2*inch))
        
        # Descrição
        if self.contrato.descricao:
            descricao = Paragraph(
                f"<b>Descrição:</b><br/>{self.contrato.descricao}",
                self.styles['BodyText']
            )
            story.append(descricao)
            story.append(Spacer(1, 0.2*inch))
        
        # Datas importantes
        story.append(self._criar_datas())
        story.append(Spacer(1, 0.2*inch))
        
        # Informações financeiras
        if self.contrato.valor_contrato:
            story.append(self._criar_info_financeira())
            story.append(Spacer(1, 0.2*inch))
        
        # Assinatura
        story.append(Spacer(1, 0.5*inch))
        story.append(self._criar_area_assinatura())
        
        # Rodapé
        story.append(Spacer(1, 0.3*inch))
        story.append(self._criar_rodape())
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def _criar_cabecalho(self):
        """Cria cabeçalho do documento"""
        data = [[
            "CONTRATO DE SERVIÇO",
            f"ID: {self.contrato.id}"
        ]]
        table = Table(data, colWidths=[4*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0d47a1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        return table
    
    def _criar_dados_principais(self):
        """Dados do cliente e contrato"""
        data = [
            ['CLIENTE', 'TIPO DE CONTRATO', 'STATUS'],
            [
                self.contrato.cliente.nome_fantasia or self.contrato.cliente.razao_social,
                self.contrato.tipo_contrato.value,
                self.contrato.status_assinatura.value
            ]
        ]
        table = Table(data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table
    
    def _criar_datas(self):
        """Datas importantes"""
        data = [
            ['DATA CRIAÇÃO', 'VIGÊNCIA INICIO', 'VIGÊNCIA FIM'],
            [
                self.contrato.data_criacao.strftime('%d/%m/%Y'),
                self.contrato.data_vigencia_inicio.strftime('%d/%m/%Y'),
                self.contrato.data_vigencia_fim.strftime('%d/%m/%Y')
            ]
        ]
        table = Table(data, colWidths=[2*inch, 2*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table
    
    def _criar_info_financeira(self):
        """Informações financeiras"""
        valor_formatado = f"R$ {self.contrato.valor_contrato:,.2f}"
        data = [
            ['VALOR DO CONTRATO', 'MOEDA', 'VIGÊNCIA'],
            [valor_formatado, self.contrato.moeda, 'Ver datas acima']
        ]
        table = Table(data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table
    
    def _criar_area_assinatura(self):
        """Área para assinatura"""
        paragrafo = Paragraph(
            "<br/><br/>________________________<br/><b>ASSINADO PELO CLIENTE</b><br/>Data: ___/___/_____",
            self.styles['Normal']
        )
        return paragrafo
    
    def _criar_rodape(self):
        """Rodapé do documento"""
        rodape = Paragraph(
            f"<i>Documento gerado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}<br/>"
            f"Referência: CRM-{self.contrato.id}</i>",
            self.styles['Normal']
        )
        return rodape
```

#### 2.1.4 Service Melhorado com Auditoria

```python
# crm_modules/contratos/service.py
from crm_modules.contratos.pdf_generator import ContratosPDFGenerator
from crm_modules.contratos.repository import ContratoRepository, ContratoHistoricoRepository
from datetime import datetime, timedelta

class ContratoService:
    def __init__(self, repository_session=None, usuario_id=None):
        self.repository = ContratoRepository(session=repository_session)
        self.historico_repo = ContratoHistoricoRepository(session=repository_session)
        self.usuario_id = usuario_id
    
    def criar_contrato(self, contrato_data: ContratoCreate, usuario_id: str) -> Contrato:
        """Cria contrato com auditoria"""
        
        # Validar cliente
        cliente_service = ClienteService()
        cliente = cliente_service.obter_cliente(contrato_data.cliente_id)
        if not cliente:
            raise ValueError("Cliente não encontrado")
        
        # Criar modelo
        contrato = ContratoModel(
            cliente_id=contrato_data.cliente_id,
            titulo=contrato_data.titulo,
            descricao=contrato_data.descricao,
            tipo_contrato=contrato_data.tipo_contrato,
            data_vigencia_inicio=contrato_data.data_vigencia_inicio or datetime.utcnow(),
            data_vigencia_fim=contrato_data.data_vigencia_fim,
            valor_contrato=contrato_data.valor_contrato,
            status_renovacao=contrato_data.status_renovacao,
            criado_por=usuario_id,
            atualizado_por=usuario_id,
        )
        
        # Gerar PDF
        if contrato_data.incluir_pdf:
            pdf_generator = ContratosPDFGenerator(contrato)
            pdf_bytes = pdf_generator.gerar_pdf()
            # Salvar arquivo (usar storage service)
            arquivo_path = self._salvar_pdf(pdf_bytes, contrato.id)
            contrato.arquivo_contrato = arquivo_path
        
        # Salvar
        contrato_salvo = self.repository.create(contrato)
        
        # Registrar auditoria
        self._registrar_auditoria(
            contrato_salvo.id,
            "status_assinatura",
            None,
            "aguardando",
            usuario_id,
            "Contrato criado"
        )
        
        # Notificar cliente
        self._notificar_cliente_novo_contrato(contrato_salvo)
        
        return contrato_salvo
    
    def liberar_contrato(self, contrato_id: int, usuario_id: str, motivo: str = None) -> Contrato:
        """Libera contrato com auditoria completa"""
        
        contrato = self.repository.get(contrato_id)
        if not contrato:
            raise ValueError("Contrato não encontrado")
        
        # Validar transição de status
        if contrato.status_assinatura not in [StatusAssinatura.AGUARDANDO, StatusAssinatura.ASSINADO]:
            raise ValueError(f"Não é possível liberar contrato em status {contrato.status_assinatura.value}")
        
        status_anterior = contrato.status_assinatura.value
        
        # Atualizar
        contrato.status_assinatura = StatusAssinatura.LIBERADO
        contrato.atualizado_por = usuario_id
        contrato.atualizado_em = datetime.utcnow()
        
        contrato_atualizado = self.repository.update(contrato)
        
        # Registrar auditoria
        self._registrar_auditoria(
            contrato_id,
            "status_assinatura",
            status_anterior,
            "liberado",
            usuario_id,
            motivo or "Contrato liberado manualmente"
        )
        
        # Notificar cliente
        self._notificar_cliente_liberacao(contrato_atualizado)
        
        return contrato_atualizado
    
    def assinar_contrato(self, contrato_id: int, assinatura_base64: str, 
                        usuario_id: str, hash_documento: str = None) -> Contrato:
        """Assina contrato com validação"""
        
        contrato = self.repository.get(contrato_id)
        if not contrato:
            raise ValueError("Contrato não encontrado")
        
        if contrato.status_assinatura != StatusAssinatura.AGUARDANDO:
            raise ValueError("Contrato não está aguardando assinatura")
        
        # Validar e salvar assinatura
        assinatura_salva = self._salvar_assinatura(contrato_id, assinatura_base64)
        
        # Atualizar contrato
        contrato.status_assinatura = StatusAssinatura.ASSINADO
        contrato.assinatura_digital = assinatura_salva
        contrato.data_assinatura = datetime.utcnow()
        contrato.hash_assinatura = hash_documento
        contrato.assinado_por = usuario_id
        contrato.atualizado_por = usuario_id
        
        contrato_atualizado = self.repository.update(contrato)
        
        # Registrar auditoria
        self._registrar_auditoria(
            contrato_id,
            "status_assinatura",
            StatusAssinatura.AGUARDANDO.value,
            StatusAssinatura.ASSINADO.value,
            usuario_id,
            f"Contrato assinado digitalmente"
        )
        
        # Notificar admin
        self._notificar_admin_contrato_assinado(contrato_atualizado)
        
        return contrato_atualizado
    
    def verificar_contratos_vencidos(self):
        """Verifica contratos que estão prestes a vencer"""
        dias_alerta = 30
        data_limite = datetime.utcnow() + timedelta(days=dias_alerta)
        
        contratos_vencendo = self.repository.find_by_criteria({
            'data_vigencia_fim': ('<=', data_limite),
            'status_assinatura': StatusAssinatura.LIBERADO,
            'status_renovacao': ('!=', StatusRenovacao.NAO_RENOVAVEL),
            'data_notificacao_renovacao': ('is', None)
        })
        
        for contrato in contratos_vencendo:
            self._notificar_renovacao_proxima(contrato)
            contrato.data_notificacao_renovacao = datetime.utcnow()
            self.repository.update(contrato)
    
    def renovar_contrato_automatico(self, contrato_id: int):
        """Renova automaticamente contrato se configurado"""
        contrato = self.repository.get(contrato_id)
        
        if contrato.status_renovacao != StatusRenovacao.RENOVACAO_AUTOMATICA:
            raise ValueError("Contrato não está configurado para renovação automática")
        
        # Criar novo contrato baseado no anterior
        novo_contrato = ContratoModel(
            cliente_id=contrato.cliente_id,
            titulo=f"{contrato.titulo} (Renovação)",
            descricao=contrato.descricao,
            tipo_contrato=contrato.tipo_contrato,
            plano_id=contrato.plano_id,
            data_vigencia_inicio=contrato.data_vigencia_fim + timedelta(days=1),
            data_vigencia_fim=contrato.data_vigencia_fim + timedelta(days=365),
            valor_contrato=contrato.valor_contrato,
            status_renovacao=contrato.status_renovacao,
            criado_por="SISTEMA",
        )
        
        novo_contrato_salvo = self.repository.create(novo_contrato)
        
        # Registrar relacionamento
        contrato.proximo_contrato_id = novo_contrato_salvo.id
        self.repository.update(contrato)
        
        # Notificar
        self._notificar_contrato_renovado(novo_contrato_salvo)
        
        return novo_contrato_salvo
    
    def _registrar_auditoria(self, contrato_id: int, campo: str, valor_anterior: str,
                            valor_novo: str, usuario_id: str, motivo: str):
        """Registra histórico de alteração"""
        historico = ContratoHistoricoModel(
            contrato_id=contrato_id,
            campo_alterado=campo,
            valor_anterior=valor_anterior,
            valor_novo=valor_novo,
            alterado_por=usuario_id,
            alterado_em=datetime.utcnow(),
            motivo=motivo
        )
        self.historico_repo.create(historico)
    
    def _notificar_cliente_novo_contrato(self, contrato: ContratoModel):
        """Envia email ao cliente com novo contrato"""
        # Usar EmailService
        pass
    
    def _notificar_cliente_liberacao(self, contrato: ContratoModel):
        """Notifica cliente que contrato foi liberado"""
        pass
    
    def _notificar_admin_contrato_assinado(self, contrato: ContratoModel):
        """Notifica admin que contrato foi assinado"""
        pass
    
    def _notificar_renovacao_proxima(self, contrato: ContratoModel):
        """Notifica sobre renovação próxima"""
        pass
    
    def _notificar_contrato_renovado(self, contrato: ContratoModel):
        """Notifica que contrato foi renovado"""
        pass
    
    def _salvar_pdf(self, pdf_bytes: bytes, contrato_id: int) -> str:
        """Salva arquivo PDF no storage"""
        # Usar StorageService para salvar em S3 ou local
        pass
    
    def _salvar_assinatura(self, contrato_id: int, assinatura_base64: str) -> str:
        """Salva assinatura digital com validação"""
        # Validar formato
        # Salvar em storage seguro
        # Retornar path
        pass
```

---

### **FASE 2: Melhorias de UX/Interface (Prioridade ALTA)**

#### 2.2.1 Formulário de Criação de Contrato

```html
<!-- interfaces/web/templates/novo_contrato.html -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Criar Novo Contrato - CRM</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css">
    <link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
</head>
<body>
    <div class="container mt-4">
        <div class="row">
            <div class="col-lg-8 offset-lg-2">
                <div class="card shadow">
                    <div class="card-header bg-primary text-white">
                        <h4><i class="bi bi-file-text"></i> Novo Contrato</h4>
                    </div>
                    <div class="card-body">
                        <form id="contratoForm" enctype="multipart/form-data">
                            
                            <!-- Seção 1: Dados Básicos -->
                            <h5 class="mb-3"><i class="bi bi-info-circle"></i> Dados Básicos</h5>
                            
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <label for="cliente_id" class="form-label">Cliente *</label>
                                    <select id="cliente_id" name="cliente_id" class="form-control select2" required>
                                        <option value="">Selecione um cliente...</option>
                                    </select>
                                    <div class="invalid-feedback">
                                        Selecione um cliente
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <label for="tipo_contrato" class="form-label">Tipo de Contrato *</label>
                                    <select id="tipo_contrato" name="tipo_contrato" class="form-control" required>
                                        <option value="">Selecione...</option>
                                        <option value="servico">Serviço</option>
                                        <option value="assinatura">Assinatura/Plano</option>
                                        <option value="manutencao">Manutenção</option>
                                        <option value="suporte">Suporte</option>
                                        <option value="outro">Outro</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label for="titulo" class="form-label">Título do Contrato *</label>
                                <input type="text" id="titulo" name="titulo" class="form-control" 
                                       placeholder="Ex: Contrato de Serviço de Internet" required>
                            </div>
                            
                            <div class="mb-3">
                                <label for="descricao" class="form-label">Descrição</label>
                                <textarea id="descricao" name="descricao" class="form-control" 
                                          rows="4" placeholder="Descreva o contrato..."></textarea>
                            </div>
                            
                            <!-- Seção 2: Datas e Vigência -->
                            <hr>
                            <h5 class="mb-3"><i class="bi bi-calendar"></i> Vigência do Contrato</h5>
                            
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <label for="data_vigencia_inicio" class="form-label">Data de Início *</label>
                                    <input type="date" id="data_vigencia_inicio" name="data_vigencia_inicio" 
                                           class="form-control" required>
                                </div>
                                <div class="col-md-6">
                                    <label for="data_vigencia_fim" class="form-label">Data de Término *</label>
                                    <input type="date" id="data_vigencia_fim" name="data_vigencia_fim" 
                                           class="form-control" required>
                                </div>
                            </div>
                            
                            <!-- Seção 3: Informações Financeiras -->
                            <hr>
                            <h5 class="mb-3"><i class="bi bi-currency-dollar"></i> Informações Financeiras</h5>
                            
                            <div class="row mb-3">
                                <div class="col-md-8">
                                    <label for="valor_contrato" class="form-label">Valor do Contrato</label>
                                    <input type="number" id="valor_contrato" name="valor_contrato" 
                                           class="form-control" placeholder="0.00" step="0.01">
                                </div>
                                <div class="col-md-4">
                                    <label for="moeda" class="form-label">Moeda</label>
                                    <select id="moeda" name="moeda" class="form-control">
                                        <option value="BRL">R$ (Real)</option>
                                        <option value="USD">$ (Dólar)</option>
                                        <option value="EUR">€ (Euro)</option>
                                    </select>
                                </div>
                            </div>
                            
                            <!-- Seção 4: Renovação -->
                            <hr>
                            <h5 class="mb-3"><i class="bi bi-arrow-repeat"></i> Configuração de Renovação</h5>
                            
                            <div class="mb-3">
                                <label for="status_renovacao" class="form-label">Tipo de Renovação</label>
                                <select id="status_renovacao" name="status_renovacao" class="form-control">
                                    <option value="renovacao_manual">Manual (Aviso antes do vencimento)</option>
                                    <option value="renovacao_automatica">Automática (Renova automaticamente)</option>
                                    <option value="nao_renovavel">Não Renovável (Sem renovação)</option>
                                </select>
                            </div>
                            
                            <!-- Seção 5: Arquivo e Assinatura -->
                            <hr>
                            <h5 class="mb-3"><i class="bi bi-file-pdf"></i> Arquivo do Contrato</h5>
                            
                            <div class="mb-3">
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" id="incluir_pdf" 
                                           name="incluir_pdf" checked>
                                    <label class="form-check-label" for="incluir_pdf">
                                        Gerar PDF automaticamente com as informações acima
                                    </label>
                                </div>
                            </div>
                            
                            <div class="mb-3" id="upload_arquivo" style="display: none;">
                                <label for="arquivo_contrato" class="form-label">Ou Faça Upload de um Arquivo</label>
                                <input type="file" id="arquivo_contrato" name="arquivo_contrato" 
                                       class="form-control" accept=".pdf,.doc,.docx">
                                <small class="text-muted">Aceita PDF, DOC ou DOCX</small>
                            </div>
                            
                            <!-- Seção 6: Observações -->
                            <hr>
                            <h5 class="mb-3"><i class="bi bi-chat-dots"></i> Observações</h5>
                            
                            <div class="mb-3">
                                <textarea id="observacoes" name="observacoes" class="form-control" 
                                          rows="3" placeholder="Adicione notas sobre este contrato..."></textarea>
                            </div>
                            
                            <!-- Botões -->
                            <hr>
                            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                                <a href="/contratos" class="btn btn-secondary">Cancelar</a>
                                <button type="reset" class="btn btn-outline-secondary">Limpar</button>
                                <button type="submit" class="btn btn-primary">
                                    <i class="bi bi-save"></i> Criar Contrato
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal de Carregamento -->
    <div class="modal fade" id="loadingModal" tabindex="-1" data-bs-backdrop="static">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-body text-center">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Carregando...</span>
                    </div>
                    <p class="mt-3">Criando contrato e gerando PDF...</p>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>
    
    <script>
        // Inicializar Select2
        $(document).ready(function() {
            $('#cliente_id').select2({
                placeholder: 'Buscar cliente...',
                ajax: {
                    url: '/api/v1/clientes/search',
                    dataType: 'json',
                    delay: 250,
                    data: function(params) {
                        return {
                            q: params.term
                        };
                    },
                    processResults: function(data) {
                        return {
                            results: data.map(cliente => ({
                                id: cliente.id,
                                text: cliente.nome_fantasia || cliente.razao_social
                            }))
                        };
                    }
                }
            });
            
            // Toggle arquivo upload
            document.getElementById('incluir_pdf').addEventListener('change', function() {
                document.getElementById('upload_arquivo').style.display = 
                    this.checked ? 'none' : 'block';
            });
            
            // Validação de datas
            document.getElementById('data_vigencia_inicio').addEventListener('change', function() {
                const dataFim = document.getElementById('data_vigencia_fim');
                dataFim.min = this.value;
            });
            
            // Submeter formulário
            document.getElementById('contratoForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                if (!this.checkValidity()) {
                    this.classList.add('was-validated');
                    return;
                }
                
                const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
                modal.show();
                
                const formData = new FormData(this);
                
                try {
                    const response = await fetch('/api/v1/contratos', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (response.ok) {
                        const contrato = await response.json();
                        alert('Contrato criado com sucesso!');
                        window.location.href = `/contratos/${contrato.id}`;
                    } else {
                        const error = await response.json();
                        alert('Erro: ' + error.message);
                    }
                } catch (error) {
                    alert('Erro ao criar contrato: ' + error.message);
                } finally {
                    modal.hide();
                }
            });
        });
    </script>
</body>
</html>
```

#### 2.2.2 Página de Detalhes do Contrato

```html
<!-- interfaces/web/templates/detalhes_contrato.html -->
<!-- Mostra todos os dados do contrato, histórico, assinatura, etc -->
```

---

### **FASE 3: Dashboard e Relatórios (Prioridade MÉDIA)**

#### 2.3.1 Dashboard de Contratos

```python
# crm_modules/contratos/dashboard_service.py
class ContratosDashboardService:
    def obter_metricas_gerais(self) -> dict:
        """Métricas principais de contratos"""
        return {
            'total_contratos': self.contar_total(),
            'contratos_ativos': self.contar_por_status(StatusAssinatura.LIBERADO),
            'aguardando_assinatura': self.contar_por_status(StatusAssinatura.AGUARDANDO),
            'valor_total': self.somar_valor_contratos(),
            'vencendo_30_dias': self.contar_vencendo(30),
            'vencidos': self.contar_vencidos()
        }
    
    def obter_contratos_por_status(self) -> dict:
        """Gráfico de distribuição por status"""
        pass
    
    def obter_receita_por_mes(self) -> dict:
        """Receita mensal baseada em contratos"""
        pass
    
    def obter_clientes_sem_contrato(self) -> list:
        """Clientes que não têm contrato"""
        pass
    
    def obter_contratos_para_renovar(self) -> list:
        """Contratos que vencem nos próximos 30 dias"""
        pass
```

---

### **FASE 4: Integrações e Automações (Prioridade MÉDIA)**

#### 2.4.1 Assinatura Digital Real

```python
# crm_modules/contratos/assinatura_service.py
# Integração com serviços como DocuSign, Clicksign, etc
```

#### 2.4.2 Notificações por Email

```python
# crm_modules/contratos/email_service.py
# Templates de email para cada estado do contrato
```

#### 2.4.3 Agendador de Tarefas

```python
# crm_modules/contratos/scheduler.py
# Verificação diária de contratos vencendo
# Renovação automática
# Notificações
```

---

## 3. CHECKLIST DE IMPLEMENTAÇÃO

### Prioridade 1 (Fazer AGORA):
- [ ] Expandir modelo ContratoModel com novos campos
- [ ] Criar tabela ContratoHistoricoModel
- [ ] Implementar gerador de PDF
- [ ] Melhorar service com auditoria
- [ ] Criar formulário de novo contrato
- [ ] Criar página de detalhes
- [ ] Adicionar validações e tratamento de erros

### Prioridade 2 (Próximas semanas):
- [ ] Implementar dashboard
- [ ] Adicionar filtros e busca avançada
- [ ] Criar relatórios exportáveis
- [ ] Bulk actions
- [ ] Notificações por email

### Prioridade 3 (Futuro):
- [ ] Integração com assinatura digital real (DocuSign)
- [ ] Renovação automática com integração de pagamento
- [ ] Versioning de templates
- [ ] Análises preditivas

---

## 4. RESUMO EXECUTIVO

**Status Atual:** MVP básico (apenas CRUD com assinatura mockada)

**Principais Deficiências:**
1. Sem geração de PDF ❌
2. Sem auditoria de alterações ❌
3. Sem assinatura digital real ❌
4. Sem notificações ❌
5. Sem renovação automática ❌
6. Interface incompleta ❌
7. Sem integração com negócio (planos/produtos) ❌

**Para Profissionalizar:**
- Implementar PDF com ReportLab (1-2 dias)
- Adicionar sistema de auditoria (1 dia)
- Melhorar UI com formulários (2-3 dias)
- Implementar notificações (2 dias)
- Adicionar dashboard (2 dias)
- **Total estimado: ~10 dias de desenvolvimento**

**ROI:**
- Redução de erros administrativos
- Rastreabilidade completa
- Melhor experiência do cliente
- Cumprimento de conformidade legal
- Automação de processos

