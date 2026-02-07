# 🗺️ Roadmap de Implementação - CRM Completo

## Fase 1: AUTENTICAÇÃO E SEGURANÇA (Semana 1-2)

### 1.1 Sistema de Login Completo
```
crm_modules/usuarios/
├── models.py          # User, Role, Permission
├── schemas.py         # UserCreate, UserLogin, UserResponse
├── service.py         # UserService com autenticação
├── repository.py      # UserRepository
└── api.py            # /login, /logout, /register

interfaces/web/
├── templates/
│   ├── login.html      # Formulário de login
│   ├── register.html   # Registro de novo usuário
│   ├── perfil.html     # Editar perfil
│   └── recuperar_senha.html
└── app.py             # Rotas de autenticação
```

### 1.2 Controle de Acesso (RBAC)
```python
# crm_modules/usuarios/models.py
class User(Base):
    id: int
    username: str (unique)
    email: str (unique)
    password_hash: str
    is_active: bool
    role_id: int (FK)
    created_at: datetime
    last_login: datetime

class Role(Base):
    id: int
    name: str  # admin, gerente, tecnico, cliente
    permissions: List[Permission]

class Permission(Base):
    id: int
    name: str  # read_clientes, create_faturas, etc
    module: str

class UserAuditLog(Base):
    id: int
    user_id: int
    action: str
    resource: str
    timestamp: datetime
    ip_address: str
```

### 1.3 Middleware de Autenticação
```python
# Adicionar em app.py
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from fastapi import HTTPException, Depends

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthCredentials = Depends(security)):
    # Validar JWT
    # Retornar usuário
    pass

# Usar em rotas:
@app.get("/clientes")
def listar_clientes(current_user: User = Depends(verify_token)):
    # Apenas usuarios autenticados
    pass
```

**Estimativa**: 3-5 dias

---

## Fase 2: DASHBOARD EXECUTIVO (Semana 2-3)

### 2.1 Model de KPIs
```python
# crm_modules/relatorios/models.py
class DashboardKPI(Base):
    data: date
    clientes_ativos: int
    clientes_inativos: int
    receita_total: float
    receita_mes: float
    ordens_pendentes: int
    ordens_concluidas: int
    tickets_abertos: int
    churn_rate: float
```

### 2.2 Service de Cálculo
```python
# crm_modules/relatorios/service.py
class DashboardService:
    def obter_kpis_atuais(self):
        # Retorna KPIs do mês
        return {
            "clientes_ativos": ...,
            "receita_mes": ...,
            "ordens_pendentes": ...,
            "tickets_abertos": ...,
            "churn": ...
        }
    
    def obter_grafico_crescimento(self, meses=12):
        # Retorna dados para gráfico
        pass
    
    def obter_alertas(self):
        # Clientes para vencer, faturas vencidas, etc
        pass
```

### 2.3 Template HTML
```html
<!-- interfaces/web/templates/dashboard.html -->
<div class="dashboard-grid">
    <div class="kpi-card">
        <h3>Clientes Ativos</h3>
        <p class="value">{{ kpis.clientes_ativos }}</p>
        <p class="change">↑ 5% vs mês anterior</p>
    </div>
    
    <div class="kpi-card">
        <h3>Receita Mês</h3>
        <p class="value">R$ {{ kpis.receita_mes }}</p>
        <p class="change">↑ 12% vs mês anterior</p>
    </div>
    
    <!-- Gráficos -->
    <div class="chart-container">
        <canvas id="crescimentoChart"></canvas>
    </div>
    
    <!-- Alertas -->
    <div class="alerts">
        <div class="alert alert-warning">
            {{ alerts.count_vencer }} contratos vencem nos próximos 7 dias
        </div>
    </div>
</div>
```

**Estimativa**: 3-4 dias

---

## Fase 3: FATURAMENTO E INVOICES (Semana 3-5)

