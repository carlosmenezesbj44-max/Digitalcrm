// Menu handler - funciona para todos os templates

// Sincronizar menus ao carregar a pagina
// NOTA: Verificação de autenticação agora feita por auth-check.js
window.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    
    // Remover hash da URL se existir (https://localhost/#  -> https://localhost/)
    if (window.location.hash) {
        window.history.replaceState({}, document.title, window.location.pathname + window.location.search);
    }
    
    // Sincronizar estados de chevrons com menus
    syncMenuStates();
});

function syncMenuStates() {
    // Sincroniza o estado visual dos chevrons com os submenus
    const menus = document.querySelectorAll('.sidebar .menu-toggle');
    menus.forEach(button => {
        const submenu = button.nextElementSibling;
        const chevron = button.querySelector('i:last-child');
        
        if (!submenu || !chevron) return;
        
        // Se submenu tem 'show', chevron deve ser 'bi-chevron-up'
        // Se submenu não tem 'show', chevron deve ser 'bi-chevron-down'
        
        const hasShow = submenu.classList.contains('show');
        const hasChevronUp = chevron.classList.contains('bi-chevron-up');
        
        // Se estado está inconsistente, corrige
        if (hasShow && !hasChevronUp) {
            chevron.classList.remove('bi-chevron-down');
            chevron.classList.add('bi-chevron-up');
        } else if (!hasShow && hasChevronUp) {
            chevron.classList.remove('bi-chevron-up');
            chevron.classList.add('bi-chevron-down');
        }
    });
}

function toggleSubmenu(button) {
    const submenu = button.nextElementSibling;
    if (!submenu) return;
    
    const chevron = button.querySelector('i:last-child');
    
    submenu.classList.toggle('show');
    if (chevron) {
        chevron.classList.toggle('bi-chevron-down');
        chevron.classList.toggle('bi-chevron-up');
    }
    
    // Sincronizar estado após toggle
    syncMenuStates();
}

function logout() {
    // Limpar token do localStorage
    localStorage.removeItem('access_token');
    // Redirecionar para login
    window.location.replace('/login');
}
