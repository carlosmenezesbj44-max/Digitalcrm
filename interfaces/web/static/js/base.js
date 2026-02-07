/* ==========================================================================
   CRM Provedor - JavaScript Base Centralizado
   ========================================================================== */

/**
 * Namespace principal do CRM
 */
const CRM = {
    // Configurações globais
    config: {
        apiBase: '/api/v1',
        timeout: 30000,
        maxRetries: 3
    },
    
    // Estado da aplicação
    state: {
        sidebarOpen: true,
        currentTheme: 'light',
        user: null
    }
};

/* ==========================================================================
   Utility Functions
   ========================================================================== */

/**
 * Executa uma requisição HTTP assíncrona
 */
CRM.api = {
    async get(endpoint, options = {}) {
        return this._request('GET', endpoint, null, options);
    },
    
    async post(endpoint, data = null, options = {}) {
        return this._request('POST', endpoint, data, options);
    },
    
    async put(endpoint, data = null, options = {}) {
        return this._request('PUT', endpoint, data, options);
    },
    
    async delete(endpoint, options = {}) {
        return this._request('DELETE', endpoint, null, options);
    },
    
    async _request(method, endpoint, data = null, options = {}) {
        // Normalizar caminhos antigos /api/ para /api/v1/
        if (endpoint.startsWith('/api/') && !endpoint.startsWith('/api/v1/')) {
            endpoint = endpoint.replace('/api/', '/');
        }
        
        const url = `${CRM.config.apiBase}${endpoint.startsWith('/') ? endpoint : '/' + endpoint}`;
        
        const config = {
            method,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        if (data) {
            config.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                const error = await response.json().catch(() => ({ detail: 'Erro desconhecido' }));
                throw new Error(error.detail || `HTTP ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error(`API Error [${method} ${endpoint}]:`, error);
            throw error;
        }
    }
};

/**
 * Funções de formatação
 */
CRM.format = {
    // Formatar CPF
    cpf(value) {
        const cleaned = value.replace(/\D/g, '');
        if (cleaned.length > 11) return cleaned.slice(0, 11);
        return cleaned.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
    },
    
    // Formatar CNPJ
    cnpj(value) {
        const cleaned = value.replace(/\D/g, '');
        if (cleaned.length > 14) return cleaned.slice(0, 14);
        return cleaned.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
    },
    
    // Formatar CEP
    cep(value) {
        const cleaned = value.replace(/\D/g, '');
        if (cleaned.length > 8) return cleaned.slice(0, 8);
        return cleaned.replace(/(\d{5})(\d{3})/, '$1-$2');
    },
    
    // Formatar telefone
    telefone(value) {
        const cleaned = value.replace(/\D/g, '');
        if (cleaned.length > 11) return cleaned.slice(0, 11);
        
        if (cleaned.length <= 10) {
            return cleaned.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
        } else {
            return cleaned.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
        }
    },
    
    // Formatar data
    date(date, format = 'dd/MM/yyyy') {
        if (!date) return '';
        const d = new Date(date);
        const day = String(d.getDate()).padStart(2, '0');
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const year = d.getFullYear();
        
        return format.replace('dd', day).replace('MM', month).replace('yyyy', year);
    },
    
    // Formatar moeda
    currency(value, locale = 'pt-BR', currency = 'BRL') {
        return new Intl.NumberFormat(locale, {
            style: 'currency',
            currency
        }).format(value);
    },
    
    // Formatar número
    number(value, decimals = 0) {
        return new Intl.NumberFormat('pt-BR', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        }).format(value);
    }
};

/* ==========================================================================
   Menu Functions
   ========================================================================== */

/**
 * Alterna a visibilidade do submenu
 */
function toggleSubmenu(button) {
    const submenu = button.nextElementSibling;
    const icon = button.querySelector('.chevron, .bi-chevron-down, .bi-chevron-up');
    const isExpanded = submenu.classList.contains('show');
    
    // Fechar outros submenus
    document.querySelectorAll('.submenu.show').forEach(sm => {
        if (sm !== submenu) {
            sm.classList.remove('show');
        }
    });
    
    // Alternar submenu atual
    submenu.classList.toggle('show');
    
    // Atualizar ícone
    if (icon) {
        icon.classList.toggle('bi-chevron-down', !submenu.classList.contains('show'));
        icon.classList.toggle('bi-chevron-up', submenu.classList.contains('show'));
    }
    
    // Atualizar aria-expanded
    button.setAttribute('aria-expanded', !isExpanded);
}

/**
 * Alternar sidebar em dispositivos móveis
 */
function toggleMobileSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('show');
    }
}

/* ==========================================================================
   Form Functions
   ========================================================================== */

/**
 * Adicionar máscara de input
 */
function addInputMask(inputId, maskType) {
    const input = document.getElementById(inputId);
    if (!input) return;
    
    input.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\D/g, '');
        
        switch (maskType) {
            case 'cpf':
                e.target.value = CRM.format.cpf(value);
                break;
            case 'cnpj':
                e.target.value = CRM.format.cnpj(value);
                break;
            case 'cep':
                e.target.value = CRM.format.cep(value);
                break;
            case 'telefone':
                e.target.value = CRM.format.telefone(value);
                break;
            case 'data':
                e.target.value = value.slice(0, 8).replace(/(\d{2})(\d{2})(\d{4})/, '$1/$2/$3');
                break;
            case 'moeda':
                const num = parseFloat(value) / 100;
                e.target.value = CRM.format.currency(num);
                break;
        }
    });
}

/**
 * Validar formulário
 */
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        const feedback = field.parentElement.querySelector('.invalid-feedback');
        
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            if (feedback) feedback.style.display = 'block';
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
            if (feedback) feedback.style.display = 'none';
        }
    });
    
    return isValid;
}

/**
 * Limpar erros do formulário
 */
function clearFormErrors(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    form.querySelectorAll('.is-invalid').forEach(field => {
        field.classList.remove('is-invalid');
    });
    
    form.querySelectorAll('.invalid-feedback').forEach(feedback => {
        feedback.style.display = 'none';
    });
}

/* ==========================================================================
   Toast/Notification Functions
   ========================================================================== */

/**
 * Mostrar notificação toast
 */
function showToast(message, type = 'info', duration = 3000) {
    const container = document.getElementById('toastContainer') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="bi ${getToastIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Adicionar estilos inline temporários
    toast.style.cssText = `
        background: ${getToastBg(type)}; 
        color: ${getToastColor(type)};
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 10px;
        animation: slideIn 0.3s ease;
        min-width: 250px;
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

/**
 * Mostrar notificação toast a partir de resposta JSON
 */
function showToastFromResponse(response, duration = 3000) {
    if (typeof response === 'string') {
        try {
            response = JSON.parse(response);
        } catch (e) {
            showToast(response, 'info', duration);
            return;
        }
    }
    
    if (response && typeof response === 'object') {
        const message = response.message || response.detail || 'Operação concluída';
        const type = response.success === true ? 'success' : (response.success === false ? 'error' : 'info');
        showToast(message, type, duration);
    } else {
        showToast(response, 'info', duration);
    }
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 350px;
    `;
    document.body.appendChild(container);
    return container;
}

function getToastIcon(type) {
    const icons = {
        success: 'bi-check-circle-fill',
        error: 'bi-exclamation-circle-fill',
        warning: 'bi-exclamation-triangle-fill',
        info: 'bi-info-circle-fill'
    };
    return icons[type] || icons.info;
}

function getToastBg(type) {
    const colors = {
        success: '#d4edda',
        error: '#f8d7da',
        warning: '#fff3cd',
        info: '#d1ecf1'
    };
    return colors[type] || colors.info;
}

function getToastColor(type) {
    const colors = {
        success: '#155724',
        error: '#721c24',
        warning: '#856404',
        info: '#0c5460'
    };
    return colors[type] || colors.info;
}

/**
 * Mostrar loading overlay
 */
function showLoading(message = 'Carregando...') {
    let loading = document.getElementById('loadingOverlay');
    if (!loading) {
        loading = document.createElement('div');
        loading.id = 'loadingOverlay';
        loading.innerHTML = `
            <div class="loading-content">
                <div class="spinner spinner-lg"></div>
                <p class="loading-message">${message}</p>
            </div>
        `;
        loading.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
        `;
        document.body.appendChild(loading);
    }
    loading.querySelector('.loading-message').textContent = message;
    loading.style.display = 'flex';
}

function hideLoading() {
    const loading = document.getElementById('loadingOverlay');
    if (loading) {
        loading.style.display = 'none';
    }
}

/* ==========================================================================
   Modal Functions
   ========================================================================== */

/**
 * Abrir modal
 */
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal && window.bootstrap) {
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    } else {
        const el = document.getElementById(modalId);
        if (el) el.style.display = 'block';
    }
}

/**
 * Fechar modal
 */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal && window.bootstrap) {
        const bsModal = bootstrap.Modal.getInstance(modal);
        if (bsModal) bsModal.hide();
    } else {
        if (modal) modal.style.display = 'none';
    }
}

