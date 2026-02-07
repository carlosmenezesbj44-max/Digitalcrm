# 🔒 Solução: Problema de Autenticação ao Navegar no Menu

## Problema
Ao clicar em um item do menu e depois clicar em "Home" (dashboard), você é redirecionado para a página de login.

## Causa
O token JWT estava armazenado em `localStorage`, mas as páginas HTML não estavam verificando se o token era válido ao carregar. Se o token expirava ou era removido, ao navegar para outra página HTML, você era redirecionado para login.

## Solução Implementada

### 1. Arquivo `auth-check.js` Criado ✅
```
interfaces/web/static/js/auth-check.js
```

Este arquivo:
- Verifica se tem token em `localStorage`
- Se não tiver, redireciona para `/login`
- Valida o token no servidor
- Adiciona automaticamente o token a todos os requests da API

### 2. Integração em contratos.html ✅
Adicionei no início dos scripts:
```html
<script src="/static/js/auth-check.js"></script>
```

---

## Como Adicionar em Outras Páginas

### Para TODAS as páginas protegidas (exceto login/registrar):

1. **Abra o arquivo HTML** (ex: `clientes.html`)

2. **Encontre esta linha:**
```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
```

3. **Adicione LOGO APÓS:**
```html
<script src="/static/js/auth-check.js"></script>
```

**Exemplo:**
```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
<script src="/static/js/auth-check.js"></script>  <!-- ← ADICIONE ISTO -->
<script src="/static/js/menu-handler.js"></script>
```

---

## Páginas Que Precisam da Alteração

Adicione em:
- [ ] `novo_cliente.html`
- [ ] `clientes.html`
- [ ] `novo_tecnico.html`
- [ ] `tecnicos.html`
- [ ] `novo_produto.html`
- [ ] `produtos.html`
- [ ] `novo_plano.html`
- [ ] `planos.html`
- [ ] `novo_contrato.html`
- [ ] `contratos.html` ✅ (PRONTO)
- [ ] `ordens_servico.html`
- [ ] `nova_ordem_servico.html`
- [ ] `servidores.html`
- [ ] `novo_servidor.html`
- [ ] `usuarios.html`
- [ ] Qualquer outra página protegida

---

## Páginas Que NÃO Precisam

Não adicione em:
- `login.html` (rota pública)
- `registrar.html` (rota pública)

---

## Como Funciona

### Fluxo Quando Clica em Menu

**Antes (PROBLEMA):**
```
1. Clica em "Novo Cliente"
2. Vai para /clientes/novo
3. Página carrega HTML sem verificar token
4. Se token expirado, fica sem autenticação
5. Clica em "Home" → Redireciona para login
```

**Depois (SOLUÇÃO):**
```
1. Clica em "Novo Cliente"
2. Vai para /clientes/novo
3. auth-check.js verifica token em localStorage
4. Se não tiver, redireciona para /login
5. Se tiver, valida no servidor
6. Se válido, permite acesso
7. Clica em "Home" → Carrega normalmente
```

---

## O que auth-check.js Faz

### 1. Verifica Autenticação
```javascript
// Se não tem token, redireciona para login
const token = localStorage.getItem('access_token');
if (!token) {
    window.location.href = '/login';
}
```

### 2. Valida Token no Servidor
```javascript
// Faz request para /api/usuarios/me
// Se resposta é 401, token expirou
// Redireciona para login
```

### 3. Adiciona Token Automaticamente
```javascript
// Intercepta todos os fetch() para API
// Adiciona Authorization: Bearer <token>
// Não precisa fazer manualmente
```

---

## Teste a Solução

1. **Abra o navegador**
2. **Faça login no CRM**
3. **Clique em um item do menu** (ex: "Novo Cliente")
4. **Aguarde carregar**
5. **Clique em "Home"**
6. **Resultado esperado:** Dashboard carrega normalmente (não redireciona para login)

---

## Script Completo

Se precisar saber o que está em `auth-check.js`:

```javascript
// 1. Verifica se tem token
// 2. Se não tiver, vai para login
// 3. Se tiver, valida no servidor
// 4. Adiciona token automaticamente a API calls
// 5. Se servidor diz que token inválido, vai para login
```

---

## Próximas Ações

- [ ] Adicione `<script src="/static/js/auth-check.js"></script>` em todas as páginas protegidas
- [ ] Teste navegação entre páginas
- [ ] Verifique que volta para login se token expirar
- [ ] Pronto! ✅

---

## Troubleshooting

### "Continuo sendo redirecionado para login"

**Causa:** Página não tem o script `auth-check.js`

**Solução:** Adicione a linha:
```html
<script src="/static/js/auth-check.js"></script>
```

### "Consigo entrar, mas ao navegar para outra página dá erro"

**Causa:** Página não tem o script

**Solução:** Mesma acima

### "Diz que preciso fazer login, mas já estou logado"

**Causa:** Token expirou ou foi apagado

**Solução:**
1. Faça logout
2. Faça login novamente
3. Token será renovado

---

## Status

✅ Script criado e integrado em `contratos.html`  
⏳ Precisa adicionar em outras páginas (15 minutos)  
✅ Depois, problema resolvido!

---

**Próximo:** Adicione o script em todas as outras páginas HTML protegidas. Use o checklist acima.
