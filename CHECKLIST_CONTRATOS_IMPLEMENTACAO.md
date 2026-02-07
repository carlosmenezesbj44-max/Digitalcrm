# ✅ Checklist: Implementação de Contratos Profissionais

## 📋 Fase 1: Preparação do Banco de Dados

- [x] Migration `0008_add_payment_fields_to_contratos.py` criada
- [x] Campos adicionados:
  - [x] `data_primeiro_pagamento`
  - [x] `data_proximo_pagamento`
  - [x] `dia_pagamento`
  - [x] `frequencia_pagamento`
  - [x] `desconto_total`
  - [x] `juros_atraso_percentual`
- [ ] **AÇÃO MANUAL**: Executar migration: `alembic upgrade head`

---

## 📦 Fase 2: Atualização de Modelos

- [x] `ContratoModel` atualizado com 6 novos campos
- [x] `ContratoModel.dia_pagamento` (padrão: 10)
- [x] `ContratoModel.frequencia_pagamento` (padrão: "mensal")
- [x] `ContratoModel.desconto_total` (padrão: 0.0)
- [x] `ContratoModel.juros_atraso_percentual` (padrão: 1.0)
- [x] `ContratoModel.data_primeiro_pagamento` (nullable)
- [x] `ContratoModel.data_proximo_pagamento` (nullable)
- [x] Relacionamentos mantidos

---

## 📝 Fase 3: Schemas Pydantic

- [x] `ContratoBase` atualizado
  - [x] `data_primeiro_pagamento`
  - [x] `data_proximo_pagamento`
  - [x] `dia_pagamento`
  - [x] `frequencia_pagamento`
  - [x] `desconto_total`
  - [x] `juros_atraso_percentual`
- [x] `ContratoCreate` herda novos campos
- [x] `ContratoResponse` inclui novos campos
- [x] `ContratoResponse.Config.from_attributes = True`

---

## 🖥️ Fase 4: Interface Web

### novo_contrato.html
- [x] Criado do zero com design profissional
- [x] 7 Seções organizadas
  - [x] Informações do Cliente
  - [x] Informações do Contrato
  - [x] Vigência do Contrato
  - [x] Valores e Financeiro
  - [x] Configuração de Pagamentos
  - [x] Observações
  - [x] Geração do Contrato (PDF)
- [x] Estilo responsivo
  - [x] Desktop
  - [x] Tablet
  - [x] Mobile
- [x] Validações JavaScript
  - [x] Data término > Data início
  - [x] Valor > 0
  - [x] Cliente selecionado
- [x] Busca de cliente com modal
- [x] Auto-calcula data de término (12 meses)
- [x] Campos de entrada com help text
- [x] Mensagens de erro/sucesso

---

## 📄 Fase 5: Template PDF Profissional

### contrato_profissional.html
- [x] Criado template com 9 seções
- [x] **1. Cabeçalho**
  - [x] Número e data do contrato
  - [x] Identificação visual
- [x] **2. Partes**
  - [x] Dados empresa (lado esquerdo)
  - [x] Dados cliente (lado direito)
  - [x] CNPJ, IE, endereço, telefone, email
- [x] **3. Objeto do Contrato**
  - [x] Descrição dos serviços
  - [x] Período de execução
- [x] **4. Valores**
  - [x] Tabela valor × desconto
  - [x] Valor líquido destacado
- [x] **5. Cronograma de Pagamento**
  - [x] Tabela dinâmica com datas
  - [x] Valores aplicados
  - [x] Descrição das parcelas
- [x] **6. Obrigações da Contratada** (8 itens)
- [x] **7. Obrigações do Contratante** (6 itens)
- [x] **8. Multas e Penalidades**
  - [x] Tabela de atrasos
  - [x] Percentuais de multa
- [x] **9. Vigência e Rescisão**
  - [x] Termos de renovação
  - [x] Condições de rescisão
