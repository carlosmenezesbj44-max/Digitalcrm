# 🔍 Diagnóstico: Problema de Login Persistente

## Procedimento de Diagnóstico

Siga EXATAMENTE estes passos:

### Passo 1: Abra o Navegador em Modo Incógnito

```
Ctrl + Shift + N (ou abra Incógnito do menu)
```

**Por quê?** Evita interferência de cookies antigos

---

### Passo 2: Abra o Console de Desenvolvimento

```
Pressione F12 → Clique em "Console"
```

---

### Passo 3: Acesse a Página de Login

```
Vá para: http://seu-crm/login
```

---

### Passo 4: Limpe o localStorage (importante!)

No console, digite:
```javascript
localStorage.clear();
console.log('localStorage limpo');
```

Pressione Enter.

---

### Passo 5: Faça Login

1. **Username:** (seu usuário)
2. **Senha:** (sua senha)
3. **Clique em Login**

---

### Passo 6: Observe o Console

Você deve ver estas mensagens:

**✅ CORRETO (mensagens esperadas):**
```
[LOGIN] Token recebido: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
[LOGIN] Token salvo em localStorage
[LOGIN] Token em localStorage: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
[AUTH] Token encontrado em localStorage
```

**❌ ERRADO (significa problema):**
```
[LOGIN] Token recebido: undefined
// OU
[LOGIN] Token em localStorage: null
// OU
[AUTH] Sem token em localStorage, redirecionando para login
```

---

## O Que Fazer Baseado no Resultado

### Se Viu ✅ (Correto)

Se viu as mensagens corretas mas ainda redireciona para login:

1. **Abra Console (F12)**
2. **Vá para /dashboard**
3. **Veja se aparece:** `[AUTH] Token encontrado em localStorage`
4. Se sim → Clique em Home (menu)
5. Se redirecionar mesmo assim → PROBLEMA NO auth-check.js

**Solução:** Reinicie o servidor (Ctrl+C + python -m uvicorn...)

---

### Se Viu ❌ (Token undefined)

Significa que `/api/usuarios/login` **não está retornando token**.

1. **Abra console novamente**
2. **No formulário, insira credenciais**
3. **Vá para aba "Network"** (F12)
4. **Faça login**
5. **Procure por requisição para `/api/usuarios/login`**
6. **Clique nela**
7. **Veja aba "Response"**

Você deve ver:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

Se não tiver `access_token`, o problema é no **backend** (API).

**Solução:** Verifique se a API `/api/usuarios/login` está funcionando corretamente.

---

### Se Viu ❌ (Token em localStorage é null)

Significa que localStorage está **bloqueado ou com problema**.

**Teste isso no console:**
```javascript
// Teste 1: Pode salvar em localStorage?
localStorage.setItem('test', 'value');
console.log(localStorage.getItem('test'));

// Resultado esperado: "value"
```

Se resultado for `null`:
- [ ] Seu navegador bloqueou localStorage
- [ ] Você está em modo privado/incógnito
- [ ] Há um problema com as configurações do navegador

**Solução:** 
1. Use navegador normal (não incógnito)
2. Teste em outro navegador
3. Limpe cache/cookies do navegador

---

## Resumo do Fluxo Esperado

```
1. Digite credenciais
   ↓
2. Clique Login
   ↓
3. API retorna token
   ↓
4. JavaScript salva em localStorage
   ↓
5. Redireciona para /dashboard
   ↓
6. auth-check.js verifica localStorage
   ↓
7. Token encontrado ✅
   ↓
8. Página carrega normalmente
   ↓
9. Clique em "Home"
   ↓
10. Dashboard carrega (NÃO redireciona) ✅
```

---

## Se Ainda Não Funcionar

Envie para mim:
1. **Screenshot do console** mostrando quais mensagens aparecem
2. **URL que está acessando**
3. **Qual navegador está usando**
4. **Quais credenciais está tentando**

---

## Checklist Rápido

- [ ] Abri em modo incógnito
- [ ] Abri console (F12)
- [ ] Limpei localStorage
- [ ] Vi mensagens `[LOGIN]` no console
- [ ] Token não é `undefined`
- [ ] localStorage tem o token
- [ ] Consigo navegar sem ser redirecionado

Se todos checados ✅ → **Problema resolvido!**

Se algum não checado ❌ → **Vimos o ponto do problema**

---

**Próximo:** Execute este diagnóstico e me mostre qual passo falhou!
