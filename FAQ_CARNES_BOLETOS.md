# FAQ - Carnês e Boletos com Gerencianet

## Perguntas Frequentes

---

### 1. **O que é um Carnê?**

Um carnê é um **plano de pagamento parcelado**. 

**Exemplo**: 
- Cliente deve R$ 1.200
- Quer pagar em 12 parcelas de R$ 100
- Cada mês vence uma parcela
- Cada parcela gera um boleto

---

### 2. **Qual a diferença entre Carnê e Boleto?**

| Carnê | Boleto |
|-------|--------|
| Múltiplas parcelas | Uma cobrança única |
| Ex: 12x de R$ 100 | Ex: R$ 1.200 |
| Vários vencimentos | Um vencimento |
| Gera boleto por parcela | Um boleto só |

---

### 3. **Como criar um Carnê?**

```python
POST /api/faturamento/carnes

{
    "cliente_id": 123,
    "valor_total": 1200.00,
    "quantidade_parcelas": 12,
    "data_primeiro_vencimento": "2024-02-01",
    "intervalo_dias": 30,
    "gerar_boletos": true
}
```

O sistema:
1. ✅ Divide R$ 1.200 ÷ 12 = R$ 100 cada
2. ✅ Cria 12 parcelas com datas diferentes
3. ✅ Gera boleto para cada parcela no Gerencianet
4. ✅ Retorna links dos boletos

---

### 4. **O cliente precisa de CPF e Email?**

**Sim.** Obrigatório:
- **Email**: Para enviar boleto
- **CPF**: Para o boleto bancário

Se não tiver dados completos, error:
```json
{
    "error": "Cliente não possui email cadastrado"
}
```

---

### 5. **Como sincronizar pagamentos?**

```python
# Sincronizar um boleto
PUT /api/faturamento/boletos/1/sincronizar

# Ou todos de uma vez
POST /api/faturamento/boletos/sincronizar/todos
```

Isso consulta Gerencianet e atualiza:
- ✅ Boletos pagos
- ✅ Boletos cancelados
- ✅ Boletos vencidos

---

### 6. **Como saber se o cliente pagou?**

### Opção A: Webhooks (Automático)

Gerencianet notifica sua app:
```
POST /api/faturamento/webhooks/gerencianet/boleto
{
    "id": 12345,
    "status": "paid"
}
```

Sistema atualiza automaticamente.

### Opção B: Sincronizar (Manual)

```python
POST /api/faturamento/boletos/sincronizar/todos
```

---

### 7. **Como cancelar um Carnê?**

```python
DELETE /api/faturamento/carnes/1/cancelar
```

Resultado:
- ✅ Todas as parcelas pendentes são canceladas
- ✅ Boletos no Gerencianet são cancelados
- ✅ Status fica "cancelado"

**Nota**: Não pode cancelar se tiver parcelas já pagas.

---

### 8. **Posso ajustar parcelas já criadas?**

Não diretamente. Você deve:
1. ❌ Cancelar o carnê original
2. ✅ Criar um novo com os valores corretos

Exemplo:
```python
# 1. Cancelar
DELETE /api/faturamento/carnes/1/cancelar

# 2. Criar novo
POST /api/faturamento/carnes
{
    "cliente_id": 123,
    "valor_total": 1500.00,  # Novo valor
    "quantidade_parcelas": 15,  # Novo número
    "gerar_boletos": true
}
```

---

### 9. **Qual é o número máximo de parcelas?**

**360 parcelas** (30 anos).

Limitações práticas:
- 12x - Mensal (padrão)
- 24x - 2 anos
- 60x - 5 anos
- 360x - 30 anos (raro)

---

### 10. **Posso cobrar juros e multa?**

**Sim!** Ao gerar boleto:

```python
POST /api/faturamento/boletos

{
    "cliente_id": 123,
    "valor": 500.00,
    "data_vencimento": "2024-02-20",
    "juros_dia": 0.05,      # 0.05% ao dia
    "multa_atraso": 2.0      # 2% de multa
}
```

Valores são configuraços por boleto.

---

### 11. **Como enviar boleto por email?**

**Atualmente**: Sistema não envia automaticamente.

**Próximo passo**: Integrar com SMTP:

```python
# Será implementado em breve
service.enviar_boleto_por_email(
    parcela_id=1,
    cliente_email="cliente@exemplo.com"
)
```

**Workaround atual**:
1. Obter URL do boleto na resposta
2. Enviar link para cliente
3. Cliente acessa e baixa PDF

---

### 12. **Como saber quais boletos venceram?**

```python
GET /api/faturamento/boletos/vencidos/listar
```

Retorna:
- Data de vencimento < hoje
- Status = "pendente"

**Use para**: Enviar lembretes, cobranças, etc.

---

### 13. **Posso ter múltiplos carnês por cliente?**

**Sim!** Um cliente pode ter vários carnês simultâneos.

```python
GET /api/faturamento/carnes/cliente/123
```

Retorna todos os carnês do cliente 123.

---

### 14. **O que fazer se o Gerencianet cair?**

