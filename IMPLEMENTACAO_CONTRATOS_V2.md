# Implementação Completa - Módulo de Contratos v2

**Data**: Janeiro 2026  
**Status**: ✅ Implementado - Fase 1 (Melhorias Críticas)

---

## 📋 O que foi implementado

### 1. **Expansão do Modelo de Dados** ✅

#### Novos campos adicionados ao `ContratoModel`:

```python
# Tipo e categorização
tipo_contrato: TipoContrato          # servico, assinatura, manutencao, suporte, outro
status_renovacao: StatusRenovacao    # nao_renovavel, renovacao_automatica, renovacao_manual, expirado

# Datas críticas
data_vigencia_inicio: DateTime        # Quando começa a valer
data_vigencia_fim: DateTime           # Quando expira
data_notificacao_renovacao: DateTime  # Data para avisar renovação

# Financeiro
valor_contrato: Float                 # Valor total
moeda: String                         # Moeda (BRL, USD, EUR, etc)

# Assinatura e informações adicionais
assinado_por: String                  # Nome de quem assinou
proximo_contrato_id: Integer          # Referência para renovação

# Auditoria completa
criado_por: String                    # Quem criou
criado_em: DateTime                   # Quando criou
atualizado_por: String                # Quem atualizou
atualizado_em: DateTime               # Quando atualizou
deletado_em: DateTime                 # Soft delete
```

#### Nova tabela `ContratoHistoricoModel`:

```python
# Rastreamento completo de alterações
campo_alterado: String                # Qual campo mudou
valor_anterior: String                # Valor antes
valor_novo: String                    # Valor depois
alterado_por: String                  # Quem mudou
alterado_em: DateTime                 # Quando mudou
motivo: String                        # Por que mudou
ip_address: String                    # IP de quem fez
user_agent: String                    # Cliente HTTP
```

### 2. **Gerador de PDF Profissional** ✅

**Arquivo**: `crm_modules/contratos/pdf_generator.py`

Gera PDFs profissionais com:
- ✅ Cabeçalho com logo e ID do contrato
- ✅ Dados completos do cliente (nome, CNPJ/CPF, email)
- ✅ Tipo e status do contrato com cores
- ✅ Datas de vigência e duração calculada
- ✅ Informações financeiras com valor formatado
- ✅ Informações de renovação
- ✅ Área de assinatura para impressão
- ✅ Rodapé com referência e data de geração
- ✅ Formatação profissional com ReportLab

**Uso**:
```python
from crm_modules.contratos.pdf_generator import ContratosPDFGenerator

generator = ContratosPDFGenerator(contrato_model)
pdf_bytes = generator.gerar_pdf()
```

### 3. **Service Melhorado com Auditoria** ✅

**Arquivo**: `crm_modules/contratos/service.py`

Novas funcionalidades:

#### a) Criação com PDF automático
```python
def criar_contrato(self, contrato_data: ContratoCreate, usuario_id: str = None) -> Contrato:
    # Cria contrato + gera PDF automaticamente
    # Registra no histórico
    # Atualiza status do cliente
```

#### b) Assinatura com auditoria
```python
def assinar_contrato(self, contrato_id: int, assinatura_base64: str, 
                    hash_documento: str, usuario_id: str = None, 
                    nome_signatario: str = None) -> Contrato:
    # Assina contrato
    # Valida hash do documento
    # Salva assinatura em arquivo
    # Registra quem assinou, quando e por que
```

#### c) Liberação com rastreamento
```python
def liberar_contrato(self, contrato_id: int, usuario_id: str = None, 
                    motivo: str = None) -> Contrato:
    # Libera contrato
    # Registra motivo da liberação
    # Rastreia quem liberou
    # Atualiza status do cliente
```

#### d) Histórico completo
```python
def obter_historico(self, contrato_id: int) -> list:
    # Retorna todas as alterações do contrato
    # Com quem, quando e por que cada mudança
```

#### e) Monitoramento de vencimento
```python
def verificar_contratos_vencendo(self, dias: int = 30) -> List[Contrato]:
    # Lista contratos que vencem em X dias

def verificar_contratos_vencidos(self) -> List[Contrato]:
    # Lista contratos já vencidos
```

#### f) Renovação automática
```python
def renovar_contrato_automatico(self, contrato_id: int, usuario_id: str = None) -> Contrato:
    # Renova contrato automaticamente
    # Vincula novo ao anterior
    # Registra no histórico
```

### 4. **Repositório Expandido** ✅

**Arquivo**: `crm_modules/contratos/repository.py`

Novos métodos:

