/**
 * Auth Check - Verifica autenticação em cada página
 * Se não tiver token, redireciona para login
 * 
 * NOTA: Não faz requisição ao servidor pois o middleware já valida
 */

(function() {
    // Verificar apenas em rotas protegidas
    const rotasPublicas = ['/login', '/registrar'];
    const caminhoAtual = window.location.pathname;
    
    // Se é rota pública, não verificar
    if (rotasPublicas.some(rota => caminhoAtual.startsWith(rota))) {
        console.log('[AUTH] Rota pública: ' + caminhoAtual);
        return;
    }
    
    // Verificar token
    const token = localStorage.getItem('access_token');
    
    if (!token) {
        console.warn('[AUTH] Sem token em localStorage, redirecionando para login');
        window.location.href = '/login';
        return;
    }
    
    console.log('[AUTH] Token encontrado em localStorage');
    // O middleware do servidor validará o token nas requisições da API
})();

/**
 * Adiciona token ao header automaticamente em todos os fetch
 * E trata erro 401 redirecionando para login
 */
const originalFetch = window.fetch;
window.fetch = function(...args) {
    const token = localStorage.getItem('access_token');
    
    if (args[0] && typeof args[0] === 'string' && args[0].startsWith('/api/')) {
        // Normalizar caminhos antigos /api/ para /api/v1/
        if (!args[0].startsWith('/api/v1/')) {
            args[0] = args[0].replace('/api/', '/api/v1/');
        }
    }

    if (token && args[0] && typeof args[0] === 'string' && args[0].startsWith('/api')) {
        // É uma chamada para API
        const options = args[1] || {};
        
        if (!options.headers) {
            options.headers = {};
        }
        
        // Adicionar Authorization header se não existir
        if (!options.headers['Authorization']) {
            options.headers['Authorization'] = `Bearer ${token}`;
        }
        
        args[1] = options;
    }
    
    // Chamar fetch original e tratar resposta
    return originalFetch.apply(this, args).then(response => {
        // Se receber 401 (não autenticado), redirecionar para login
        if (response.status === 401) {
            console.warn('[AUTH] Resposta 401 recebida, redirecionando para login');
            localStorage.removeItem('access_token');
            window.location.href = '/login';
            return response;
        }
        return response;
    });
};

console.log('[AUTH] Script de autenticação carregado');