Sistema funciona:

1. ✅ Localmente:
   - Criar carnê (sem Gerencianet)
   - Salvar dados no BD
   - Gerar números

2. ❌ Sem Gerencianet:
   - Não gera boleto (erro)
   - Não sincroniza status
   - Não recebe webhooks

**Solução**: Quando voltar:
```python
POST /api/faturamento/boletos/sincronizar/todos
```

---

### 15. **Como testar antes de produção?**

Use **SANDBOX**:

```env
GERENCIANET_SANDBOX=true
```

Características:
- ✅ Dados de teste fornecidos
- ✅ Sem cobranças reais
- ✅ Mesmo comportamento da produção
- ✅ Dados fictícios garantidos

Dados de teste:
- CPF: `94087216055`
- Email: `teste@sandboxgerencianet.com.br`

---

### 16. **Como migrar de SANDBOX para produção?**

```env
# Mudar de:
GERENCIANET_SANDBOX=true

# Para:
GERENCIANET_SANDBOX=false

# E use credenciais de produção
GERENCIANET_CLIENT_ID=seu_id_producao
GERENCIANET_CLIENT_SECRET=seu_secret_producao
```

**Cuidado!** Isso gera **cobranças reais**.

---

### 17. **Posso gerar boleto sem carnê?**

**Sim!** Boleto direto:

```python
POST /api/faturamento/boletos

{
    "cliente_id": 123,
    "valor": 500.00,
    "data_vencimento": "2024-02-20"
}
```

Uso: Pagamentos únicos, taxa, ajuste, etc.

---

### 18. **Como listar todas as parcelas de um carnê?**

```python
GET /api/faturamento/carnes/1/parcelas
```

Retorna:
```json
[
    {
        "numero": 1,
        "valor": 100.00,
        "data_vencimento": "2024-02-01",
        "status": "pendente",
        "codigo_barras": "..."
    },
    ...
]
```

---

### 19. **Como registrar pagamento manual?**

Se cliente pagou sem boleto (ex: transferência):

```python
POST /api/faturamento/parcelas/1/pagar?valor_pago=100.0
```

Resultado:
- ✅ Parcela marcada como "pago"
- ✅ Data de pagamento registrada
- ✅ Se todas pagas → Carnê finalizado

---

### 20. **Qual é o custo do Gerencianet?**

Varia conforme tipo:

- **Boleto**: 2-5% do valor
- **Cartão**: 2-3% do valor
- **Mensalidade**: A partir de R$ 10

[Consulte tabela atual](https://gerencianet.com.br/precos)

---

### 21. **Erro: "Invalid credentials"**

**Causa**: Client ID ou Secret incorretos.

**Solução**:
1. Acesse https://gerencianet.com.br
2. Vá em **Aplicações** → **Minhas Aplicações**
3. Copie `Client ID` e `Client Secret` corretos
4. Atualize no `.env`
5. Teste novamente

---

### 22. **Erro: "Customer not found"**

**Causa**: Dados do cliente incompletos.

**Solução**: Verifique se cliente tem:
- ✅ Email preenchido
- ✅ CPF preenchido
- ✅ Nome preenchido

```python
# Verificar
GET /api/clientes/123

# Atualizar
PUT /api/clientes/123
{
    "email": "cliente@exemplo.com",
    "cpf": "12345678900",
    "nome": "João Silva"
}
```

---

### 23. **Erro: "Webhook timeout"**

**Causa**: URL não acessível.

**Solução**:
1. Verificar `APP_URL` no `.env`
2. Garantir que app está rodando
3. Testar webhook no painel Gerencianet

```env
APP_URL=http://seu-dominio.com.br
# Não use localhost em produção!
```

---

### 24. **Como fazer relatório de recebimento?**

```python
GET /api/faturamento/carnes/cliente/123

# Retorna carnês e parcelas com status:
{
    "id": 1,
    "numero_carne": "CARNE-...",
    "valor_total": 1200.00,
    "parcelas": [
        {
            "numero": 1,
            "valor": 100.00,
            "status": "pago",
            "data_pagamento": "2024-02-05"
        },
        ...
    ]
}
```

Daí você calcula:
- Total devido
- Total pago
- Pendente
- Taxa de recebimento

---

### 25. **Posso integrar com outro payment gateway?**

**Sim!** Mas precisa:

1. Criar novo `Client`:
```python
class PagSeguroClient:
    def gerar_boleto(...): ...
    def consultar_status(...): ...
```

2. Criar nova `Service`:
```python
class BoleatoPagSeguroService:
    def gerar_boleto(...): ...
```

3. Implementar no `Service` principal:
```python
if provider == "gerencianet":
    client = GerencianetClient()
elif provider == "pagseguro":
    client = PagSeguroClient()
```

---

## 🆘 Não encontrou a resposta?

1. Consulte **INTEGRACAO_GERENCIANET.md**
2. Veja exemplos em **exemplo_carne_boleto.py**
3. Abra issue ou contate suporte

---

**Última atualização**: 2024-01-18  
**Versão**: 1.0
