# 🎯 Como Usar - Interface de Carnês e Boletos

## ✅ Problema Resolvido: Erro 404

O erro `Failed to load resource: the server responded with a status of 404 (Not Found)` foi corrigido!

As rotas foram adicionadas ao `main.py`:
- `/carnes` - Página de carnês
- `/boletos` - Página de boletos

---

## 🚀 Passo a Passo

### 1️⃣ Garantir que a Aplicação Está Rodando

```bash
# No terminal, execute:
python interfaces/api/main.py

# Ou
uvicorn interfaces.api.main:app --reload
```

**Saída esperada:**
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 2️⃣ Acessar as Páginas

Abra no navegador:

**Carnês (Planos de Pagamento):**
```
http://localhost:8000/carnes
```

**Boletos:**
```
http://localhost:8000/boletos
```

---

## 📝 Criar Carnê (Exemplo Prático)

### Cenário
Cliente **"João Silva"** quer pagar **R$ 1.200** em **12 parcelas**.

### Passo 1: Acessar Página
```
http://localhost:8000/carnes
```

Você verá:
- Cabeçalho com "Novo Carnê" (botão azul)
- Resumo com totais
- Tabela vazia ou com carnês existentes

### Passo 2: Clicar em "+ Novo Carnê"

Abre um formulário com abas:

### Passo 3: Preencher Formulário

| Campo | Valor | Obrigatório |
|-------|-------|------------|
| **Cliente** | João Silva | ✅ Sim |
| **Valor Total** | 1200,00 | ✅ Sim |
| **Quantidade de Parcelas** | 12 | ✅ Sim |
| **Intervalo (dias)** | 30 | ❌ Não (padrão) |
| **Primeiro Vencimento** | 01/02/2024 | ✅ Sim |
| **Descrição** | Serviços consultoria | ❌ Não |
| **Gerar Boletos** | ✓ Marcado | ✅ Recomendado |

### Passo 4: Clicar "Criar Carnê"

**O sistema:**
- ✅ Cria o carnê no banco
- ✅ Divide R$ 1.200 ÷ 12 = R$ 100 por parcela
- ✅ Cria 12 parcelas com datas diferentes:
  - Parcela 1: 01/02/2024 - R$ 100
  - Parcela 2: 01/03/2024 - R$ 100
  - Parcela 3: 01/04/2024 - R$ 100
  - ... (até parcela 12)
- ✅ Gera 12 boletos no Gerencianet
- ✅ Obtém código de barras para cada um
- ✅ Mostra mensagem de sucesso

**Mensagem:**
```
✓ Carnê criado com sucesso!

Número: CARNE-20240118-0001-001
12x de R$ 100.00
```

### Passo 5: Ver as Parcelas

Na tabela, clique no ícone **👁️** (Ver Parcelas)

Você vê:
```
Parcela 1
├─ Vence em: 01/02/2024
├─ Status: pendente
├─ Valor: R$ 100,00
├─ Código: 12345.67890...
└─ Botão: Baixar Boleto / Registrar Pagamento

Parcela 2
├─ Vence em: 01/03/2024
├─ Status: pendente
├─ Valor: R$ 100,00
...
```

---

## 💳 Criar Boleto (Exemplo Prático)

### Cenário A: Boleto Direto
Cliente quer pagar **R$ 500** como pagamento adicional.

### Acesso
```
http://localhost:8000/boletos
```

### Passo 1: Clicar "+ Novo Boleto"

### Passo 2: Selecionar Aba "Boleto Direto"

### Passo 3: Preencher

| Campo | Valor |
|-------|-------|
| **Cliente** | Maria Silva |
| **Valor** | 500,00 |
| **Vencimento** | 28/02/2024 |
| **Descrição** | Pagamento adicional |
| **Juros** | 0 |
| **Multa** | 0 |

### Passo 4: Clicar "Gerar Boleto"

**Resultado:**
```
✓ Boleto gerado com sucesso!

Número: BOL-20240118-0002-0001
Valor: R$ 500,00
```

### Cenário B: Boleto de Fatura
Gerar boleto para fatura existente.

### Aba "De Fatura"

| Campo | Valor |
|-------|-------|
| **Fatura** | FAT-001 - R$ 1.500 |
| **Juros** | 0.05 |
| **Multa** | 2.0 |

### Resultado
Boleto criado com juros e multa configurados.

---

## 📊 Visualizar Boletos

### Abas

**1️⃣ Tabela**
- Formato tradicional
- Colunas: Número, Cliente, Valor, Vencimento, Status
- Botões de ação

**2️⃣ Cards**
- Visual mais moderno
- Cards com código de barras
- Melhor para mobile

