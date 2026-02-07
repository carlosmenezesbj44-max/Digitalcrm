# 🎨 Interface Gráfica - Carnês e Boletos

## Visão Geral

Páginas web completas para criar e gerenciar carnês e boletos sem usar API ou terminal.

### Páginas Criadas

- **`/carnes`** - Gerenciar carnês (planos de pagamento)
- **`/boletos`** - Gerenciar boletos

---

## 🚀 Como Acessar

### 1. Iniciar a Aplicação

```bash
python main.py
```

### 2. Acessar as Páginas

**Carnês**:
```
http://localhost:8000/carnes
```

**Boletos**:
```
http://localhost:8000/boletos
```

---

## 📋 Página de Carnês (`/carnes`)

### O que é?

Interface para criar planos de pagamento parcelado. Exemplo: Cliente quer pagar R$ 1.200 em 12 parcelas.

### Recursos

✅ **Criar Carnês**
- Cliente
- Valor total
- Quantidade de parcelas (2-360)
- Intervalo entre parcelas (dias)
- Data do primeiro vencimento
- Descrição
- Gerar boletos automaticamente

✅ **Visualizar Carnês**
- Tabela com todos os carnês
- Filtros por cliente e status
- Status de cada carnê (ativo, finalizado, cancelado)

✅ **Ver Parcelas**
- Lista todas as parcelas
- Mostra status (pendente, pago)
- Código de barras de cada parcela
- Link para baixar boleto

✅ **Registrar Pagamentos**
- Marcar parcela como paga
- Registrar valor pago
- Confirmação automática

✅ **Cancelar Carnês**
- Cancela todas as parcelas pendentes
- Cancela boletos no Gerencianet

---

## 📊 Como Usar a Página de Carnês

### Passo 1: Acessar

```
http://localhost:8000/carnes
```

Você verá:
- **Resumo superior** com totais
- **Filtros** para buscar carnês
- **Tabela** com lista de carnês
- **Botão azul** "Novo Carnê"

### Passo 2: Criar um Carnê

Clique no botão **"+ Novo Carnê"**

**Preencha:**

1. **Cliente** - Selecione na lista
2. **Valor Total** - Ex: 1200,00
3. **Quantidade de Parcelas** - Ex: 12
4. **Intervalo** - Deixe 30 (1 mês)
5. **Primeiro Vencimento** - Selecione a data
6. **Descrição** - Opcional (Ex: Serviços)
7. **Gerar Boletos** - Deixe marcado ✓

Clique em **"Criar Carnê"**

**Resultado:**
- ✅ Carnê criado no banco
- ✅ 12 parcelas criadas
- ✅ 12 boletos gerados no Gerencianet
- ✅ Mensagem de sucesso

### Passo 3: Ver as Parcelas

Na tabela, clique no botão **👁️** (Ver Parcelas)

Você verá:
- Lista de todas as 12 parcelas
- Data de vencimento de cada uma
- Status (pendente/pago)
- Código de barras
- Link para baixar boleto

### Passo 4: Registrar Pagamento

Se cliente pagou uma parcela:
1. Clique no botão ✓ (verde) ao lado da parcela
2. Digite o valor pago
3. Clique "Registrar Pagamento"
4. Status muda para "pago" automaticamente

### Passo 5: Cancelar Carnê (Opcional)

Se precisar cancelar:
1. Clique no botão ✗ (vermelho) na tabela
2. Confirme a ação
3. Todas as parcelas pendentes são canceladas

---

## 💳 Página de Boletos (`/boletos`)

### O que é?

Interface para gerar boletos para cobranças únicas ou de faturas.

### Recursos

✅ **Criar Boletos Diretos**
- Cliente
- Valor
- Data de vencimento
- Descrição
- Juros (opcional)
- Multa por atraso (opcional)

✅ **Gerar Boleto de Fatura**
- Selecione uma fatura existente
- Gera boleto automaticamente

✅ **Visualizar Boletos**
- Em **tabela** ou **cards**
- Filtros por cliente e status
- Código de barras
- Link de download

✅ **Sincronizar com Gerencianet**
- Atualizar status de todos os boletos
- Ver quais foram pagos

---

## 📊 Como Usar a Página de Boletos

### Passo 1: Acessar

```
http://localhost:8000/boletos
```

Você verá:
- **Resumo** com totais
- **Abas** para tabela ou cards
- **Filtros**
- **Botão azul** "Novo Boleto"

### Passo 2: Criar um Boleto Direto

Clique em **"+ Novo Boleto"**

**Na aba "Boleto Direto":**

1. **Cliente** - Selecione
2. **Valor** - Ex: 500,00
3. **Vencimento** - Selecione data
4. **Descrição** - Opcional
5. **Juros por Dia** - Opcional (Ex: 0.05%)
6. **Multa por Atraso** - Opcional (Ex: 2%)

Clique **"Gerar Boleto"**

**Resultado:**
- ✅ Boleto criado no Gerencianet
- ✅ Código de barras gerado
- ✅ Link PDF disponível

