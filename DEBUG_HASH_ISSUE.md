# Problema: Hash (#) na URL

## Análise

A URL está aparecendo como `localhost:8001/#` quando deveria ser apenas `localhost:8001/`.

Possíveis causas:

1. **Navegador cache**: O navegador armazenou uma versão antiga com hash
2. **JavaScript antigo**: Há código JavaScript que adiciona hash
3. **Middleware ou servidor**: Algo está redirecionando para URL com hash
4. **Service Worker**: Um service worker pode estar interceptando navegação

## Solução Implementada

### 1. Remoção de hash no DOMContentLoaded
```javascript
if (window.location.hash) {
    window.history.replaceState({}, document.title, window.location.pathname + window.location.search);
}
```

Este código:
- Detecta se há hash na URL
- Remove o hash usando `replaceState`
- Não cria um novo entry no histórico do navegador

### 2. Uso de `location.replace()` ao invés de `location.href`
- `location.replace()` não mantém o redirecionamento anterior no histórico
- Evita que o usuário volte para uma URL com hash

### 3. Limpeza de cache (Instruções para o usuário)

## Como Testar

### Opção 1: Hard Refresh (Melhor)
```
Windows: Ctrl + Shift + R  ou Ctrl + F5
Mac: Cmd + Shift + R ou Cmd + Option + R
```

### Opção 2: Limpar Cache Completo
1. Abra DevTools (F12)
2. Vá em Settings → Storage
3. Clique em "Clear site data"
4. Refresh F5

### Opção 3: Incógnito/Privado
1. Abra navegador em modo incógnito
2. Acesse `http://localhost:8001/`
3. Verifique se o hash ainda aparece

## Debug

Se o hash continuar aparecendo:

### No Console (F12 → Console):
```javascript
// Verificar URL atual
console.log('Hash:', window.location.hash);
console.log('Pathname:', window.location.pathname);
console.log('Full URL:', window.location.href);

// Remover manualmente
window.location.replace(window.location.pathname);
```

### Verificar se há Service Worker
```javascript
// No console
navigator.serviceWorker.getRegistrations().then(registrations => {
    console.log('Service Workers:', registrations);
    // Unregister todos
    registrations.forEach(reg => reg.unregister());
});
```

### Verificar requisições de rede (F12 → Network)
- Verifique se há um redirect 301/302/307
- A URL inicial deve ser `/`, não `/#`

## Próximos Passos

1. **Fazer hard refresh** (Ctrl+Shift+R no Windows, Cmd+Shift+R no Mac)
2. **Fechar completamente o navegador** e reabrir
3. **Testar em modo incógnito**
4. Se persistir, há um problema no servidor ou service worker

## Se o Problema Persistir

Isso indica que há algo gerando o hash:

1. Verifique se há um service worker ativo:
   ```javascript
   navigator.serviceWorker.getRegistrations().then(r => console.log(r));
   ```

2. Procure no código por `location.hash` ou `#`

3. Verifique se há um arquivo `.well-known` ou `service-worker.js` servindo código

4. Limpe o banco de dados IndexedDB/LocalStorage:
   ```javascript
   // No console
   localStorage.clear();
   sessionStorage.clear();
   indexedDB.databases().then(dbs => {
       dbs.forEach(db => indexedDB.deleteDatabase(db.name));
   });
   ```
