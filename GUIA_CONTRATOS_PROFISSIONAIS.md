# 📋 Guia Completo: Contratos Profissionais e Elaborados

## 🎯 Visão Geral

Este documento descreve o sistema de contratos profissionais do CRM Provedor, que agora inclui:

✅ **Formulário elaborado** com seções bem organizadas  
✅ **Vínculo automático** com datas de pagamento  
✅ **Geração automática** de faturas relacionadas  
✅ **Template PDF profissional** com cronograma  
✅ **Gestão completa** do ciclo de vida do contrato  

---

## 📊 Arquitetura de Dados

### Modelo de Contrato (ContratoModel)

O modelo foi expandido com campos de pagamento:

```python
# Campos adicionados:
data_primeiro_pagamento: DateTime      # Primeira data de vencimento
data_proximo_pagamento: DateTime       # Próximo vencimento
dia_pagamento: Integer                 # Dia fixo (1-31)
frequencia_pagamento: String           # mensal, bimestral, etc
desconto_total: Float                  # Desconto a aplicar
juros_atraso_percentual: Float         # % de juros/mês
```

### Fluxo de Dados

```
Novo Contrato
    ↓
[Validação do Cliente]
    ↓
[Cálculo de Datas de Pagamento]
    ↓
[Criação no Banco de Dados]
    ↓
[Geração de PDF Profissional]
    ↓
[Geração Automática de Faturas]
    ↓
[Registro em Histórico de Auditoria]
```

---

## 🖥️ Interface de Criação (novo_contrato.html)

### Seções do Formulário

#### **1. Informações do Cliente**
- Seleção de cliente existente
- Busca por nome/email integrada

#### **2. Informações do Contrato**
- Título do contrato
- Descrição detalhada
- Tipo de contrato (Serviço, Assinatura, Manutenção, Suporte, Outro)
- Política de renovação (Manual, Automática, Não Renovável)

#### **3. Vigência do Contrato**
- Data de início
- Data de término (auto-calculada para 12 meses)

#### **4. Valores e Financeiro**
- Valor do contrato/período (obrigatório)
- Moeda (BRL, USD, EUR)
- Desconto total (opcional)

#### **5. Configuração de Pagamentos**
- Dia de vencimento (1-28)
- Frequência (Mensal, Bimestral, Trimestral, Semestral, Anual)
- Juros por atraso (% ao mês)

#### **6. Observações**
- Observações internas e cláusulas especiais

#### **7. Geração do Contrato**
- Checkbox para gerar PDF automaticamente

### Validações Implementadas

✅ **Validação de Datas**: Data término > Data início  
✅ **Validação de Valores**: Valor > 0  
✅ **Cliente Obrigatório**: Selecionar cliente válido  
✅ **Sincronização de Data**: Auto-calcula término em 12 meses  

---

## 📄 Template PDF Profissional

### Localização
`crm_modules/contratos/infrastructure/pdf/templates/contrato_profissional.html`

### Estrutura do Documento

O PDF inclui 9 seções principais:

1. **Cabeçalho**: Informações do documento
2. **Partes**: Dados da empresa e cliente (lado a lado)
3. **Objeto**: Descrição dos serviços
4. **Valores**: Tabela de valores com desconto
5. **Cronograma**: Tabela de pagamentos calculada
6. **Obrigações da Contratada**: 8 obrigações principais
7. **Obrigações do Contratante**: 6 obrigações principais
8. **Multas e Penalidades**: Tabela de atrasos
9. **Vigência e Rescisão**: Termos de renovação

### Placeholders Dinâmicos

```
{{ empresa_nome }}              # Nome da empresa
{{ empresa_cnpj }}              # CNPJ
{{ empresa_ie }}                # Inscrição Estadual
{{ empresa_endereco }}          # Endereço completo
{{ empresa_telefone }}          # Telefone
{{ empresa_email }}             # Email

{{ cliente_nome }}              # Nome do cliente
{{ cliente_cpf }}               # CPF/CNPJ
{{ cliente_endereco }}          # Endereço
{{ cliente_telefone }}          # Telefone
{{ cliente_email }}             # Email

{{ contrato_id }}               # Número do contrato
{{ contrato_titulo }}           # Título
{{ contrato_tipo }}             # Tipo (serviço, assinatura, etc)
{{ contrato_descricao }}        # Descrição detalhada

{{ data_vigencia_inicio }}      # Data início
{{ data_vigencia_fim }}         # Data término
{{ contrato_valor_formatado }}  # Valor formatado (R$)
{{ desconto_formatado }}        # Desconto formatado
{{ valor_liquido_formatado }}   # Valor líquido

{{ dia_pagamento }}             # Dia (10º, 15º, etc)
{{ frequencia_pagamento }}      # Frequência (mensal, etc)
{{ juros_atraso_percentual }}   # Taxa de juros
{{ status_renovacao }}          # Manual/Automática

{{ cronograma_pagamentos }}     # Tabela HTML das parcelas
{{ observacoes }}               # Observações especiais
{{ data_atual }}                # Data de geração

{{ empresa_cidade }}            # Cidade para foro
```

