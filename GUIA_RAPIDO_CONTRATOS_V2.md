# Guia Rápido - Contratos v2

## 🚀 Começar em 5 minutos

### 1️⃣ Instalar dependência
```bash
pip install reportlab==4.0.9
```

### 2️⃣ Executar migração
```bash
cd c:\Users\menezes\OneDrive\Documentos\DigitalcodeCRM\crm_provedor
python scripts/migrate_contratos_v2.py
```

Você verá:
```
============================================================
MIGRAÇÃO DE CONTRATOS - Versão 2
============================================================
✓ Tabela 'contratos' já existe. Verificando campos...
  - Adicionando campo 'tipo_contrato' (VARCHAR)...
    ✓ Campo 'tipo_contrato' adicionado
  ...
✓ Tabela 'contratos_historico' criada com sucesso!

============================================================
MIGRAÇÃO CONCLUÍDA COM SUCESSO!
============================================================
```

### 3️⃣ Testar criação de contrato

**Via API**:
```bash
curl -X POST http://localhost:8000/api/v1/contratos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -d '{
    "cliente_id": 1,
    "titulo": "Contrato de Serviço",
    "descricao": "Serviço mensal",
    "tipo_contrato": "servico",
    "data_vigencia_inicio": "2026-01-20",
    "data_vigencia_fim": "2027-01-20",
    "valor_contrato": 150.00,
    "moeda": "BRL",
    "status_renovacao": "renovacao_manual",
    "incluir_pdf": true
  }'
```

**Via código Python**:
```python
from crm_modules.contratos.service import ContratoService
from crm_modules.contratos.schemas import ContratoCreate, TipoContrato, StatusRenovacao
from datetime import datetime, timedelta
from interfaces.api.dependencies import get_db

# Obter sessão do BD
db = next(get_db())

# Criar dados
contrato_data = ContratoCreate(
    cliente_id=1,
    titulo="Contrato Teste",
    tipo_contrato=TipoContrato.SERVICO,
    data_vigencia_inicio=datetime.now(),
    data_vigencia_fim=datetime.now() + timedelta(days=365),
    valor_contrato=99.90,
    incluir_pdf=True
)

# Criar contrato
service = ContratoService(repository_session=db, usuario_id="admin_001")
contrato = service.criar_contrato(contrato_data, usuario_id="admin_001")

print(f"✓ Contrato criado com ID: {contrato.id}")
print(f"✓ PDF gerado em: {contrato.arquivo_contrato}")
```

---

## 📋 Principais recursos agora disponíveis

### ✅ PDF Profissional
- PDF é gerado automaticamente ao criar contrato
- Salvo em: `interfaces/web/static/contratos/`

### ✅ Auditoria Completa
Todas as ações registram:
- Quem fez (usuário)
- Quando fez (data/hora)
- O que fez (mudança específica)
- Por que fez (motivo)

Exemplo de histórico:
```python
historico = service.obter_historico(contrato_id=1)
# [
#   {
#     "campo_alterado": "status_assinatura",
#     "valor_anterior": "aguardando",
#     "valor_novo": "assinado",
#     "alterado_por": "cliente_123",
#     "alterado_em": "2026-01-20T10:30:00",
#     "motivo": "Contrato assinado digitalmente por João Silva"
#   }
# ]
```

### ✅ Monitoramento de Contratos
```python
# Contratos vencendo em 30 dias
vencendo = service.verificar_contratos_vencendo(dias=30)

# Contratos já vencidos
vencidos = service.verificar_contratos_vencidos()

# Renovar automático
novo = service.renovar_contrato_automatico(contrato_id=1)
```

---

## 🎯 Fluxos principais

### Fluxo 1: Criar → Assinar → Liberar

```
1. Criar contrato
   POST /api/v1/contratos
   ↓ (PDF gerado automaticamente)
   
2. Cliente assina
   POST /api/v1/contratos/{id}/assinar
   ↓ (Histórico registra)
   
3. Admin libera
   POST /api/v1/contratos/{id}/liberar?motivo="Doc verificada"
   ↓ (Status muda para "liberado")
   
4. Visualizar histórico
   GET /api/v1/contratos/{id}/historico
```

### Fluxo 2: Monitorar Vencimentos

```
1. Verificar contratos vencendo
   GET /api/v1/contratos/vencendo/lista?dias=30
   
2. Renovar contrato
   POST /api/v1/contratos/{id}/renovar
   
3. Novo contrato criado com datas atualizadas
   Vinculado ao contrato anterior
```

---

## 📁 Arquivos criados/modificados

**Criados**:
- `crm_modules/contratos/pdf_generator.py` - Gerador de PDF
- `scripts/migrate_contratos_v2.py` - Script de migração
- `ANALISE_CONTRATOS_PROFISSIONAL.md` - Análise completa
- `IMPLEMENTACAO_CONTRATOS_V2.md` - Documentação técnica
- `requirements_contratos.txt` - Dependências

**Modificados**:
- `crm_modules/contratos/models.py` - Novos campos
- `crm_modules/contratos/schemas.py` - Novos enums
- `crm_modules/contratos/repository.py` - Novos métodos
- `crm_modules/contratos/service.py` - Auditoria e PDF
- `crm_modules/contratos/api.py` - Novos endpoints

---

## 🔍 Verificar migração

```bash
# Abrir banco de dados
sqlite3 crm.db

# Ver estrutura da tabela contratos
.schema contratos

# Ver se tabela de histórico existe
SELECT name FROM sqlite_master WHERE type='table' AND name='contratos_historico';

# Ver exemplos de histórico
SELECT * FROM contratos_historico LIMIT 5;
```

---

## 🐛 Troubleshooting

**Erro: "No module named 'reportlab'"**
```bash
pip install reportlab==4.0.9
```

**Erro: "Base de dados bloqueada"**
- Feche outros programas usando o banco
- Reinicie o servidor FastAPI

**PDF não gerado**
- Verifique pasta `interfaces/web/static/contratos/` existe
- Verifique permissões de escrita

---

## 💡 Próximas etapas

1. **Fase 2 - Interface Web**:
   - Formulário para criar contratos
   - Visualizar PDF no navegador
   - Timeline de histórico

2. **Fase 3 - Automação**:
   - Email ao cliente quando contrato criado
   - Alerta 7 dias antes de vencer
   - Renovação automática com cobrança

3. **Fase 4 - Integrações**:
   - Assinatura digital real (DocuSign)
   - Integração com gateway de pagamento
   - Webhooks para eventos

---

## 📞 Suporte

Documentos de referência:
- `ANALISE_CONTRATOS_PROFISSIONAL.md` - Análise detalhada
- `IMPLEMENTACAO_CONTRATOS_V2.md` - Documentação técnica completa
- Código comentado em `crm_modules/contratos/`

---

**Versão**: 2.0  
**Data**: Janeiro 2026  
**Status**: ✅ Pronto para usar
