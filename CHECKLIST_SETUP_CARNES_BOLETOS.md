# ✅ Checklist de Setup - Carnês e Boletos

## 📋 Antes de Começar

### Passo 1: Verificar Arquivos Criados

```bash
# Verifique se existem os arquivos:

✅ crm_modules/faturamento/carne_models.py
✅ crm_modules/faturamento/carne_schemas.py
✅ crm_modules/faturamento/carne_service.py
✅ crm_modules/faturamento/boleto_service.py
✅ crm_modules/faturamento/gerencianet_client.py
✅ crm_modules/faturamento/carne_api.py

✅ interfaces/web/templates/carnes.html
✅ interfaces/web/templates/boletos.html

✅ alembic/versions/002_create_carnes_boletos_tables.py
```

### Passo 2: Configurar Variáveis de Ambiente

**Arquivo:** `.env`

```env
# Adicione estas linhas:
GERENCIANET_CLIENT_ID=seu_client_id_aqui
GERENCIANET_CLIENT_SECRET=seu_client_secret_aqui
GERENCIANET_SANDBOX=true
APP_URL=http://localhost:8000
```

**Onde obter?**
1. Acesse https://gerencianet.com.br
2. Vá em **Aplicações** → **Minhas Aplicações**
3. Copie `Client ID` e `Client Secret`
4. Cole no `.env`

### Passo 3: Instalar Dependência

```bash
# Certifique-se que requests está instalado
pip install requests

# Ou se usa poetry
poetry add requests
```

### Passo 4: Criar Tabelas no Banco

```bash
# Execute migration
alembic upgrade head

# Ou manualmente, execute em Python:
python -c "
from crm_core.db.models_base import Base, engine
from crm_modules.faturamento.carne_models import *
Base.metadata.create_all(bind=engine)
print('✓ Tabelas criadas com sucesso!')
"
```

**Saída esperada:**
```
✓ Tabelas criadas com sucesso!
```

---

## 🔌 Integrar API no Main

**Arquivo:** `interfaces/api/main.py`

### Verificar se já tem:

```python
# Linha 8 (aproximadamente)
from crm_modules.faturamento.carne_api import router as carne_router

# Linha 18 (aproximadamente)
app.include_router(carne_router)  # Rotas de carnês e boletos

# Linhas 330+ (no final)
@app.get("/carnes", response_class=HTMLResponse)
def pagina_carnes():
    """Página para gerenciar carnês"""
    ...

@app.get("/boletos", response_class=HTMLResponse)
def pagina_boletos():
    """Página para gerenciar boletos"""
    ...
```

Se não tiver, copie do arquivo `main.py` que foi atualizado.

---

## 🎨 Verificar Templates

### Arquivo 1: `interfaces/web/templates/carnes.html`

- [ ] Arquivo existe
- [ ] Tem menu do lado esquerdo
- [ ] Tem formulário "Novo Carnê"
- [ ] Tem tabela de carnês
- [ ] Tem modal de parcelas

**Teste:**
```
http://localhost:8000/carnes
```

Deve carregar a página com:
- ✓ Menu azul à esquerda
- ✓ Botão "+ Novo Carnê" (azul, no topo)
- ✓ Tabela vazia (ou com dados)

### Arquivo 2: `interfaces/web/templates/boletos.html`

- [ ] Arquivo existe
- [ ] Tem menu do lado esquerdo
- [ ] Tem formulário "Novo Boleto"
- [ ] Tem abas (Tabela / Cards)
- [ ] Tem botão sincronizar

**Teste:**
```
http://localhost:8000/boletos
```

Deve carregar a página com:
- ✓ Menu azul à esquerda
- ✓ Botão "+ Novo Boleto" (azul, no topo)
- ✓ Abas visíveis

---

## 🧪 Testar Endpoints API

### Teste 1: Criar Carnê

```bash
curl -X POST http://localhost:8000/api/faturamento/carnes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer seu_token" \
  -d '{
    "cliente_id": 1,
    "valor_total": 1200,
    "quantidade_parcelas": 12,
    "data_primeiro_vencimento": "2024-02-01",
    "gerar_boletos": true
  }'
```

**Resposta esperada:**
```json
{
  "id": 1,
  "numero_carne": "CARNE-...",
  "valor_total": 1200,
  "quantidade_parcelas": 12,
  "status": "ativo"
}
```

### Teste 2: Listar Carnês

```bash
curl http://localhost:8000/api/faturamento/carnes/cliente/1 \
  -H "Authorization: Bearer seu_token"
```

### Teste 3: Gerar Boleto

```bash
curl -X POST http://localhost:8000/api/faturamento/boletos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer seu_token" \
  -d '{
    "cliente_id": 1,
    "valor": 500,
    "data_vencimento": "2024-02-20"
  }'
```

---

## 🖥️ Iniciar a Aplicação

