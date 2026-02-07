# 🚀 Quick Reference - Carnês e Boletos

**Saiba em 2 minutos como usar o novo sistema.**

---

## ⚡ Setup Rápido (5 minutos)

```bash
# 1. Copiar config
cp .env.gerencianet.example .env

# 2. Preencher credenciais (no .env)
# GERENCIANET_CLIENT_ID=seu_id
# GERENCIANET_CLIENT_SECRET=seu_secret

# 3. Criar tabelas
alembic upgrade head

# 4. No main.py, add:
from crm_modules.faturamento.carne_api import router
app.include_router(router)

# 5. Rodar!
python main.py
```

---

## 📚 Endpoints Principais

### Carnês

```bash
# Criar carnê (12x de R$ 100)
POST /api/faturamento/carnes
{
    "cliente_id": 123,
    "valor_total": 1200.00,
    "quantidade_parcelas": 12,
    "data_primeiro_vencimento": "2024-02-01",
    "gerar_boletos": true
}

# Listar parcelas
GET /api/faturamento/carnes/1/parcelas

# Registrar pagamento
POST /api/faturamento/parcelas/1/pagar?valor_pago=100.0

# Cancelar carnê
DELETE /api/faturamento/carnes/1/cancelar
```

### Boletos

```bash
# Boleto para fatura
POST /api/faturamento/faturas/42/boleto

# Boleto direto
POST /api/faturamento/boletos
{
    "cliente_id": 123,
    "valor": 500.00,
    "data_vencimento": "2024-02-20"
}

# Listar vencidos
GET /api/faturamento/boletos/vencidos/listar

# Sincronizar todos
POST /api/faturamento/boletos/sincronizar/todos
```

---

## 🐍 Código Python

### Criar Carnê

```python
from crm_modules.faturamento.carne_service import CarneService
from crm_modules.faturamento.carne_schemas import CarneCreate
from datetime import date

db = SessionLocal()
service = CarneService(session=db)

carne = service.criar_carne(CarneCreate(
    cliente_id=123,
    valor_total=1200,
    quantidade_parcelas=12,
    data_primeiro_vencimento=date(2024, 2, 1),
    gerar_boletos=True
))

print(f"Carnê: {carne.numero_carne}")
for parcela in carne.parcelas:
    print(f"  {parcela['numero_parcela']}: {parcela['codigo_barras']}")
```

### Gerar Boleto

```python
from crm_modules.faturamento.boleto_service import BoletoService
from datetime import date

db = SessionLocal()
service = BoletoService(session=db)

boleto = service.gerar_boleto_direto(
    cliente_id=123,
    valor=500.00,
    data_vencimento=date(2024, 2, 20)
)

print(f"Boleto: {boleto.numero_boleto}")
print(f"Código: {boleto.codigo_barras}")
print(f"Link: {boleto.url_boleto}")
```

### Sincronizar

```python
service = BoletoService(session=db)
atualizados = service.sincronizar_pagamentos_gerencianet()
print(f"{len(atualizados)} boletos sincronizados")
```

---

## 📊 Fluxo Visual

```
Cliente solicita 12x
        ↓
POST /api/faturamento/carnes
        ↓
Carnê criado (id=1)
        ↓
12 Parcelas criadas
        ↓
12 Boletos gerados no Gerencianet
        ↓
GET /api/faturamento/carnes/1/parcelas
        ↓
Cliente vê 12 boletos com códigos de barras
```

---

## 🔑 Variáveis .env

```env
GERENCIANET_CLIENT_ID=seu_id
GERENCIANET_CLIENT_SECRET=seu_secret
GERENCIANET_SANDBOX=true     # false em produção
APP_URL=http://localhost:8000
```

---

## 📱 Teste no Swagger

```
http://localhost:8000/docs
```

Abra no navegador e clique em "Try it out"

---

## 🆘 Problemas Comuns

| Erro | Solução |
|------|---------|
| `Invalid credentials` | Verifique .env |
| `Customer not found` | Cliente precisa de email |
| `Webhook timeout` | Configure APP_URL |
| `Duplicate reference` | Números já existem |

---

## 📖 Docs Completa

- **Setup**: `IMPLEMENTACAO_CARNES_BOLETOS.md`
- **API**: `INTEGRACAO_GERENCIANET.md`
- **FAQ**: `FAQ_CARNES_BOLETOS.md`
- **Exemplos**: `exemplo_carne_boleto.py`

---

## 🎯 Status em 1 Linha

✅ **Pronto para produção**. Crie carnês e boletos em minutos com integração Gerencianet.

---

**Tempo de leitura: 2 minutos**  
**Tempo para usar: 5 minutos**
