# Teste Imediato

## Passo 1: Parar o servidor atual
Pressione `Ctrl+C` no terminal onde o servidor está rodando

## Passo 2: Reiniciar o servidor
```bash
cd interfaces/web
python -m uvicorn app:app --host 127.0.0.1 --port 8001 --reload
```

## Passo 3: Testar
1. Abra navegador em modo incógnito (Ctrl+Shift+N no Windows, Cmd+Shift+N no Mac)
2. Acesse `http://localhost:8001/`
3. Você deve ver:
   - Página de Home COM o menu sidebar
   - **Sem `#` na URL**
4. Clique em "Cadastros" (o botão)
5. Clique em "Novo Cliente"
6. A URL deve mudar para `http://localhost:8001/clientes/novo`
7. A página "Novo Cliente" deve carregar

## Passo 4: Se der erro
Procure no console do servidor por mensagens como:
```
Erro ao carregar novo_cliente_form: ...
Traceback ...
```

## Debug
No navegador (F12 → Console):
```javascript
// Verificar URL
console.log(window.location.href);

// Verificar token
console.log(localStorage.getItem('access_token'));

// Limpar cache se necessário
localStorage.clear();
```

## Resultado Esperado

Depois de testar:
1. Home funciona sem `#`
2. Cliques em menus funcionam
3. Outras páginas carregam (clientes, técnicos, etc.)
4. Logout funciona

Se tiver erro 404, o console do servidor vai mostrar qual é o erro real (provavelmente um import ou banco de dados).