### 3.1 Modelos de Dados
```python
# crm_modules/faturamento/models.py
class Ciclo(Base):
    id: int
    nome: str  # "Mensal", "Bimestral"
    dias: int  # 30, 60
    ativo: bool

class Invoice(Base):
    id: int
    numero: str  # Número sequencial
    cliente_id: int (FK)
    data_emissao: date
    data_vencimento: date
    data_pagamento: date (nullable)
    valor_total: float
    valor_pago: float
    status: str  # draft, emitida, paga, vencida, cancelada
    observacoes: str
    created_at: datetime
    updated_at: datetime

class ItemInvoice(Base):
    id: int
    invoice_id: int (FK)
    descricao: str
    quantidade: float
    valor_unitario: float
    valor_total: float
    tipo: str  # plano, produto, serviço

class Pagamento(Base):
    id: int
    invoice_id: int (FK)
    data_pagamento: date
    valor: float
    metodo: str  # boleto, pix, cartao, transferencia
    numero_referencia: str  # ID da transação
    status: str  # pendente, confirmado, falha
    
class CicloFaturamento(Base):
    id: int
    cliente_id: int (FK)
    ciclo_id: int (FK)
    data_inicio: date
    proximo_vencimento: date
    ativo: bool
```

### 3.2 Service de Faturamento
```python
# crm_modules/faturamento/service.py
class FaturamentoService:
    def gerar_invoice(self, cliente_id: int, itens: List):
        """Gera nova fatura para cliente"""
        # Calcula valores
        # Cria invoice
        # Cria itens
        # Envia email
        pass
    
    def gerar_invoices_automaticas(self):
        """Chamado por job agendado (Celery)"""
        # Encontra clientes com ciclo para hoje
        # Gera invoices para cada um
        pass
    
    def registrar_pagamento(self, invoice_id: int, valor: float, metodo: str):
        """Registra pagamento recebido"""
        # Atualiza invoice
        # Ativa cliente se estava bloqueado
        pass
    
    def enviar_lembrete_pagamento(self, dias_antes=3):
        """Envia email 3 dias antes do vencimento"""
        pass
    
    def bloquear_clientes_vencidos(self, dias_atraso=10):
        """Bloqueia clientes com atraso"""
        # Atualiza status de cliente
        # Chama BloqueioService
        pass
```

### 3.3 Templates
```html
<!-- interfaces/web/templates/faturamento/invoices.html -->
<table class="invoice-table">
    <thead>
        <tr>
            <th>Número</th>
            <th>Cliente</th>
            <th>Emissão</th>
            <th>Vencimento</th>
            <th>Valor</th>
            <th>Status</th>
            <th>Ações</th>
        </tr>
    </thead>
    <tbody>
        {% for invoice in invoices %}
        <tr class="status-{{ invoice.status }}">
            <td>{{ invoice.numero }}</td>
            <td>{{ invoice.cliente.nome }}</td>
            <td>{{ invoice.data_emissao }}</td>
            <td>{{ invoice.data_vencimento }}</td>
            <td>R$ {{ invoice.valor_total }}</td>
            <td><span class="badge">{{ invoice.status }}</span></td>
            <td>
                <a href="/faturamento/{{ invoice.id }}" class="btn btn-sm">Ver</a>
                <a href="/faturamento/{{ invoice.id }}/pdf" class="btn btn-sm">PDF</a>
                <button onclick="registrarPagamento({{ invoice.id }})" class="btn btn-sm">Pagar</button>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

### 3.4 Job Agendado (Celery)
```python
# tasks/jobs/faturamento.py
from celery import shared_task

@shared_task
def gerar_invoices_diarias():
    """Executado todo dia às 00:00"""
    faturamento_service = FaturamentoService()
    faturamento_service.gerar_invoices_automaticas()

@shared_task
def enviar_lembretes_pagamento():
    """Executado todo dia às 09:00"""
    faturamento_service = FaturamentoService()
    faturamento_service.enviar_lembrete_pagamento(dias_antes=3)

@shared_task
def bloquear_clientes_vencidos():
    """Executado todo dia às 22:00"""
    faturamento_service = FaturamentoService()
    faturamento_service.bloquear_clientes_vencidos(dias_atraso=10)
```

**Estimativa**: 5-7 dias

---

## Fase 4: CONTRATOS (Semana 5-7)

### 4.1 Modelos
```python
# crm_modules/contratos/models.py
class Contrato(Base):
    id: int
    numero: str
    cliente_id: int (FK)
    data_inicio: date
    data_fim: date (nullable - indefinido)
    data_renovacao: date
    plano_id: int (FK)
    preco: float
    termo: str  # texto do contrato
    status: str  # ativo, vencido, cancelado, suspenso
    renovacao_automatica: bool
    created_at: datetime
    updated_at: datetime

class ContratoHistorico(Base):
    id: int
    contrato_id: int (FK)
    versao: int
    termo: str
    data_criacao: date
