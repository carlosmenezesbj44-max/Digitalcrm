# 🧪 Teste: Autenticação no Menu

## Guia de Teste Passo a Passo

### Cenário 1: Navegação Normal (Deve Funcionar ✅)

**Tempo:** 2 minutos

1. **Abra o navegador** (Chrome, Firefox, Edge)
2. **Vá para:** `http://seu-crm/login`
3. **Faça login** com suas credenciais
4. **Você será redirecionado para dashboard**
5. **Clique em "Novo Cliente"** (no menu Cadastros)
6. **Página carrega normalmente** ✅
7. **Clique em "Home"** (menu principal)
8. **Dashboard carrega normalmente** ✅ (NÃO redireciona para login)
9. **Resultado esperado:** Pode navegar livremente

---

### Cenário 2: Token Expirado (Deve Redirecionar para Login ✅)

**Tempo:** 5 minutos

1. **Abra o navegador console** (F12)
2. **Vá para:** `http://seu-crm/dashboard`
3. **Você vê dashboard normalmente**
4. **Abra Console** (F12 → Console)
5. **Cole este comando:**
   ```javascript
   localStorage.removeItem('access_token');
   ```
6. **Pressione Enter**
7. **Atualize a página** (F5)
8. **Resultado esperado:** Redirecionado para `/login` ✅

---

### Cenário 3: Token Inválido (Deve Redirecionar para Login ✅)

**Tempo:** 5 minutos

1. **Abra Console** (F12 → Console)
2. **Cole este comando:**
   ```javascript
   localStorage.setItem('access_token', 'token_invalido_12345');
   ```
3. **Pressione Enter**
4. **Vá para:** `http://seu-crm/clientes`
5. **Resultado esperado:** Redirecionado para `/login` ✅

---

### Cenário 4: Múltiplas Abas (Deve Sincronizar ✅)

**Tempo:** 3 minutos

1. **Abra primeira aba do navegador**
2. **Faça login em:** `http://seu-crm/login`
3. **Abra nova aba** (Ctrl+T)
4. **Vá para:** `http://seu-crm/clientes`
5. **Resultado esperado:** Carrega normalmente (compartilha localStorage) ✅

---

## Checklist de Teste

### Teste Básico
- [ ] Login funciona
- [ ] Dashboard carrega após login
- [ ] Menu está visível
- [ ] Clique em item do menu funciona
- [ ] Clique em "Home" funciona
- [ ] Não redireciona para login ao navegar

### Teste Avançado
- [ ] Remover token → Redireciona para login
- [ ] Colocar token inválido → Redireciona para login
- [ ] Abrir múltiplas abas → Todas funcionam
- [ ] Logout funciona
- [ ] Fazer login novamente funciona

### Teste em Diferentes Páginas
- [ ] Clientes
- [ ] Contratos
- [ ] Produtos
- [ ] Planos
- [ ] Ordens de Serviço
- [ ] Configurações
- [ ] Usuários

---

## O Que Procurar no Console (F12)

### Mensagens de Sucesso ✅
```
[AUTH] Path: /contratos, Public: true
[AUTH] Autenticação validada
```

### Mensagens de Erro ❌
```
[AUTH] Sem token, redirecionando para login
[AUTH] Token inválido, redirecionando para login
[AUTH ERROR] SomeError: message
```

---

## Se Algo Não Funcionar

### 1. Verificar se auth-check.js foi carregado

No Console (F12):
```javascript
// Procure por esta mensagem:
// [AUTH] Script de autenticação carregado
```

Se não aparecer:
- Página não tem `<script src="/static/js/auth-check.js"></script>`
- Revise as modificações feitas

### 2. Verificar se token está salvo

No Console (F12):
```javascript
console.log(localStorage.getItem('access_token'));
```

Resultado esperado:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Se vazio:
- Você não fez login
- Faça login novamente

### 3. Verificar Network (abas carregadas)

1. Abra Console (F12)
2. Vá para aba "Network"
3. Recarregue página (F5)
4. Procure por requisições com status 401
5. Se tiver, token está inválido

---

## Resultados Esperados

### ✅ Funcionando Corretamente

```
Ação: Clica em "Novo Cliente" → Dashboard → Home
Resultado: Navega sem erros
Status: ✅ PASSA
```

```
Ação: Remove token → Recarrega página
Resultado: Vai para login
Status: ✅ PASSA
```

```
Ação: Coloca token inválido → Navega
Resultado: Vai para login
Status: ✅ PASSA
```

### ❌ Não Funcionando

```
Ação: Clica em "Home" após clicar em item do menu
Resultado: Redireciona para login
Status: ❌ FALHA - Verificar console (F12)
```

---

## Relatório de Teste

Use este modelo para documentar seu teste:

```markdown
# Teste de Autenticação

## Data: __/__/____
## Versão: ___
## Navegador: ___

### Resultados:
- Cenário 1 (Navegação Normal): [ ] ✅ [ ] ❌
- Cenário 2 (Token Expirado): [ ] ✅ [ ] ❌
- Cenário 3 (Token Inválido): [ ] ✅ [ ] ❌
- Cenário 4 (Múltiplas Abas): [ ] ✅ [ ] ❌

### Problemas Encontrados:
- [ ] Nenhum
- [ ] __________

### Notas:
_________________
```

---

## Perguntas Frequentes

**P: Por quanto tempo o token dura?**  
R: Verifique em `crm_core/security/auth_utils.py` - geralmente 24 horas

**P: E se o token expirar enquanto estou usando?**  
R: Você será redirecionado para login - faça login novamente

**P: Preciso fazer algo special após instalar?**  
R: Não! Tudo funciona automaticamente

**P: Vai afetar meu código?**  
R: Não! É 100% compatível com código existente

---

## Support

Se tiver problema:

1. **Abra Console** (F12)
2. **Procure por erros**
3. **Copie a mensagem de erro**
4. **Reporte com a mensagem**

---

**Pronto para testar? Comece pelo Cenário 1!** 🚀