/* ==========================================================================
   Table/List Functions
   ========================================================================== */

/**
 * Alternar visualização entre tabela e cards
 */
function toggleView(viewName) {
    const tableView = document.getElementById('viewTable');
    const cardsView = document.getElementById('viewCards');
    const toggleBtn = document.getElementById('btnToggleView');
    
    if (viewName === 'table') {
        if (tableView) tableView.style.display = 'block';
        if (cardsView) cardsView.style.display = 'none';
        if (toggleBtn) toggleBtn.innerHTML = '<i class="bi bi-grid"></i> Cards';
        localStorage.setItem('viewMode', 'table');
    } else {
        if (tableView) tableView.style.display = 'none';
        if (cardsView) cardsView.style.display = 'flex';
        if (toggleBtn) toggleBtn.innerHTML = '<i class="bi bi-table"></i> Tabela';
        localStorage.setItem('viewMode', 'cards');
    }
}

/**
 * Inicializar toggle de visualização
 */
function initViewToggle(defaultView = 'table') {
    const toggleBtn = document.getElementById('btnToggleView');
    if (!toggleBtn) return;
    
    const savedView = localStorage.getItem('viewMode') || defaultView;
    toggleView(savedView);
    
    toggleBtn.addEventListener('click', () => {
        const currentView = document.getElementById('viewTable')?.style.display !== 'none' ? 'table' : 'cards';
        toggleView(currentView === 'table' ? 'cards' : 'table');
    });
}