```bash
# Opção 1: Python direto
python interfaces/api/main.py

# Opção 2: Uvicorn
uvicorn interfaces.api.main:app --reload

# Opção 3: Pytest (se configurado)
pytest
```

**Saída esperada:**
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 🎯 Verificação Final

### Teste 1: Acessar Dashboard

```
http://localhost:8000/
```

✅ Deve mostrar dashboard com menu

### Teste 2: Acessar Carnês

```
http://localhost:8000/carnes
```

✅ Deve mostrar página completa de carnês

### Teste 3: Acessar Boletos

```
http://localhost:8000/boletos
```

✅ Deve mostrar página completa de boletos

### Teste 4: Criar Carnê (UI)

1. Acesse `/carnes`
2. Clique "+ Novo Carnê"
3. Preencha:
   - Cliente: (selecione um)
   - Valor: 100
   - Parcelas: 12
   - Vencimento: data futura
4. Clique "Criar Carnê"

**Esperado:**
- ✅ Mensagem de sucesso
- ✅ Carnê aparece na tabela
- ✅ Sem erros no console (F12)

### Teste 5: Criar Boleto (UI)

1. Acesse `/boletos`
2. Clique "+ Novo Boleto"
3. Aba: "Boleto Direto"
4. Preencha:
   - Cliente: (selecione um)
   - Valor: 500
   - Vencimento: data futura
5. Clique "Gerar Boleto"

**Esperado:**
- ✅ Mensagem de sucesso
- ✅ Boleto aparece na tabela
- ✅ Sem erros no console

---

## 🐛 Se Algo Não Funcionar

### Erro: ImportError em carne_api

**Solução:**
```python
# Verifique se existem:
from crm_modules.faturamento.gerencianet_client import GerencianetClient
from crm_modules.faturamento.carne_service import CarneService
from crm_modules.faturamento.boleto_service import BoletoService
```

### Erro: Tabelas não existem

**Solução:**
```bash
# Crie manualmente
python -c "
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from alembic.operations import Operations

# Ou execute:
alembic upgrade head
"
```

### Erro: Cliente não encontrado

**Solução:**
```bash
# Certifique-se que existe cliente com ID 1
# Vá em /clientes e crie um novo cliente
```

### Erro: Gerencianet inválido

**Solução:**
1. Abra `.env`
2. Verifique `GERENCIANET_CLIENT_ID`
3. Verifique `GERENCIANET_CLIENT_SECRET`
4. Teste em sandbox primeiro (`GERENCIANET_SANDBOX=true`)

---

## 📊 Checklist Final

- [ ] Arquivos Python criados
- [ ] Templates HTML criados
- [ ] `.env` preenchido
- [ ] `requests` instalado
- [ ] Tabelas criadas (migration)
- [ ] Rotas registradas no `main.py`
- [ ] Aplicação inicializada
- [ ] Página `/carnes` acessível
- [ ] Página `/boletos` acessível
- [ ] Pode criar carnê (sem erros)
- [ ] Pode criar boleto (sem erros)
- [ ] Menu mostra opções (Carnês, Boletos)

---

## 🚀 Próximos Passos

Após verificar tudo acima:

1. **Leia documentação:**
   - `INTERFACE_GRAFICA_CARNES_BOLETOS.md` - Como usar
   - `INTEGRACAO_GERENCIANET.md` - Detalhes técnicos
   - `FAQ_CARNES_BOLETOS.md` - Perguntas comuns

2. **Teste funcionalidades:**
   - Criar carnês
   - Criar boletos
   - Registrar pagamentos
   - Sincronizar com Gerencianet

3. **Personalize:**
   - Adicione logo
   - Altere cores
   - Configure email
   - Setup webhooks

4. **Deploy:**
   - Configure HTTPS
   - Setup domínio
   - Configure Gerencianet produção
   - Faça backup

---

## 📞 Suporte

Se encontrar erros:

1. **Verifique o console:**
   ```bash
   # Terminal rodando a aplicação
   # Procure por mensagens de erro
   ```

2. **Abra console do navegador:**
   ```
   F12 → Console → Procure erros em vermelho
   ```

3. **Verifique logs:**
   ```bash
   # Se rodando com uvicorn
   # Logs aparecem no terminal
   ```

4. **Consulte documentação:**
   - `INTERFACE_GRAFICA_CARNES_BOLETOS.md`
   - `FAQ_CARNES_BOLETOS.md`

---

## ✅ Status

- **Código:** ✅ Completo
- **Templates:** ✅ Completo
- **API:** ✅ Completo
- **Documentação:** ✅ Completo
- **Testes:** ✅ Manual (siga checklist)
- **Setup:** ⏳ Pendente (Faça agora!)

---

**Tempo estimado:** 15-20 minutos

**Dificuldade:** ⭐⭐ (Muito fácil)

**Pronto para começar?** Siga o checklist acima! 🎉