### Filtros

**Cliente:**
- Selecione um cliente específico
- Deixe em branco para ver todos

**Status:**
- Pendente
- Pago
- Cancelado

**Exemplo:**
```
Cliente: João Silva
Status: Pendente
Resultado: 3 boletos de João Silva ainda não pagos
```

---

## ✅ Registrar Pagamento

### Quando Cliente Paga

**Na página de Carnês:**
1. Clique "Ver Parcelas"
2. Clique no botão ✓ (verde) da parcela
3. Preencha:
   - **Valor Pago:** Digite exato (R$ 100,00)
   - **Data:** Deixa automática ou mude
4. Clique "Registrar Pagamento"

**Resultado:**
- Status muda para ✅ **pago**
- Data de pagamento registrada
- Se todas as 12 pagas → Carnê finalizado

---

## 🔄 Sincronizar com Gerencianet

**Por que?**
Para atualizar status dos boletos quando cliente paga no banco.

**Como:**
1. Vá para `/boletos`
2. Clique no botão ☁️ (nuvem com verificação)
3. Aguarde sincronização
4. Vê mensagem: "15 boletos sincronizados"

**Automaticamente:**
- Procura por pagamentos no Gerencianet
- Atualiza status no CRM
- Marca como pago

---

## 🎓 Fluxo Completo (Fim a Fim)

```
CLIENTE SOLICITA PARCELAMENTO
        ↓
    [VOCÊ]
    Acessa http://localhost:8000/carnes
        ↓
    Clica "+ Novo Carnê"
        ↓
    Preenche:
    - Cliente: João
    - Valor: 1200
    - Parcelas: 12
    - Data: 01/02/2024
        ↓
    Clica "Criar Carnê"
        ↓
    SISTEMA
    - Cria 12 parcelas
    - Gera 12 boletos
    - Obtém códigos de barras
        ↓
    VOCÊ
    Clica "Ver Parcelas"
        ↓
    CLIENTE
    Recebe link/boleto
    Paga no banco
        ↓
    1-2 DIAS DEPOIS
    VOCÊ sincroniza
    Clica ☁️ em /boletos
        ↓
    SISTEMA
    Verifica Gerencianet
    Atualiza status para "pago"
        ↓
    VOCÊ
    Vê: ✅ Parcela 1 paga
         ✅ Parcela 2 paga
         ⏳ Parcelas 3-12 pendentes
```

---

## 🐛 Troubleshooting

### Erro: "Cliente não encontrado"

**Causa:** Cliente sem email

**Solução:**
1. Volte ao menu principal
2. Vá para **Cadastros** → **Listar Clientes**
3. Clique para editar o cliente
4. Preencha o **Email**
5. Salve
6. Volte e tente novamente

### Erro: "Credenciais inválidas"

**Causa:** Gerencianet não configurado

**Solução:**
1. Abra `.env`
2. Preencha:
   ```env
   GERENCIANET_CLIENT_ID=seu_id
   GERENCIANET_CLIENT_SECRET=seu_secret
   ```
3. Reinicie a aplicação
4. Tente novamente

### Página em branco

**Causa:** Template não encontrado

**Solução:**
1. Verifique se os arquivos existem:
   - `interfaces/web/templates/carnes.html`
   - `interfaces/web/templates/boletos.html`
2. Verifique os caminhos no `main.py`
3. Reinicie a aplicação

### Botões não funcionam

**Causa:** API não está respondendo

**Solução:**
1. Certifique-se que `/api/faturamento/*` está ativa
2. Verifique no console do navegador (F12)
3. Procure por erros na aba Network
4. Reinicie a aplicação

---

## 📌 Dicas Importantes

✅ **Sempre preencha Email do Cliente** antes de criar boletos

✅ **Use "Gerar Boletos" marcado** ao criar carnês

✅ **Sincronize diariamente** para manter status atualizado

✅ **Use Tabela** para buscar por filtros

✅ **Use Cards** para visualização amigável

✅ **Teste em Sandbox** antes de usar em produção

---

## 🎉 Resumo

| Ação | URL | Tempo |
|------|-----|-------|
| Criar carnê | `/carnes` | 2 min |
| Ver parcelas | `/carnes` → 👁️ | 1 min |
| Registrar pagamento | `/carnes` → ✓ | 1 min |
| Criar boleto | `/boletos` | 2 min |
| Sincronizar | `/boletos` → ☁️ | 30 seg |
| Baixar boleto | `/boletos` → ⬇️ | 1 min |

---

**Agora está pronto!** 🚀

Acesse: `http://localhost:8000/carnes` e comece a criar carnês!