```python
# Buscas avançadas
def get_contratos_vencendo(self, dias: int = 30) -> List[ContratoModel]
def get_contratos_vencidos(self) -> List[ContratoModel]

# Soft delete
def soft_delete(self, contrato_id: int)

# Histórico
class ContratoHistoricoRepository:
    def get_historico_contrato(self, contrato_id: int)
    def registrar_alteracao(self, contrato_id, campo, valor_anterior, valor_novo, usuario_id, motivo)
```

### 5. **Schemas Expandidos** ✅

**Arquivo**: `crm_modules/contratos/schemas.py`

Novos schemas:

```python
# Enums
class TipoContrato(str, enum.Enum)
class StatusRenovacao(str, enum.Enum)

# Schemas
class ContratoCreate:
    # Inclui todos os novos campos
    incluir_pdf: bool = True

class ContratoResponse:
    # Retorna informações de auditoria
    criado_por, atualizado_por, atualizado_em

class ContratoHistoricoResponse:
    # Novo schema para histórico
    campo_alterado, valor_anterior, valor_novo, alterado_por, etc
```

### 6. **API Profissional** ✅

**Arquivo**: `crm_modules/contratos/api.py`

Novos endpoints:

```
GET    /api/v1/contratos                      # Lista todos (com paginação)
POST   /api/v1/contratos                      # Cria novo
GET    /api/v1/contratos/{id}                 # Obtém detalhes
GET    /api/v1/contratos/cliente/{id}         # Lista do cliente
GET    /api/v1/contratos/{id}/historico       # Histórico completo

POST   /api/v1/contratos/{id}/assinar         # Assina contrato
POST   /api/v1/contratos/{id}/liberar         # Libera contrato
POST   /api/v1/contratos/{id}/renovar         # Renova contrato

GET    /api/v1/contratos/vencendo/lista       # Contratos vencendo
GET    /api/v1/contratos/vencidos/lista       # Contratos vencidos
```

**Melhorias**:
- ✅ Tratamento de erros detalhado
- ✅ Paginação para listas
- ✅ Validação de permissões
- ✅ Rastreamento de auditoria
- ✅ Respostas padronizadas

### 7. **Script de Migração** ✅

**Arquivo**: `scripts/migrate_contratos_v2.py`

Migra automaticamente:
- Adiciona novos campos à tabela existente
- Cria tabela de histórico
- Verifica integridade dos dados

```bash
python scripts/migrate_contratos_v2.py
```

---

## 🚀 Como usar

### Instalação

1. **Instalar dependências**:
```bash
pip install reportlab
```

2. **Executar migração**:
```bash
python scripts/migrate_contratos_v2.py
```

### Exemplos de uso

#### Criar contrato com PDF
```python
from crm_modules.contratos.schemas import ContratoCreate, TipoContrato, StatusRenovacao
from datetime import datetime, timedelta

contrato_data = ContratoCreate(
    cliente_id=1,
    titulo="Contrato de Serviço de Internet",
    descricao="Plano Premium com 100Mbps",
    tipo_contrato=TipoContrato.SERVICO,
    data_vigencia_inicio=datetime.now(),
    data_vigencia_fim=datetime.now() + timedelta(days=365),
    valor_contrato=99.90,
    moeda="BRL",
    status_renovacao=StatusRenovacao.RENOVACAO_MANUAL,
    incluir_pdf=True  # Gera PDF automaticamente
)

service = ContratoService(repository_session=db, usuario_id="admin_123")
contrato = service.criar_contrato(contrato_data, usuario_id="admin_123")
# PDF foi gerado em: interfaces/web/static/contratos/contrato_1_1.pdf
```

#### Assinar contrato
```python
contrato_assinado = service.assinar_contrato(
    contrato_id=1,
    assinatura_base64="iVBORw0KGgoAAAANS...",  # imagem da assinatura
    hash_documento="abc123def456...",
    usuario_id="cliente_456",
    nome_signatario="João Silva"
)
# Histórico registrado automaticamente
```

#### Liberar contrato
```python
contrato_liberado = service.liberar_contrato(
    contrato_id=1,
    usuario_id="admin_123",
    motivo="Documentação verificada e aceita"
)
# Auditoria registrada
```

#### Obter histórico
```python
historico = service.obter_historico(contrato_id=1)
# Retorna lista com todas as alterações:
# [
#   {
#     "campo_alterado": "status_assinatura",
#     "valor_anterior": "aguardando",
#     "valor_novo": "assinado",
#     "alterado_por": "cliente_456",
#     "alterado_em": "2026-01-19T14:30:00",
#     "motivo": "Contrato assinado digitalmente por João Silva"
#   },
#   ...
# ]
```

#### Monitorar contratos vencendo
```python
contratos_vencendo = service.verificar_contratos_vencendo(dias=30)
# Lista contratos que vencem nos próximos 30 dias

contratos_vencidos = service.verificar_contratos_vencidos()
# Lista contratos que já venceram
```