```

### 4.2 Service
```python
# crm_modules/contratos/service.py
class ContratoService:
    def criar_contrato(self, cliente_id: int, plano_id: int, termo_template: str):
        """Cria novo contrato baseado em template"""
        # Substitui placeholders
        # Cria contrato
        # Envia para assinatura (integração com docusign/signaturepad)
        pass
    
    def renovar_contrato(self, contrato_id: int):
        """Renova contrato existente"""
        pass
    
    def notificar_vencimento(self):
        """Chamado por job - envia email 30 dias antes"""
        pass
```

**Estimativa**: 3-4 dias

---

## Fase 5: TICKETS DE SUPORTE (Semana 7-9)

### 5.1 Modelos
```python
# crm_modules/tickets/models.py
class Ticket(Base):
    id: int
    numero: str
    cliente_id: int (FK)
    titulo: str
    descricao: str
    prioridade: str  # baixa, media, alta, critica
    status: str  # aberto, em_andamento, fechado, reabert
    categoria: str
    tecnico_atribuido_id: int (FK User)
    data_criacao: datetime
    data_atualizacao: datetime
    data_fechamento: datetime
    tempo_resolucao_minutos: int
    
class ComentarioTicket(Base):
    id: int
    ticket_id: int (FK)
    usuario_id: int (FK)
    tipo: str  # cliente, tecnico, sistema
    texto: str
    anexos: List[str]
    data_criacao: datetime

class SLA(Base):
    id: int
    prioridade: str
    tempo_resposta_horas: int
    tempo_resolucao_horas: int
    horario_inicio: time
    horario_fim: time
```

### 5.2 Service
```python
# crm_modules/tickets/service.py
class TicketService:
    def criar_ticket(self, cliente_id: int, titulo: str, descricao: str):
        # Cria ticket
        # Atribui prioritáde
        # Notifica técnicos
        pass
    
    def atribuir_tecnico(self, ticket_id: int, tecnico_id: int):
        # Atribui a técnico
        # Envia notificação
        pass
    
    def adicionar_comentario(self, ticket_id: int, usuario_id: int, texto: str):
        # Adiciona comentário
        # Notifica envolvidos
        pass
    
    def fechar_ticket(self, ticket_id: int):
        # Fecha ticket
        # Calcula SLA
        # Envia notificação
        pass
    
    def alertar_sla_vencido(self):
        # Job: verifica SLAs
        pass
```

**Estimativa**: 4-5 dias

---

## Fase 6: RELATÓRIOS E ANALYTICS (Semana 9-12)

### 6.1 Service de Relatórios
```python
# crm_modules/relatorios/service.py
class RelatorioService:
    def relatorio_clientes(self, filtros: dict):
        # Retorna dados de clientes com filtros
        pass
    
    def relatorio_faturamento(self, data_inicio, data_fim):
        # Receita, invoices, pagamentos
        pass
    
    def relatorio_churn(self, meses=12):
        # Taxa de cancelamento
        pass
    
    def relatorio_performance_tecnicos(self):
        # Tickets resolvidos, tempo médio
        pass
    
    def exportar_pdf(self, relatorio_id: int):
        # Gera PDF
        pass
    
    def exportar_excel(self, relatorio_id: int):
        # Gera Excel
        pass
```

### 6.2 Agendamento de Relatórios
```python
# crm_modules/relatorios/models.py
class RelatorioAgendado(Base):
    id: int
    nome: str
    tipo: str  # clientes, faturamento, churn
    frequencia: str  # diario, semanal, mensal
    destinatarios: List[str]  # emails
    proximo_envio: datetime
    ativo: bool
```

**Estimativa**: 4-5 dias

---

## Fase 7: PORTAL DO CLIENTE (Semana 12-15)

### 7.1 Interface Self-Service
```html
<!-- interfaces/web/templates/portal_cliente.html -->
- Dashboard pessoal (dados de uso)
- Faturas (visualizar, baixar, pagar)
- Tickets (abrir, acompanhar)
- Mudança de plano
- Alteração de dados pessoais
- Histórico de conexão
```

### 7.2 Service de Cliente
```python
# crm_modules/clientes/portal_service.py
class PortalClienteService:
    def obter_dados_cliente(self, cliente_id: int):
        # Dados pessoais, plano, histórico
        pass
    
    def obter_faturas(self, cliente_id: int):
        # Faturas do cliente
        pass
    
    def processar_pagamento(self, invoice_id: int, metodo: str):
        # Integra com gateway de pagamento
        pass
    
    def solicitar_mudanca_plano(self, cliente_id: int, novo_plano_id: int):
        # Cria solicitação
        # Notifica gerente
        pass