- [x] **Assinaturas** (espaço para manuscritas)
- [x] Placeholders dinâmicos todos mapeados
- [x] CSS profissional
  - [x] Cores corporativas (azul #003366)
  - [x] Tipografia clara
  - [x] Tables com linhas alternadas
  - [x] Print-friendly

---

## ⚙️ Fase 6: Serviço de Negócio (ContratoService)

### Método: criar_contrato()
- [x] Valida cliente existe
- [x] Calcula `data_primeiro_pagamento`
- [x] Calcula `data_proximo_pagamento`
- [x] Cria `ContratoModel` com novos campos
- [x] Gera PDF automaticamente
- [x] Gera faturas automaticamente
- [x] Registra no histórico
- [x] Atualiza status do cliente

### Método: _calcular_data_primeiro_pagamento()
- [x] Recebe data_inicio e dia_pagamento
- [x] Calcula primeira data de vencimento
- [x] Ajusta para próximo mês se necessário
- [x] Retorna DateTime formatado

### Método: _gerar_cronograma_pagamentos_html()
- [x] Gera tabela HTML com parcelas
- [x] Calcula datas conforme frequência
- [x] Aplica desconto
- [x] Formata valores em R$
- [x] Limita a 12 linhas
- [x] Respeita data_vigencia_fim

### Método: _gerar_faturas_automaticas()
- [x] Importa FaturaService
- [x] Calcula número de faturas
- [x] Itera conforme frequência
  - [x] Mensal
  - [x] Bimestral
  - [x] Trimestral
  - [x] Semestral
  - [x] Anual
- [x] Cria FaturaModel para cada período
- [x] Aplica desconto
- [x] Gera número único de fatura
- [x] Persiste no banco
- [x] Trata exceções

### Método: _model_to_dict()
- [x] Inclui todos os 6 novos campos
- [x] Formata datas em ISO
- [x] Retorna dicionário completo

---

## 🔄 Fase 7: Fluxo de Dados

- [x] novo_contrato.html → POST /contratos/novo
- [x] ContratoCreate → Validação Pydantic
- [x] Service.criar_contrato() → ContratoModel
- [x] ContratoModel → INSERT contratos
- [x] Cálculos de data → data_primeiro_pagamento
- [x] Geração de PDF → arquivo salvo
- [x] Geração de faturas → INSERT faturas
- [x] Histórico registrado → INSERT histórico

---

## 📊 Fase 8: Documentação

- [x] `GUIA_CONTRATOS_PROFISSIONAIS.md` criado
  - [x] Visão geral
  - [x] Arquitetura de dados
  - [x] Interface explicada
  - [x] Template PDF documentado
  - [x] Fluxo de vida do contrato
  - [x] Database schema
  - [x] Métodos do serviço
  - [x] Checklist de implementação
  - [x] Testes recomendados
  - [x] Relatórios disponíveis
  - [x] Próximos passos

- [x] `RESUMO_CONTRATOS_PROFISSIONAIS.md` criado
  - [x] Características principais
  - [x] Arquivos criados/modificados
  - [x] Como usar (passo-a-passo)
  - [x] Exemplo de uso prático
  - [x] Verificação de dados
  - [x] Seções do PDF listadas
  - [x] Configurações padrão
  - [x] Fluxo de integração
  - [x] Métricas de sucesso
  - [x] Troubleshooting

- [x] `CHECKLIST_CONTRATOS_IMPLEMENTACAO.md` (este arquivo)

---

## 🧪 Fase 9: Testes Necessários

### Testes Unitários
- [ ] `test_criar_contrato_valido()`
- [ ] `test_criar_contrato_cliente_inexistente()`
- [ ] `test_calcular_data_primeiro_pagamento()`
- [ ] `test_gerar_cronograma_pagamentos()`
- [ ] `test_valores_formatados_corretamente()`

### Testes de Integração
- [ ] `test_criar_contrato_gera_pdf()`
- [ ] `test_criar_contrato_gera_faturas()`
- [ ] `test_criar_contrato_12_parcelas_mensais()`
- [ ] `test_criar_contrato_desconto_aplicado()`
- [ ] `test_historico_registrado()`

### Testes Manuais
- [ ] Acessar `/contratos/novo`
- [ ] Preencher formulário completo
- [ ] Submeter contrato
- [ ] Verificar criação no BD
- [ ] Verificar geração de PDF
- [ ] Verificar faturas criadas (SQL)
- [ ] Download do PDF
- [ ] Validar conteúdo do PDF

---

## 🚀 Fase 10: Deploy

- [ ] Backup do banco de dados
- [ ] Executar migration: `alembic upgrade head`
- [ ] Testar criação de contrato
- [ ] Verificar geração de faturas
- [ ] Validar PDF gerado
- [ ] Testar assinatura digital
- [ ] Testar renovação automática
- [ ] Monitorar logs de erro

---

## 📈 Fase 11: Validação Final

- [ ] Formulário carrega corretamente
- [ ] Validações JavaScript funcionam
- [ ] Busca de cliente funciona
- [ ] Contrato criado com sucesso
- [ ] PDF gerado e acessível
- [ ] Faturas criadas no banco
- [ ] Histórico registrado
- [ ] Emails de confirmação (se configurado)
- [ ] Dashboard mostra novo contrato
- [ ] Relatórios funcionam

---

## 🎯 Fase 12: Pós-Implementação

### Monitoramento
- [ ] Logs de criação de contratos
- [ ] Quantidade de faturas por contrato
- [ ] Taxa de sucesso de geração de PDF
- [ ] Erros de validação do formulário

### Melhorias Futuras
- [ ] Dashboard visual de contratos
- [ ] Renovação automática com notificação
- [ ] Integração com email
- [ ] Integração com boleto/Pix
- [ ] Relatórios de receita
- [ ] Analytics de contratos

---

## 📋 Resumo por Componente

| Componente | Status | Arquivos |
|------------|--------|----------|
| **Migration** | ✅ Pronto | `0008_add_payment_fields_to_contratos.py` |
| **Modelo** | ✅ Pronto | `crm_modules/contratos/models.py` |
| **Schemas** | ✅ Pronto | `crm_modules/contratos/schemas.py` |
| **Interface** | ✅ Pronto | `novo_contrato.html` |
| **PDF Template** | ✅ Pronto | `contrato_profissional.html` |
| **Service** | ✅ Pronto | `crm_modules/contratos/service.py` |
| **Documentação** | ✅ Pronto | 3 arquivos .md |
| **Testes** | ⏳ Pendente | A fazer |
| **Deploy** | ⏳ Pendente | Aguardando execução |

---

## 🎬 Próximos Passos Imediatos

### 1. Executar Migration (IMPORTANTE!)
```bash
cd /caminho/do/projeto
alembic upgrade head
```

### 2. Testar Formulário
```
http://localhost:8001/contratos/novo
```

### 3. Criar Contrato de Teste
- Cliente: Selecionar um cliente existente
- Título: "Teste Contrato Profissional"
- Valor: 1000.00
- Desconto: 100.00
- Dia: 10
- Frequência: Mensal
- Submeter

### 4. Verificar Resultados
```sql
-- Verificar contrato criado
SELECT * FROM contratos WHERE titulo LIKE 'Teste%';

-- Verificar faturas geradas
SELECT * FROM faturas WHERE numero_fatura LIKE 'FAT-%';

-- Verificar histórico
SELECT * FROM contratos_historico WHERE contrato_id = ?;
```

### 5. Verificar PDF
```
http://localhost:8001/api/v1/contratos/{id}/pdf
```

---

## ⚠️ Observações Importantes

1. **Migration**: Deve ser executada ANTES de usar o sistema
2. **Frequência**: Padrão é mensal, customize conforme necessário
3. **PDF**: Usa template `contrato_profissional.html`, customize placeholders
4. **Faturas**: Auto-geradas, altere `_gerar_faturas_automaticas()` se necessário
5. **Desconto**: Aplicado no total, não por parcela

---

## 📞 Dúvidas?

- **Formulário**: Abrir `novo_contrato.html`
- **Lógica**: Abrir `ContratoService` em `service.py`
- **PDF**: Abrir `contrato_profissional.html`
- **Banco**: Ver `ContratoModel` em `models.py`

---

**Status Geral**: 🟢 **IMPLEMENTAÇÃO COMPLETA**

**Próximo**: Executar migration e testar sistema

---

Data: 23 de Janeiro de 2026  
Versão: 1.0