#### Renovar contrato
```python
novo_contrato = service.renovar_contrato_automatico(
    contrato_id=1,
    usuario_id="sistema"
)
# Cria novo contrato com datas atualizadas
# Vincula ao contrato anterior
# Registra no histórico
```

---

## 📊 Estrutura de arquivos criados/modificados

```
crm_modules/contratos/
├── models.py                    (MODIFICADO - adicionados campos)
├── schemas.py                   (MODIFICADO - novos enums e schemas)
├── repository.py                (MODIFICADO - novos métodos de busca)
├── service.py                   (MODIFICADO - auditoria e PDF)
├── api.py                       (MODIFICADO - novos endpoints)
├── pdf_generator.py             (NOVO - gerador de PDF)
└── domain.py                    (sem alterações)

scripts/
└── migrate_contratos_v2.py      (NOVO - script de migração)

documentation/
├── ANALISE_CONTRATOS_PROFISSIONAL.md       (guia completo de análise)
└── IMPLEMENTACAO_CONTRATOS_V2.md           (este arquivo)
```

---

## 🔒 Segurança implementada

✅ **Auditoria completa**: Cada ação registra quem, quando, onde e por que  
✅ **Soft delete**: Contratos deletados não são removidos, apenas marcados  
✅ **Validação de hash**: Detecta alterações não autorizadas  
✅ **Controle de permissão**: Apenas admins podem liberar  
✅ **Rastreamento de IP**: Grava IP de quem fez cada ação  
✅ **Histórico imutável**: Alterações passadas não podem ser mudadas  

---

## ⚠️ Próximas melhorias (Fase 2)

- [ ] Interface web para criar/visualizar contratos
- [ ] Assinatura digital real (DocuSign/Clicksign)
- [ ] Notificações por email
- [ ] Dashboard com métricas
- [ ] Bulk actions
- [ ] Filtros e busca avançada
- [ ] Relatórios exportáveis
- [ ] Integração com pagamentos
- [ ] Renovação automática com cobrança
- [ ] Templates customizáveis

---

## 🧪 Testando

### Testar geração de PDF
```python
from crm_modules.contratos.pdf_generator import ContratosPDFGenerator
from crm_modules.contratos.models import ContratoModel

# Assumindo que existe um contrato no BD
contrato = session.query(ContratoModel).first()
generator = ContratosPDFGenerator(contrato)
pdf_bytes = generator.gerar_pdf()

# Salvar arquivo para visualizar
with open('/tmp/test.pdf', 'wb') as f:
    f.write(pdf_bytes)
```

### Testar via API
```bash
# Criar contrato
curl -X POST http://localhost:8000/api/v1/contratos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "cliente_id": 1,
    "titulo": "Test Contract",
    "tipo_contrato": "servico",
    "data_vigencia_inicio": "2026-01-20",
    "data_vigencia_fim": "2027-01-20",
    "valor_contrato": 100.00,
    "incluir_pdf": true
  }'

# Obter histórico
curl http://localhost:8000/api/v1/contratos/1/historico \
  -H "Authorization: Bearer TOKEN"

# Listar vencendo
curl "http://localhost:8000/api/v1/contratos/vencendo/lista?dias=30" \
  -H "Authorization: Bearer TOKEN"
```

---

## 📈 Impacto

| Aspecto | Antes | Depois |
|---------|-------|--------|
| **Auditoria** | ❌ Nenhuma | ✅ Completa com histórico |
| **PDF** | ❌ Simulado | ✅ Profissional com ReportLab |
| **Datas** | ⚠️ Básicas | ✅ Vigência, renovação, notificação |
| **Segurança** | ⚠️ Limitada | ✅ Hash, IP, rastreamento |
| **Monitoramento** | ❌ Manual | ✅ Automático (vencendo, vencido) |
| **Renovação** | ❌ Manual | ✅ Automática com rastreamento |
| **Conformidade** | ⚠️ Parcial | ✅ Rastreabilidade completa |

---

## 📝 Notas

- ReportLab foi escolhido por ser puro Python e sem dependências externas pesadas
- SQLite oferece soft delete simples, em produção considere usar um flag booleano
- Os PDFs são salvos em `interfaces/web/static/contratos/`
- As assinaturas são salvas em `interfaces/web/static/assinaturas/`
- Histórico é imutável e nunca é deletado (importante para auditoria)

---

## ✅ Checklist de implementação

- [x] Expandir modelo de dados
- [x] Criar tabela de histórico
- [x] Implementar gerador de PDF
- [x] Melhorar service com auditoria
- [x] Adicionar novos endpoints
- [x] Expandir schemas
- [x] Criar script de migração
- [x] Documentação completa
- [ ] Testar em produção
- [ ] Implementar interface web (próxima fase)

---

Desenvolvido em: **Janeiro 2026**  
Versão: **2.0**  
Status: **Pronto para produção**