### Passo 3: Gerar Boleto de Fatura

Clique em **"+ Novo Boleto"**

**Na aba "De Fatura":**

1. **Fatura** - Selecione na lista
2. **Juros/Multa** - Opcional

Clique **"Gerar Boleto"**

### Passo 4: Visualizar de Diferentes Formas

**Tabela:**
- Clique na aba "Visualização em Tabela"
- Lista formatada com todas as colunas

**Cards:**
- Clique na aba "Visualização em Cards"
- Cards com código de barras visível
- Mais visual e moderno

### Passo 5: Baixar Boleto

**Na tabela ou cards:**
1. Clique no ícone **⬇️** (download)
2. Abre PDF do boleto no navegador
3. Salve ou imprima

### Passo 6: Sincronizar com Gerencianet

Clique no botão **☁️** (nuvem)

Sistema:
- ✅ Consulta Gerencianet
- ✅ Verifica quais foram pagos
- ✅ Atualiza status
- ✅ Mostra resumo

---

## 🎨 Características da Interface

### Design Responsivo

- ✅ Funciona em Desktop
- ✅ Funciona em Tablet
- ✅ Funciona em Mobile

### Cores e Ícones

- **Verde** ✓ = Pago/Sucesso
- **Amarelo** ⏳ = Pendente
- **Vermelho** ✗ = Cancelado/Erro
- **Azul** ℹ️ = Informação

### Validação

- Campo obrigatório marcado com *
- Avisos se campo vazio
- Confirmação antes de ações importantes
- Mensagens de sucesso/erro

---

## 📱 Resumo de Botões

### Carnês

| Ícone | Função |
|-------|--------|
| ➕ | Novo carnê |
| 👁️ | Ver parcelas |
| ✏️ | Editar carnê |
| ✗ | Cancelar carnê |

### Boletos

| Ícone | Função |
|-------|--------|
| ➕ | Novo boleto |
| 👁️ | Ver detalhes |
| ⬇️ | Baixar PDF |
| ☁️ | Sincronizar |

---

## 🆘 Troubleshooting

### Erro: "Cliente não encontrado"

**Causa**: Cliente não tem email cadastrado

**Solução**:
1. Vá em **Cadastros** → **Listar Clientes**
2. Edite o cliente
3. Preencha **Email**
4. Salve

### Erro: "Credenciais inválidas"

**Causa**: Gerencianet não configurado

**Solução**:
1. Abra arquivo `.env`
2. Preencha:
   ```env
   GERENCIANET_CLIENT_ID=seu_id
   GERENCIANET_CLIENT_SECRET=seu_secret
   ```
3. Reinicie a aplicação

### Boleto não aparece

**Causa**: API ainda carregando

**Solução**:
1. Clique em **Atualizar** (botão com seta)
2. Aguarde alguns segundos
3. Recarregue a página (F5)

### Parcela não marca como pago

**Causa**: Valor incorreto

**Solução**:
1. Verifique se o valor está correto
2. Clique no ✓ novamente
3. Digite o valor exato

---

## 🔒 Segurança

- ✅ Requer autenticação
- ✅ Token JWT
- ✅ Dados criptografados
- ✅ Confirmação de ações importantes

---

## 📸 Fluxo Visual

### Criar Carnê

```
Página /carnes
    ↓
Clique "+ Novo Carnê"
    ↓
Preencha formulário
    ↓
Clique "Criar Carnê"
    ↓
12 boletos gerados automaticamente
    ↓
Clique "Ver Parcelas" para listar
    ↓
Cliente baixa boletos e paga
```

### Gerar Boleto

```
Página /boletos
    ↓
Clique "+ Novo Boleto"
    ↓
Escolha: "Direto" ou "De Fatura"
    ↓
Preencha dados
    ↓
Clique "Gerar Boleto"
    ↓
Boleto criado no Gerencianet
    ↓
Clique ⬇️ para baixar PDF
```

---

## 💡 Dicas

1. **Sempre preencha o email do cliente** antes de criar boletos
2. **Use "Gerar Boletos" automaticamente** ao criar carnês
3. **Sincronize diariamente** com Gerencianet para atualizar status
4. **Use Cards** para visualização mais amigável
5. **Filtros** ajudam a encontrar boletos específicos

---

## 🚀 Próximas Melhorias

- [ ] Enviar boleto por email
- [ ] Imprimir carnê
- [ ] Gráficos de recebimento
- [ ] Dashboard com KPIs
- [ ] Exportar para Excel
- [ ] Agendamento de boletos

---

## 📚 Documentação Relacionada

- `INTEGRACAO_GERENCIANET.md` - Detalhes técnicos
- `FAQ_CARNES_BOLETOS.md` - Perguntas comuns
- `QUICK_REFERENCE.md` - Cola rápida

---

**Status**: ✅ Pronto para uso  
**Versão**: 1.0  
**Última atualização**: 2024-01-18
