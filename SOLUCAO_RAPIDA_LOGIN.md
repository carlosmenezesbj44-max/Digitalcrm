# ⚡ Solução Rápida: Problema de Login

## Teste Rápido (2 minutos)

### 1. Abra o Console (F12)

Pressione **F12** e clique na aba **Console**

### 2. Cole Este Código

```javascript
// Limpar tudo
localStorage.clear();
sessionStorage.clear();
console.log('✅ Cache limpo');

// Verificar localStorage
console.log('localStorage vazio?', localStorage.length === 0);
```

### 3. Recarregue a Página

```
Ctrl + F5 (reload completo)
```

### 4. Faça Login Novamente

Coloque seu usuário e senha e clique em Login

### 5. Observe o Console

Você deve ver:
```
[LOGIN] Token recebido: eyJ...
[LOGIN] Token salvo em localStorage
[LOGIN] Token em localStorage: eyJ...
```

### 6. Teste o Fluxo

1. **Você foi redirecionado para /dashboard?** ✅ Bom!
2. **Clique em um item do menu** (ex: "Novo Cliente")
3. **Página carrega?** ✅ Bom!
4. **Clique em "Home"**
5. **Dashboard carrega?** ✅ **PROBLEMA RESOLVIDO!**

---

## Se Não Funcionar

### Opção A: Reiniciar Servidor

Se tudo parece certo mas continua redirecionando:

```bash
# No terminal onde roda o servidor:
Ctrl + C

# Depois:
python -m uvicorn interfaces.web.app:app --reload
```

### Opção B: Trocar Navegador

Se problema continua:
- Feche **TUDO**
- Abra outro navegador (Chrome, Firefox, Edge)
- Tente novamente

### Opção C: Hard Reset

```javascript
// No console do navegador:
localStorage.clear();
sessionStorage.clear();
caches.keys().then(names => {
  names.forEach(name => caches.delete(name));
  console.log('Cache limpo');
});

// Recarregue:
// Ctrl + Shift + R
```

---

## Diagnóstico Rápido

Se vir no console:

**✅ FUNCIONA:**
```
[LOGIN] Token recebido: eyJ...
[LOGIN] Token salvo em localStorage
[AUTH] Token encontrado em localStorage
```

**❌ NÃO FUNCIONA:**
```
[LOGIN] Token recebido: undefined
// OU
[LOGIN] Token em localStorage: null
// OU
[AUTH] Sem token em localStorage
```

---

## Mensagens de Erro Comuns

| Mensagem | Significado | Solução |
|----------|-------------|---------|
| `Token recebido: undefined` | API não retornou token | Reinicie servidor |
| `Token em localStorage: null` | localStorage bloqueado | Use navegador normal |
| `Sem token em localStorage` | Token não foi salvo | Limite localStorage? |

---

## Próximos Passos

1. **Execute os testes acima**
2. **Me diga qual passo falhou**
3. **Envie screenshot do console**

---

**Status:** Pronto para testar! 🚀