---

## 💰 Geração Automática de Faturas

### Como Funciona

Quando um contrato é criado com valor definido, o sistema **gera automaticamente** as faturas:

1. **Calcula primeira data de vencimento** baseada no dia_pagamento
2. **Itera pelo período** do contrato até a data_vigencia_fim
3. **Respeita a frequência** (mensal, bimestral, etc)
4. **Aplica desconto** se houver
5. **Cria registro** na tabela `faturas`

### Exemplo de Geração

```
Contrato:
- Valor: R$ 1.000,00
- Desconto: R$ 100,00
- Frequência: Mensal
- Dia: 10º
- Início: 01/01/2026
- Fim: 31/12/2026

Resultado: 12 faturas
FAT-0001-01 | 10/01/2026 | R$ 900,00
FAT-0001-02 | 10/02/2026 | R$ 900,00
FAT-0001-03 | 10/03/2026 | R$ 900,00
...
FAT-0001-12 | 10/12/2026 | R$ 900,00
```

### Código Responsável

```python
def _gerar_faturas_automaticas(self, model):
    # Localizado em: crm_modules/contratos/service.py
    # Itera sobre as datas de vencimento
    # Cria FaturaModel para cada período
    # Aplica frequência de pagamento
```

---

## 🔄 Fluxo de Ciclo de Vida do Contrato

```
1. CRIAÇÃO
   ├─ Usuário preenche formulário novo_contrato.html
   ├─ Validações são executadas
   ├─ ContratoModel é criado
   └─ Estado: AGUARDANDO_ASSINATURA

2. GERAÇÃO DE DOCUMENTOS
   ├─ PDF é gerado automaticamente
   ├─ Faturas são criadas
   └─ Histórico é registrado

3. ASSINATURA
   ├─ Usuário assina digitalmente
   ├─ Hash é validado
   └─ Estado: ASSINADO

4. LIBERAÇÃO
   ├─ Admin libera manualmente
   └─ Estado: LIBERADO

5. VIGÊNCIA
   ├─ Contrato ativo
   ├─ Faturas são cobradas
   └─ Histórico registra alterações

6. RENOVAÇÃO/RESCISÃO
   ├─ Auto-renova (se configurado)
   ├─ Ou é rescindido
   └─ Estado: EXPIRADO ou RENOVADO
```

---

## 📦 Database Schema

### Migration: `0008_add_payment_fields_to_contratos.py`

```sql
ALTER TABLE contratos ADD COLUMN data_primeiro_pagamento DATETIME NULL;
ALTER TABLE contratos ADD COLUMN data_proximo_pagamento DATETIME NULL;
ALTER TABLE contratos ADD COLUMN dia_pagamento INTEGER DEFAULT 10;
ALTER TABLE contratos ADD COLUMN frequencia_pagamento VARCHAR(50) DEFAULT 'mensal';
ALTER TABLE contratos ADD COLUMN desconto_total FLOAT DEFAULT 0;
ALTER TABLE contratos ADD COLUMN juros_atraso_percentual FLOAT DEFAULT 1;
```

---

## 🛠️ Serviço de Contratos (ContratoService)

### Métodos Principais

#### `criar_contrato(contrato_data, usuario_id)`
Cria novo contrato com validação, PDF e faturas automáticas.

```python
service = ContratoService()
novo_contrato = service.criar_contrato(
    contrato_data=ContratoCreate(...),
    usuario_id="usuario_admin"
)
```

#### `_calcular_data_primeiro_pagamento(data_inicio, dia_pagamento)`
Calcula quando será o primeiro vencimento.

