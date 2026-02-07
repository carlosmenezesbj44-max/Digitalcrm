# 🔧 Corrigir Erro 404 - Carnês e Boletos

## ❌ Problema

```
[AUTH] Path: /carnes, Public: True
INFO: 127.0.0.1:53281 - "GET /carnes HTTP/1.1" 404 Not Found
```

A rota `/carnes` não é encontrada.

---

## ✅ Solução (3 passos)

### Passo 1️⃣: Parar a Aplicação

**No terminal onde a aplicação está rodando:**

Pressione: `Ctrl + C`

```
^CReceived signal: SIGINT (signal number: 2)
Shutting down
```

### Passo 2️⃣: Verificar que os Arquivos Existem

Execute no terminal:

```bash
# Verificar se os arquivos foram criados
dir interfaces\web\templates\carnes.html
dir interfaces\web\templates\boletos.html
```

**Esperado:**
```
18/01/2026  22:31            32.205 carnes.html
18/01/2026  22:32            33.239 boletos.html
```

### Passo 3️⃣: Reiniciar a Aplicação

```bash
# Opção 1: Python direto
python interfaces/api/main.py

# Opção 2: Uvicorn
uvicorn interfaces.api.main:app --reload

# Opção 3: Se usa poetry
poetry run python interfaces/api/main.py
```

**Esperado:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

---

## 🌐 Testar no Navegador

Após reiniciar, abra em uma **aba nova**:

### Carnês
```
http://localhost:8000/carnes
```

### Boletos
```
http://localhost:8000/boletos
```

---

## ✨ Esperado

Você deve ver:

**Página de Carnês:**
- ✅ Menu azul no lado esquerdo
- ✅ Título "Carnês"
- ✅ Botão azul "+ Novo Carnê"
- ✅ Tabela com carnês (vazia no início)
- ✅ Resumo com totais

**Página de Boletos:**
- ✅ Menu azul no lado esquerdo
- ✅ Título "Boletos"
- ✅ Botão azul "+ Novo Boleto"
- ✅ Abas: Tabela / Cards
- ✅ Resumo com totais

---

## 🐛 Se Ainda Não Funcionar

### Erro: Template não encontrado

**Mensagem:**
```
⚠️ Erro 404
Página de carnês não encontrada.
Arquivo esperado em: ...
```

**Solução:**
1. Verifique o caminho exato:
   ```bash
   cd interfaces/web/templates
   dir *.html
   ```

2. Se faltarem, execute novamente a criação:
   ```python
   # Copie o conteúdo de carnes.html e boletos.html
   # E crie os arquivos manualmente
   ```

### Erro: Módulo não encontrado

**Mensagem:**
```
ModuleNotFoundError: No module named 'crm_modules.faturamento.carne_api'
```

**Solução:**
1. Adicione ao `main.py`:
   ```python
   from crm_modules.faturamento.carne_api import router as carne_router
   app.include_router(carne_router)
   ```

2. Reinicie a aplicação

### Erro: Porta em uso

**Mensagem:**
```
OSError: [Errno 48] Address already in use
```

**Solução:**

**Windows:**
```bash
# Matar processo na porta 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Ou use porta diferente
uvicorn interfaces.api.main:app --port 8001
```

**Mac/Linux:**
```bash
# Matar processo na porta 8000
lsof -ti:8000 | xargs kill -9

# Ou use porta diferente
uvicorn interfaces.api.main:app --port 8001
```

---

## ✅ Checklist de Verificação

- [ ] Aplicação foi **parada** (Ctrl+C)
- [ ] Aplicação foi **reiniciada**
- [ ] Arquivos `carnes.html` e `boletos.html` **existem**
- [ ] `main.py` tem as rotas `@app.get("/carnes")` e `@app.get("/boletos")`
- [ ] Porta 8000 está **disponível**
- [ ] Navegador foi **recarregado** (F5)
- [ ] Abas **antigas** foram fechadas
- [ ] Nenhuma outra app usa a porta 8000

---

## 📝 Resumo

**O erro 404 ocorre porque:**
- Aplicação não foi reiniciada após adicionar as rotas

**Para resolver:**
1. `Ctrl + C` para parar
2. `python interfaces/api/main.py` para reiniciar
3. Acesse `http://localhost:8000/carnes`

**Tão simples quanto isso!** 🚀

---

Se ainda tiver problemas, verifique em:
- `COMO_USAR_CARNES_BOLETOS_UI.md` - Como usar
- `CHECKLIST_SETUP_CARNES_BOLETOS.md` - Setup completo
- `FAQ_CARNES_BOLETOS.md` - Perguntas frequentes
