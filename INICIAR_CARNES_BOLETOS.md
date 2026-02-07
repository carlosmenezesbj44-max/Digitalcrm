# 🚀 Iniciar Sistema de Carnês e Boletos

## ⚡ Jeito Mais Rápido (2 cliques)

### Windows

**Opção 1: Clique duplo no arquivo**
```
REINICIAR_APP.bat
```

Isto vai:
1. ✅ Parar a aplicação anterior
2. ✅ Reiniciar com as novas rotas
3. ✅ Mostrar mensagem de sucesso

**Depois acesse:**
- `http://localhost:8000/carnes`
- `http://localhost:8000/boletos`

---

## 🖥️ Jeito Manual (5 linhas de comando)

### Windows (CMD)

```bash
# 1. Parar o processo anterior
netstat -ano | findstr :8000
taskkill /PID <numero_do_PID> /F

# 2. Ir para a pasta
cd "C:\Users\menezes\OneDrive\Documentos\DigitalcodeCRM\crm_provedor"

# 3. Iniciar
python interfaces/api/main.py
```

### Mac/Linux

```bash
# 1. Parar o processo
lsof -ti:8000 | xargs kill -9

# 2. Ir para a pasta
cd ~/DigitalcodeCRM/crm_provedor

# 3. Iniciar
python interfaces/api/main.py
```

### PowerShell (Windows)

```powershell
# Executar script
.\REINICIAR_APP.ps1
```

---

## ✅ Confirmar que Funcionou

Você deve ver no terminal:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

Depois abra no navegador:

```
http://localhost:8000/carnes
```

Deve mostrar página com:
- ✓ Menu azul esquerda
- ✓ Botão "+ Novo Carnê"
- ✓ Tabela vazia
- ✓ Resumo com totais

---

## 🎯 Próximos Passos

Agora que está rodando:

1. **Criar Carnê:**
   - Clique "+ Novo Carnê"
   - Preencha dados
   - Clique "Criar"

2. **Criar Boleto:**
   - Vá para `/boletos`
   - Clique "+ Novo Boleto"
   - Preencha dados
   - Clique "Gerar"

3. **Ver Parcelas:**
   - Clique "Ver Parcelas" em um carnê
   - Lista apareça com detalhes

---

## 🆘 Erro: Porta 8000 em uso?

**Windows:**
```bash
# Ver qual processo usa porta 8000
netstat -ano | findstr :8000

# Matar processo (substitua PID)
taskkill /PID 1234 /F
```

**Mac/Linux:**
```bash
# Matar processo na porta 8000
lsof -ti:8000 | xargs kill -9
```

Ou use porta diferente:
```bash
uvicorn interfaces.api.main:app --port 8001
```

---

## 📊 Se Tiver Problemas

**Leia um destes arquivos:**

1. `CORRIGIR_ERRO_404_CARNES_BOLETOS.md` - Se página não carregar
2. `COMO_USAR_CARNES_BOLETOS_UI.md` - Como usar
3. `CHECKLIST_SETUP_CARNES_BOLETOS.md` - Setup completo
4. `FAQ_CARNES_BOLETOS.md` - Perguntas frequentes

---

## 📝 Resumo

| Ação | Comando |
|------|---------|
| **Parar** | Ctrl+C no terminal |
| **Iniciar** | `python interfaces/api/main.py` |
| **Rápido (Windows)** | Duplo-clique em `REINICIAR_APP.bat` |
| **PowerShell** | `.\REINICIAR_APP.ps1` |

---

## 🎉 Está Pronto!

Agora você pode:

✅ Criar carnês (planos de pagamento)  
✅ Gerar boletos (com código de barras)  
✅ Registrar pagamentos  
✅ Sincronizar com Gerencianet  

Sem escrever uma linha de código!

---

**Acesse agora:**
```
http://localhost:8000/carnes
http://localhost:8000/boletos
```