#### `_gerar_faturas_automaticas(model)`
Gera todas as faturas do contrato.

#### `_gerar_cronograma_pagamentos_html(model)`
Cria tabela HTML com cronograma para o PDF.

#### `assinar_contrato(contrato_id, assinatura_base64, hash_documento)`
Registra assinatura digital com auditoria.

#### `liberar_contrato(contrato_id, usuario_id, motivo)`
Libera contrato manualmente (admin).

#### `verificar_contratos_vencendo(dias)`
Verifica contratos próximos do vencimento.

---

## 📋 Checklist de Implementação

Use este checklist para acompanhar:

- [x] Migration criada (0008_add_payment_fields_to_contratos)
- [x] ContratoModel atualizado com novos campos
- [x] Schemas (ContratoCreate, ContratoResponse) atualizados
- [x] Formulário novo_contrato.html refeito
- [x] Template PDF profissional criado
- [x] ContratoService atualizado
  - [x] Método _calcular_data_primeiro_pagamento
  - [x] Método _gerar_faturas_automaticas
  - [x] Método _gerar_cronograma_pagamentos_html
- [x] Integração com FaturaModel
- [ ] Testes unitários (recomendado)
- [ ] Testes de integração (recomendado)
- [ ] API endpoints testados
- [ ] Documentação API atualizada

---

## 🧪 Testando o Sistema

### 1. Criar Contrato via Interface Web

```
URL: http://localhost:8001/contratos/novo
1. Selecionar cliente
2. Preencher dados
3. Clicar "Criar Contrato"
```

### 2. Verificar Geração de Faturas

```sql
SELECT * FROM faturas 
WHERE cliente_id = ? 
ORDER BY data_vencimento;
```

### 3. Baixar PDF

```
URL: http://localhost:8001/api/v1/contratos/{id}/pdf
```

### 4. Verificar Histórico

```python
historico = service.obter_historico(contrato_id)
```

---

## 🔐 Segurança e Auditoria

### Campos de Auditoria

```python
criado_por: String              # Usuário que criou
criado_em: DateTime             # Quando criou
atualizado_por: String          # Último a atualizar
atualizado_em: DateTime         # Quando atualizou
deletado_em: DateTime           # Quando deletou (soft delete)
```

### Histórico Detalhado

```python
ContratoHistoricoModel:
- contrato_id: FK
- campo_alterado: Nome do campo
- valor_anterior: Valor antes
- valor_novo: Valor depois
- alterado_por: Usuário
- alterado_em: Timestamp
- motivo: Motivo da alteração
- ip_address: IP da requisição
- user_agent: Browser/Client
```

---

## 📊 Relatórios e Estatísticas

### Métodos Disponíveis

```python
# Estatísticas gerais
stats = service.obter_estatisticas_contratos()
# {
#   'total': 42,
#   'aguardando': 5,
#   'assinado': 20,
#   'liberado': 17,
#   'vencendo_30_dias': 8,
#   'vencidos': 2
# }

# Contratos vencendo
vencendo = service.verificar_contratos_vencendo(dias=30)

# Contratos vencidos
vencidos = service.verificar_contratos_vencidos()

# Listar por cliente
do_cliente = service.listar_contratos_por_cliente(cliente_id)
```

---

## 🚀 Próximos Passos Recomendados

1. **Integração com Email**
   - Enviar PDF do contrato automaticamente
   - Lembretes de vencimento

2. **Dashboard de Contratos**
   - Gráficos de contratos por status
   - Receita por contrato
   - Timeline visual

3. **Renovação Automática**
   - Criar novo contrato automaticamente
   - Notificar cliente 30 dias antes

4. **Integração com Boleto/Pix**
   - Gerar boletos das faturas
   - Receber pagamentos automaticamente

5. **Relatórios Avançados**
   - Contratos por tipo
   - Análise de receita
   - Clientes com maior receita

---

## 📞 Suporte e Dúvidas

Para dúvidas sobre:

- **Formulário**: Ver `novo_contrato.html`
- **Template PDF**: Ver `contrato_profissional.html`
- **Lógica de Negócio**: Ver `crm_modules/contratos/service.py`
- **Banco de Dados**: Ver `crm_modules/contratos/models.py`

---

**Versão**: 1.0  
**Data**: 23 de Janeiro de 2026  
**Status**: ✅ Completo
