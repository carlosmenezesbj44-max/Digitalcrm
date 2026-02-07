# Implementação: Carnês e Boletos com Gerencianet

## 📋 Resumo

Sistema completo para criar **carnês** (planos de pagamento parcelado) e **boletos** integrado com a gateway Gerencianet.

### ✨ Funcionalidades

- ✅ **Carnês**: Parcelar pagamentos em 2 a 360 parcelas
- ✅ **Boletos**: Gerar boletos para faturas ou pagamentos avulsos
- ✅ **Integração Gerencianet**: Automação de boletos e recorrências
- ✅ **Webhooks**: Notificações automáticas de pagamentos
- ✅ **Sincronização**: Manter status de boletos sincronizado
- ✅ **Relatórios**: Listar boletos pendentes/vencidos

---

## 🚀 Instalação Rápida

### 1️⃣ Adicionar ao `.env`

```env
# Gerencianet
GERENCIANET_CLIENT_ID=seu_client_id
GERENCIANET_CLIENT_SECRET=seu_client_secret
GERENCIANET_SANDBOX=true

APP_URL=http://localhost:8000
```

### 2️⃣ Instalar Dependências

```bash
pip install requests
```

### 3️⃣ Executar Migrations

```bash
# Criar tabelas
alembic upgrade head
```

Ou manualmente:
```python
python create_tables.py
```

### 4️⃣ Registrar API no app

Adicione ao seu `main.py` ou arquivo de rotas:

```python
from crm_modules.faturamento.carne_api import router as carne_router

app.include_router(carne_router)
```

---

## 📁 Arquivos Criados

```
crm_modules/faturamento/
├── carne_models.py           # Modelos: Carnê, Parcela, Boleto
├── carne_schemas.py          # Schemas Pydantic
├── carne_service.py          # Lógica de negócio para carnês
├── boleto_service.py         # Lógica de negócio para boletos
├── gerencianet_client.py     # Cliente da API Gerencianet
├── carne_api.py              # Endpoints REST

docs/
├── INTEGRACAO_GERENCIANET.md # Documentação completa
├── IMPLEMENTACAO_CARNES_BOLETOS.md # Este arquivo

scripts/
├── exemplo_carne_boleto.py   # Exemplos de uso
```

---

## 🔧 Configuração Gerencianet

### Passo 1: Criar Conta

