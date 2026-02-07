# Correção: Menus Não Funcionando

## Problema Identificado

Quando você clicava nos menus da sidebar, nada acontecia. A causa foi:

1. **Middleware de autenticação muito restritivo**: O middleware bloqueava requisições HTTP para páginas que exigiam token JWT no header, mas o token estava apenas no `localStorage` do navegador (JavaScript).

2. **Falta de envio de token em navegações**: Os links do menu fazem navegação normal (página inteira), que não enviam o token como header HTTP.

## Soluções Implementadas

### 1. Atualização do Middleware de Autenticação
**Arquivo**: `crm_core/middleware/auth_middleware.py`

- Adicionadas rotas públicas para que as páginas HTML sejam servidas sem exigir token no header
- O controle de acesso agora é feito pelo JavaScript no cliente
- Rotas públicas adicionadas:
  - `/clientes`, `/clientes/novo`
  - `/tecnicos`, `/tecnicos/novo`
  - `/produtos`, `/produtos/novo`
  - `/planos`, `/planos/novo`
  - `/ordens-servico`, `/ordens-servico/nova`
  - `/servidores`, `/servidores/novo`
  - `/usuarios`
  - `/static` (para arquivos estáticos)

### 2. Novo Script JavaScript Compartilhado
**Arquivo**: `interfaces/web/static/js/menu-handler.js`

Este script:
- Verifica se existe token no `localStorage` ao carregar a página
- Se não houver token, redireciona para `/login`
- Intercepta cliques em todos os links internos (`<a href="/...">`)
- Envia o token JWT no header Authorization para cada navegação
- Trata erros 401 (Unauthorized) redirecionando para login

### 3. Atualização de Todos os Templates HTML
**Arquivo**: Script executado: `atualizar_templates_menu.py`

- Adicionado `<script src="/static/js/menu-handler.js"></script>` a todos os templates
- Exceções: `login.html` e `registrar.html` (páginas de autenticação)

## Como Funciona Agora

1. Usuário acessa o site
2. Se não tiver token, é redirecionado para `/login`
3. Após fazer login, o token é salvo em `localStorage`
4. Quando clica em um menu ou link:
   - O JavaScript intercepta o clique
   - Envia o token JWT no header da requisição HTTP
   - Se o token for válido, a página é carregada
   - Se o token expirou ou for inválido, o usuário é redirecionado para login

## Testar

1. Acesse `http://localhost:8001/`
2. Você será redirecionado para `/login`
3. Faça login com suas credenciais
4. Agora os menus devem funcionar ao clicar

## Debug

Se os menus ainda não funcionarem:

1. Abra o console do navegador (F12 → Console)
2. Verifique se há erros JavaScript
3. Verifique se o token está armazenado:
   ```javascript
   console.log(localStorage.getItem('access_token'))
   ```
4. Verifique as requisições de rede (F12 → Network)
   - Cada clique deve gerar uma requisição com header `Authorization: Bearer {token}`

## Notas de Segurança

- O token é armazenado em `localStorage` (acessível via JavaScript)
- Para produção, considere usar HttpOnly cookies
- Os erros HTTP devem ser tratados com cuidado para não expor informações sensíveis