```

**Estimativa**: 4-5 dias

---

## Implementação de Integrações de Pagamento

### Estrutura
```python
# crm_modules/pagamentos/
├── models.py
├── service.py
├── gateway_stripe.py
├── gateway_mercadopago.py
├── gateway_pix.py
└── gateway_boleto.py
```

### Base
```python
# crm_modules/pagamentos/gateway_base.py
from abc import ABC, abstractmethod

class GatewayPagamento(ABC):
    @abstractmethod
    def criar_cobranca(self, invoice_id: int, cliente: dict, valor: float):
        pass
    
    @abstractmethod
    def processar_webhook(self, payload: dict):
        pass
    
    @abstractmethod
    def obter_status(self, transacao_id: str):
        pass
```

### Stripe
```python
# crm_modules/pagamentos/gateway_stripe.py
import stripe

class GatewayStripe(GatewayPagamento):
    def criar_cobranca(self, invoice_id, cliente, valor):
        # Cria checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'brl',
                    'product_data': {'name': f'Invoice #{invoice_id}'},
                    'unit_amount': int(valor * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://example.com/sucesso',
            cancel_url='https://example.com/cancelado',
        )
        return session
```

**Estimativa**: 3-4 dias

---

## Estrutura de Pastas Final

```
crm_provedor/
├── crm_core/
│   ├── config/
│   ├── db/
│   ├── security/
│   │   ├── auth.py          # JWT, login
│   │   └── acl.py           # RBAC
│   ├── cache/
│   ├── events/
│   └── utils/
│
├── crm_modules/
│   ├── usuarios/             # ✅ NOVO
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   ├── repository.py
│   │   └── api.py
│   │
│   ├── clientes/
│   │   ├── portal_service.py # ✅ NOVO
│   │   └── ...
│   │
│   ├── faturamento/          # ✅ COMPLETO
│   │   ├── models.py
│   │   ├── service.py
│   │   ├── schemas.py
│   │   └── repository.py
│   │
│   ├── pagamentos/           # ✅ NOVO
│   │   ├── models.py
│   │   ├── gateway_base.py
│   │   ├── gateway_stripe.py
│   │   ├── gateway_mercadopago.py
│   │   └── service.py
│   │
│   ├── contratos/            # ✅ COMPLETO
│   │   ├── models.py
│   │   ├── service.py
│   │   └── templates.py
│   │
│   ├── tickets/              # ✅ COMPLETO
│   │   ├── models.py
│   │   ├── service.py
│   │   └── sla.py
│   │
│   ├── relatorios/           # ✅ COMPLETO
│   │   ├── models.py
│   │   ├── service.py
│   │   ├── exporters.py
│   │   └── agendador.py
│   │
│   └── ...
│
├── interfaces/
│   └── web/
│       ├── templates/
│       │   ├── login.html              # ✅ NOVO
│       │   ├── dashboard.html          # ✅ NOVO
│       │   ├── faturamento.html        # ✅ NOVO
│       │   ├── contratos.html          # ✅ NOVO
│       │   ├── tickets.html            # ✅ NOVO
│       │   ├── relatorios.html         # ✅ NOVO
│       │   └── portal_cliente.html     # ✅ NOVO
│       └── app.py
│
├── tasks/
│   └── jobs/
│       ├── faturamento.py              # ✅ NOVO
│       ├── tickets.py                  # ✅ NOVO
│       ├── relatorios.py               # ✅ NOVO
│       └── ...
│
└── tests/
    ├── test_usuarios.py                # ✅ NOVO
    ├── test_faturamento.py             # ✅ NOVO
    └── ...
```

---

## Timeline Recomendado

| Fase | Período | Esforço | Prioridade |
|------|---------|---------|-----------|
| Autenticação | Semana 1-2 | 40h | CRÍTICA |
| Dashboard | Semana 2-3 | 30h | ALTA |
| Faturamento | Semana 3-5 | 60h | CRÍTICA |
| Contratos | Semana 5-7 | 40h | ALTA |
| Tickets | Semana 7-9 | 50h | MÉDIA |
| Relatórios | Semana 9-12 | 50h | MÉDIA |
| Portal Cliente | Semana 12-15 | 60h | MÉDIA |

**Total: ~330 horas (~6-8 semanas com 1 dev)**

---

**Documento criado**: Jan 2025