/**
 * Inicializar busca com debounce
 * @param {string} inputId - ID do input de busca
 * @param {function} callback - Função a ser executada na busca
 * @param {number} delay - Tempo de debounce em ms
 */
function initSearch(inputId, callback, delay = 300) {
    const input = document.getElementById(inputId);
    if (!input) {
        console.warn(`Input de busca não encontrado: ${inputId}`);
        return;
    }
    
    let timeoutId = null;
    
    input.addEventListener('input', function(e) {
        // Limpar timeout anterior
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        
        // Definir novo timeout (debounce)
        timeoutId = setTimeout(() => {
            callback(e);
        }, delay);
    });
    
    // Também buscar ao pressionar Enter
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            if (timeoutId) {
                clearTimeout(timeoutId);
            }
            callback(e);
        }
    });
}

/**
 * Exportar dados para CSV
 */
function exportToCSV(data, filename, headers = null) {
    if (!data || !data.length) {
        showToast('Nenhum dado para exportar', 'warning');
        return;
    }
    
    const keys = headers || Object.keys(data[0]);
    const csvContent = [
        keys.join(','),
        ...data.map(row => keys.map(k => {
            let val = row[k] !== undefined ? row[k] : '';
            if (typeof val === 'string' && val.includes(',')) {
                val = `"${val.replace(/"/g, '""')}"`;
            }
            return val;
        }).join(','))
    ].join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${filename}.csv`;
    link.click();
    URL.revokeObjectURL(url);
    
    showToast('Exportação concluída!', 'success');
}

/* ==========================================================================
   Tab Functions
   ========================================================================== */

/**
 * Mudar para uma aba específica
 */
function switchTab(tabId) {
    // Remover classe active de todas as tabs
    document.querySelectorAll('.nav-link').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Adicionar classe active à tab clicada
    const activeTab = document.querySelector(`[data-bs-target="#${tabId}"], [onclick*="${tabId}"]`);
    if (activeTab) {
        activeTab.classList.add('active');
    }
    
    // Ocultar todos os panes
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('show', 'active');
    });
    
    // Mostrar o pane atual
    const currentPane = document.getElementById(tabId);
    if (currentPane) {
        currentPane.classList.add('show', 'active');
    }
}

/**
 * Avançar para a próxima aba
 */
function nextTab(nextTabId) {
    switchTab(nextTabId);
    
    // Atualizar indicador de progresso se existir
    const progressSteps = document.querySelectorAll('.progress-step');
    progressSteps.forEach(step => {
        step.classList.remove('active', 'completed');
    });
}

/**
 * Inicializar navegação de tabs
 */
function initTabs(tabId = 'clienteTabs') {
    const tabEl = document.getElementById(tabId);
    if (!tabEl || !window.bootstrap) return;
    
    new bootstrap.Tab(tabEl);
}

/* ==========================================================================
   Search/Filter Functions
   ========================================================================== */

/**
 * Debounce para busca
 */
function debounce(func, wait = 300) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Inicializar busca com debounce
 */
function initSearch(inputId, searchFunction, delay = 300) {
    const input = document.getElementById(inputId);
    if (!input) return;
    
    input.addEventListener('input', debounce(searchFunction, delay));
}

/**
 * Limpar campos de busca
 */
function clearSearch(inputs = []) {
    inputs.forEach(inputId => {
        const input = document.getElementById(inputId);
        if (input) input.value = '';
    });
    
    // Trigger change event para atualizar resultados
    inputs.forEach(inputId => {
        const input = document.getElementById(inputId);
        if (input) input.dispatchEvent(new Event('input'));
    });
}

/* ==========================================================================
   Auth Functions
   ========================================================================== */

/**
 * Verificar autenticação
 */
async function checkAuth() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login';
        return false;
    }
    
    try {
        const response = await fetch('/api/v1/usuarios/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            localStorage.removeItem('access_token');
            window.location.href = '/login';
            return false;
        }
        
        CRM.state.user = await response.json();
        return true;
    } catch (error) {
        console.error('Auth check failed:', error);
        localStorage.removeItem('access_token');
        window.location.href = '/login';
        return false;
    }
}

/**
 * Fazer logout
 */
function logout() {
    localStorage.removeItem('access_token');
    window.location.href = '/login';
}

/* ==========================================================================
   Initialization
   ========================================================================== */

/**
 * Inicializar quando o DOM estiver pronto
 */
document.addEventListener('DOMContentLoaded', () => {
    // Inicializar tooltips
    initTooltips();
    
    // Inicializar dropdowns
    initDropdowns();
    
    // Carregar preferências do usuário
    loadUserPreferences();
});

function initTooltips() {
    if (!window.bootstrap) return;
    
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}

function initDropdowns() {
    if (!window.bootstrap) return;
    
    const dropdownElementList = document.querySelectorAll('.dropdown-toggle');
    [...dropdownElementList].map(dropdownToggleEl => new bootstrap.Dropdown(dropdownToggleEl));
}

function loadUserPreferences() {
    // Carregar tema preferido (futuro)
    const theme = localStorage.getItem('theme');
    if (theme) {
        document.body.classList.add(`theme-${theme}`);
    }

    const density = localStorage.getItem('density');
    if (density) {
        document.body.classList.add(`density-${density}`);
    }
}

/* ==========================================================================
   Error Handling
   ========================================================================== */

/**
 * Mostrar mensagem de erro amigável
 */
function showError(message, title = 'Erro') {
    showToast(message, 'error');
    console.error(`${title}: ${message}`);
}

/**
 * Tratar erros de rede
 */
function handleNetworkError(error) {
    showToast(error.message || 'Erro de conexão', 'error');
}

/* ==========================================================================
   Animation Keyframes (inline for portability)
   ========================================================================== */
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);