1. Acesse [gerencianet.com.br](https://gerencianet.com.br)
2. Crie uma conta
3. Faça login no painel

### Passo 2: Obter Credenciais

1. Vá em **Aplicações** → **Minhas Aplicações**
2. Crie uma nova aplicação
3. Copie:
   - `Client ID`
   - `Client Secret`

### Passo 3: Configurar Webhooks

1. Acesse **Configurações** → **Webhooks**
2. Adicione as URLs:
   ```
   POST http://seu-app.com/api/faturamento/webhooks/gerencianet/boleto
   POST http://seu-app.com/api/faturamento/webhooks/gerencianet/subscription
   ```
3. Ative notificações para:
   - Payment success
   - Payment failure
   - Charge overdue

---

## 💡 Exemplos de Uso

### Exemplo 1: Criar um Carnê

```python
from datetime import date
from crm_modules.faturamento.carne_schemas import CarneCreate

# Cliente quer pagar R$ 1.200 em 12 parcelas
carne_data = CarneCreate(
    cliente_id=123,
    valor_total=1200.00,
    quantidade_parcelas=12,
    data_inicio=date(2024, 1, 1),
    data_primeiro_vencimento=date(2024, 2, 1),
    intervalo_dias=30,
    descricao="Serviços de consultoria",
    gerar_boletos=True  # Gera boletos automaticamente
)

# Via API
POST /api/faturamento/carnes
Content-Type: application/json

{
    "cliente_id": 123,
    "valor_total": 1200.00,
    "quantidade_parcelas": 12,
    "data_inicio": "2024-01-01",
    "data_primeiro_vencimento": "2024-02-01",
    "intervalo_dias": 30,
    "descricao": "Serviços de consultoria",
    "gerar_boletos": true
}

# Response
{
    "id": 1,
    "numero_carne": "CARNE-20240101-0123-001",
    "valor_total": 1200.00,
    "quantidade_parcelas": 12,
    "valor_parcela": 100.00,
    "status": "ativo",
    "parcelas": [
        {
            "id": 1,
            "numero_parcela": 1,
            "valor": 100.00,
            "data_vencimento": "2024-02-01",
            "status": "pendente",
            "codigo_barras": "12345.67890...",
            "linha_digitavel": "12345.67890..."
        },
        ...
    ]
}
```

### Exemplo 2: Gerar Boleto para Fatura

```python
# POST /api/faturamento/faturas/{fatura_id}/boleto
POST /api/faturamento/faturas/42/boleto?juros_dia=0.05&multa_atraso=2.0

# Response
{
    "id": 1,
    "numero_boleto": "BOL-20240101-0123-0001",
    "valor": 1500.00,
    "data_vencimento": "2024-02-15",
    "status": "pendente",
    "codigo_barras": "12345.67890 12345.678901...",
    "linha_digitavel": "12345.67890 12345.678901...",
    "url_boleto": "https://gerencianet.com.br/boleto/...",
    "gerencianet_status": "aberto"
}
```

### Exemplo 3: Listar Parcelas

```python
GET /api/faturamento/carnes/1/parcelas

# Response
[
    {
        "id": 1,
        "numero": 1,
        "valor": 100.00,
        "data_vencimento": "2024-02-01",
        "status": "pendente",
        "valor_pago": 0.0,
        "codigo_barras": "...",
        "link_boleto": "https://..."
    },
    ...
]
```

### Exemplo 4: Registrar Pagamento

```python
POST /api/faturamento/parcelas/1/pagar?valor_pago=100.0

# Response
{
    "message": "Pagamento registrado com sucesso"
}
```

### Exemplo 5: Sincronizar com Gerencianet

```python
# Sincronizar um boleto
PUT /api/faturamento/boletos/1/sincronizar

# Ou sincronizar todos
POST /api/faturamento/boletos/sincronizar/todos

# Response
{
    "message": "15 boletos sincronizados",
    "boletos_sincronizados": 15
}
```

### Exemplo 6: Cancelar Carnê

```python
DELETE /api/faturamento/carnes/1/cancelar

# Response
{
    "id": 1,
    "numero_carne": "CARNE-20240101-0123-001",
    "status": "cancelado",
    ...
}
```

---

## 📊 Estrutura de Dados

### Tabela: CARNES
```sql
CREATE TABLE carnes (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    numero_carne VARCHAR UNIQUE,
    valor_total FLOAT,
    quantidade_parcelas INTEGER,
    valor_parcela FLOAT,
    data_inicio DATE,
    data_primeiro_vencimento DATE,
    intervalo_dias INTEGER DEFAULT 30,
    descricao TEXT,
    status VARCHAR DEFAULT 'ativo',
    gerencianet_subscription_id VARCHAR,
    ativo BOOLEAN DEFAULT true,
    data_criacao DATETIME,
    data_atualizacao DATETIME
);
```

### Tabela: PARCELAS
```sql
CREATE TABLE parcelas (
    id INTEGER PRIMARY KEY,
    carne_id INTEGER NOT NULL,
    numero_parcela INTEGER,
    valor FLOAT,
    data_vencimento DATE,
    status VARCHAR DEFAULT 'pendente',
    valor_pago FLOAT DEFAULT 0.0,
    data_pagamento DATETIME,
    gerencianet_charge_id VARCHAR,
    gerencianet_link_boleto VARCHAR,
    codigo_barras VARCHAR,
    linha_digitavel VARCHAR,
    ativo BOOLEAN DEFAULT true,
    FOREIGN KEY (carne_id) REFERENCES carnes(id)
);
```

### Tabela: BOLETOS
```sql
CREATE TABLE boletos (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    fatura_id INTEGER,
    parcela_id INTEGER,
    numero_boleto VARCHAR UNIQUE,
    valor FLOAT,
    data_vencimento DATE,
    data_emissao DATETIME,
    codigo_barras VARCHAR,
    linha_digitavel VARCHAR,
    url_boleto VARCHAR,
    gerencianet_charge_id VARCHAR UNIQUE,
    gerencianet_status VARCHAR DEFAULT 'aberto',
    status VARCHAR DEFAULT 'pendente',
    ativo BOOLEAN DEFAULT true,
    data_criacao DATETIME,
    data_atualizacao DATETIME
);
```

---

## 🔌 Webhooks

### Webhook de Boleto

Gerencianet notificará sua aplicação em:
```
POST /api/faturamento/webhooks/gerencianet/boleto
```

**Payload recebido**:
```json
{
    "id": 12345,
    "status": "paid",
    "amount": 100000,
    "paid_at": "2024-01-15T10:30:00Z"
}
```

**Status possíveis**:
- `paid` - Boleto pago
- `canceled` - Boleto cancelado
- `overdue` - Boleto vencido
- `pending` - Boleto pendente

---

## 📈 Fluxo Completo

```
Cliente solicita parcelamento
        ↓
  Cria Carnê (12x)
        ↓
Sistema cria Parcelas (24 registros)
        ↓
Para cada Parcela → Gera Boleto no Gerencianet
        ↓
Armazena dados do boleto (código de barras, link, etc)
        ↓
Cliente baixa boleto e paga no banco
        ↓
Gerencianet confirma pagamento
        ↓
Webhook atualiza status da parcela
        ↓
Se todas pagas → Carnê marcado como "finalizado"
```

---

## ⚙️ Configurações Avançadas

### Juros e Multa

```python
# Gerar boleto com juros e multa por atraso
POST /api/faturamento/boletos

{
    "cliente_id": 123,
    "valor": 500.00,
    "data_vencimento": "2024-02-20",
    "juros_dia": 0.05,      # 0.05% ao dia
    "multa_atraso": 2.0      # 2% de multa
}
```

### Sincronização Automática

```python
# Criar task agendada para sincronizar todos os dias
from celery import shared_task

@shared_task
def sincronizar_boletos_diario():
    db = SessionLocal()
    service = BoletoService(session=db)
    service.sincronizar_pagamentos_gerencianet()
    db.close()

# No beat schedule:
{
    'sincronizar-boletos': {
        'task': 'app.tasks.sincronizar_boletos_diario',
        'schedule': crontab(hour=0, minute=0)  # Todo dia à meia-noite
    }
}
```

---

## 🛡️ Segurança

✅ **Implementar**:
1. Validação de webhooks do Gerencianet
2. Rate limiting nas APIs
3. Criptografia de dados sensíveis
4. Audit log de transações
5. HTTPS em produção

**Exemplo - Validar webhook**:
```python
def validar_webhook_gerencianet(signature: str, body: str) -> bool:
    """Valida assinatura do webhook"""
    secret = os.getenv("GERENCIANET_WEBHOOK_SECRET")
    expected_signature = hmac.new(
        secret.encode(),
        body.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature == expected_signature
```

---

## 🧪 Testes

### Testar no Sandbox

Use `GERENCIANET_SANDBOX=true` no `.env`

**Dados de teste**:
- CPF: `94087216055`
- Email: `teste@sandboxgerencianet.com.br`

### Script de Teste

```bash
python exemplo_carne_boleto.py
```

Selecione opção 9 para executar todos os exemplos.

---

## 📱 API REST - Endpoints

### Carnês

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/faturamento/carnes` | Criar carnê |
| GET | `/api/faturamento/carnes/{id}` | Obter carnê |
| GET | `/api/faturamento/carnes/cliente/{cliente_id}` | Listar carnês cliente |
| PUT | `/api/faturamento/carnes/{id}` | Atualizar carnê |
| DELETE | `/api/faturamento/carnes/{id}/cancelar` | Cancelar carnê |
| GET | `/api/faturamento/carnes/{id}/parcelas` | Listar parcelas |
| POST | `/api/faturamento/parcelas/{id}/pagar` | Registrar pagamento |

### Boletos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/faturamento/boletos` | Criar boleto direto |
| POST | `/api/faturamento/faturas/{id}/boleto` | Gerar boleto para fatura |
| GET | `/api/faturamento/boletos/{id}` | Obter boleto |
| GET | `/api/faturamento/boletos/cliente/{cliente_id}` | Listar boletos cliente |
| GET | `/api/faturamento/boletos/vencidos/listar` | Listar vencidos |
| PUT | `/api/faturamento/boletos/{id}/cancelar` | Cancelar boleto |
| PUT | `/api/faturamento/boletos/{id}/sincronizar` | Sincronizar com Gerencianet |
| POST | `/api/faturamento/boletos/sincronizar/todos` | Sincronizar todos |

---

## 🐛 Troubleshooting

| Problema | Causa | Solução |
|----------|-------|--------|
| `Invalid credentials` | Client ID/Secret incorretos | Verifique no painel Gerencianet |
| `Customer not found` | Dados do cliente incompletos | Ensure email e CPF preenchidos |
| `Webhook timeout` | URL não acessível | Configure `APP_URL` corretamente |
| `Duplicate reference` | Número duplicado | Use números únicos para referências |
| `Boleto não gera` | Cliente sem email | Adicionar email no cadastro do cliente |

---

## 📚 Próximos Passos

1. **Email**: Enviar boleto por email ao cliente
2. **Dashboard**: Criar visualização de carnês e boletos
3. **Relatórios**: Gerar relatórios de recebimento
4. **Multiple Gateways**: Adicionar suporte a mais gateways (PagSeguro, Wise, etc)
5. **PIX**: Integrar pagamentos via PIX
6. **Cartão**: Suporte a parcelamento em cartão de crédito

---

## 📖 Documentação

- [INTEGRACAO_GERENCIANET.md](./INTEGRACAO_GERENCIANET.md) - Documentação detalhada
- [API Gerencianet](https://gerencianet.com.br/api) - Documentação oficial
- [exemplo_carne_boleto.py](./exemplo_carne_boleto.py) - Exemplos de código

---

## ✅ Checklist de Implementação

- [ ] Adicionar credenciais Gerencianet ao `.env`
- [ ] Instalar dependência `requests`
- [ ] Executar migrations para criar tabelas
- [ ] Incluir router no `main.py`
- [ ] Configurar webhooks no painel Gerencianet
- [ ] Testar criação de carnê
- [ ] Testar geração de boleto
- [ ] Testar sincronização
- [ ] Implementar envio de email com boleto
- [ ] Criar dashboard de controle

---

**Pronto para começar?** Siga a [Instalação Rápida](#-instalação-rápida) acima!
