# ✅ Checklist Executivo: Melhorias UI/UX

## 📊 Prioridade & Impacto

| Tarefa | Impacto | Dificuldade | Horas | Status |
|--------|--------|------------|-------|--------|
| Design System CSS | 🔴 CRÍTICO | ⭐ Fácil | 2 | ⬜ |
| Sidebar Nova | 🔴 CRÍTICO | ⭐ Fácil | 3 | ⬜ |
| Atualizar 36 Templates | 🟠 ALTO | ⭐ Fácil | 6 | ⬜ |
| Dashboard Executivo | 🟠 ALTO | ⭐⭐ Médio | 6 | ⬜ |
| Tabelas Avançadas | 🟠 ALTO | ⭐⭐ Médio | 4 | ⬜ |
| Formulários Modern | 🟡 MÉDIO | ⭐⭐ Médio | 5 | ⬜ |
| Login Premium | 🟡 MÉDIO | ⭐ Fácil | 3 | ⬜ |
| Mobile Responsivo | 🟡 MÉDIO | ⭐⭐⭐ Difícil | 4 | ⬜ |
| QA & Testes | 🟢 BAIXO | ⭐ Fácil | 3 | ⬜ |

**Total Estimado: 36-40 horas**

---

## 🚀 SEMANA 1: Foundation

### Dia 1: Design System (2-3 horas)

#### Manhã (1-2h)
- [ ] Criar arquivo `static/css/design-system.css`
- [ ] Definir variáveis CSS (cores, spacing, tipografia)
- [ ] Testar no browser (F12)
- [ ] Commit git: "feat: add design system foundation"

**Arquivo que será criado:**
```
interfaces/web/static/css/design-system.css (500+ linhas)
```

**Checklist Interno:**
```
Cores Primárias:
  [ ] --primary-dark: #1a252f
  [ ] --primary-color: #2c3e50
  [ ] --accent-color: #3498db
  
Cores Semânticas:
  [ ] --success-color: #27ae60
  [ ] --warning-color: #f39c12
  [ ] --danger-color: #e74c3c
  
Espacamento:
  [ ] --spacing-xs/sm/md/lg/xl
  
Tipografia:
  [ ] Font-family padrão
  [ ] Font sizes (xs, sm, base, lg, xl, xxl)
  
Shadows:
  [ ] Shadow-sm/md/lg
  
Border Radius:
  [ ] Radius-sm/md/lg
```

#### Tarde (1h)
- [ ] Importar em 3 templates teste (login.html, index.html, clientes.html)
- [ ] Remover `<style>` inline desses 3 templates
- [ ] Verificar se CSS não quebrou nada
- [ ] Commit: "refactor: import design-system in test templates"

---

### Dia 2-3: Sidebar Nova (6 horas)

#### Dia 2 Manhã (2-3h) - Code
- [ ] Escrever HTML nova sidebar (287 linhas)
- [ ] Escrever CSS para sidebar
- [ ] Escrever JavaScript para toggle de menus
- [ ] Testar em 1 template (clientes.html)
- [ ] Ajustar main-content margin (250px → 280px)
- [ ] Teste Mobile (F12, responsive)

**Estrutura da Nova Sidebar:**
```
sidebar/
├── sidebar-header (logo)
├── user-section (avatar + nome)
├── sidebar-nav (PRINCIPAL, GERENCIAMENTO, FINANCEIRO, MAIS)
│   ├── menu-group
│   │   ├── menu-group-title
│   │   ├── nav-item (colapsível)
│   │   └── submenu
│   │       └── nav-sub-item
└── sidebar-footer (configurações, logout)
```

**Checklist JS:**
```
toggleSubmenu():
  [ ] Toggle classe 'active' no submenu
  [ ] Fechar outros submenus abertos
  [ ] Rotacionar ícone chevron
  [ ] Max-height animation
  
DOMContentLoaded:
  [ ] Detectar nav-item.active
  [ ] Abrir submenu pai automaticamente
  [ ] Scroll para item ativo
```

#### Dia 2 Tarde (1-2h) - QA
- [ ] Testar todos os submenus
- [ ] Testar mobile (375px)
- [ ] Testar tablet (768px)
- [ ] Testar scroll de menu longo
- [ ] Verificar acessibilidade (TAB, ENTER)

#### Dia 3: Duplicação (3h)
- [ ] Script/Manual para copiar nova sidebar em todos 36 templates
- [ ] Verificar cada tipo de template (novo_*, listar, detalhes)
- [ ] Ajustar main-content em todos
- [ ] Commit: "refactor: update sidebar in all templates"

**Templates críticos a testar primeiro:**
```
✅ clientes.html (tabela + novo)
✅ novo_cliente.html (multi-step form)
✅ index.html (dashboard)
✅ login.html (sem sidebar)
✅ contratos.html (cards)
```

---

### Dia 4: Ajustes de Cores (2-3 horas)

- [ ] Identificar todas as cores hardcoded nos templates
- [ ] Substituir por variáveis CSS
- [ ] Testar contraste (acessibilidade)
- [ ] Commit: "refactor: use CSS variables for colors"

**Buscar & Substituir:**
```
#0d47a1 → var(--primary-dark)
#1565c0 → var(--primary-light)
#667eea → var(--accent-color)
#764ba2 → var(--accent-dark)
#28a745 → var(--success-color)
#f39c12 → var(--warning-color)
#e74c3c → var(--danger-color)
```

**Checklist:**
```
Arquivos a revisar:
  [ ] index.html
  [ ] clientes.html
  [ ] novo_cliente.html
  [ ] contratos.html
  [ ] novo_cliente.html
  [ ] login.html
  [ ] todos os outros 30 templates
```

---

### Dia 5: Teste Geral (1-2 horas)

- [ ] Rodar aplicação em localhost
- [ ] Testar TODOS os links do menu
- [ ] Testar submenu collapse/expand em 5 páginas diferentes
- [ ] Testar mobile em 3 resoluções (375px, 768px, 1024px)
- [ ] Testar em 2 navegadores (Chrome, Firefox)
- [ ] Verificar console.log para erros
- [ ] Commit: "test: foundation week complete"

**Teste Checklist:**
```
Login:
  [ ] Fazer login
  [ ] Verificar menu expandido
  [ ] Verificar usuário na sidebar
  
Dashboard:
  [ ] KPI cards aparecem
  [ ] Gráficos carregam
  [ ] Menu ativo = Dashboard
  
Clientes:
  [ ] Tabela renderiza
  [ ] Busca funciona
  [ ] Menu ativo = Clientes
  [ ] Sidebar colapsível

Novo Cliente:
  [ ] Formulário multi-step funciona
  [ ] Validação em tempo real
  [ ] Salvar cliente
  [ ] Redirect para lista

Mobile (375px):
  [ ] Sidebar colapsa para 60px
  [ ] Ícones visíveis
  [ ] Conteúdo não overflow
  [ ] Tabelas não quebram
```

---

## 🎨 SEMANA 2: Componentes

### Dia 6-7: Dashboard Executivo (6 horas)

#### Dia 6 (3h) - KPI Cards

**Arquivo:** `templates/index.html`

**Checklist:**
```
KPI Cards:
  [ ] Layout grid responsivo (4 cols)
  [ ] Ícones de trending (↑ ↓)
  [ ] Cores de status (success, warning, danger)
  [ ] Hover effect com transform
  [ ] Mini gráficos (Chart.js)
  [ ] Comparação período anterior
  [ ] Responsividade (1 col em mobile)
  
CSS:
  [ ] Gradient top border (4px)
  [ ] Box-shadow on hover
  [ ] Animation smooth
  [ ] Accessibility (color + icon)
```

**Exemplo HTML:**
```html
<div class="kpi-card">
  <div class="kpi-header">
    <h3>Receita Total</h3>
    <span class="kpi-period">Últimos 30 dias</span>
  </div>
  <div class="kpi-body">
    <div class="kpi-value">R$ 125.430</div>
    <div class="kpi-comparison positive">
      <i class="bi bi-graph-up"></i>
      <span>+12.5% vs mês anterior</span>
    </div>
  </div>
  <div class="kpi-chart">
    <canvas id="revenueMiniChart"></canvas>
  </div>
</div>
```

#### Dia 6 Tarde (3h) - Gráficos

**Checklist:**
```
Charts (Chart.js):
  [ ] Revenue Chart (Line)
  [ ] Growth Chart (Line)
  [ ] Distribution Chart (Pie)
  [ ] Status Chart (Doughnut)
  [ ] Tooltip on hover
  [ ] Legend visible
  [ ] Responsive canvas
  [ ] Cores do Design System
  [ ] Mock data fallback
  
Layout:
  [ ] 2x2 grid desktop
  [ ] 1x4 mobile
  [ ] Gaps consistentes
  [ ] Cards iguais em altura
```

#### Dia 7 (3h) - Insights & Polish

**Checklist:**
```
Alertas:
  [ ] Alert box para contratos vencendo
  [ ] Success message para crescimento
  [ ] Warning colors corretas
  [ ] Ícones adequados
  [ ] Links acionáveis
  
Date Range:
  [ ] Input date picker
  [ ] Filtro por período
  [ ] Aplicar botão
  [ ] Recarregar dados
  
Dados:
  [ ] API endpoint ou mock
  [ ] Tratamento de erro
  [ ] Loading spinner
  [ ] Refresh automático 5 min
```

---

### Dia 8: Tabelas Avançadas (4 horas)

**Arquivo:** `templates/clientes.html`, `contratos.html`, `ordens_servico.html`

#### Manhã (2h) - Toolbar

**Checklist:**
```
Busca:
  [ ] Input com ícone search
  [ ] Debounce 300ms
  [ ] Clear button
  [ ] Placeholder relevante
  
Filtros:
  [ ] Dropdown de status
  [ ] Múltiplos filtros
  [ ] Dropdown avançado (trigger)
  [ ] Apply button
  
Ações:
  [ ] Export CSV
  [ ] Sort direction
  [ ] View toggle (table/cards)
  [ ] Refresh data
```

#### Tarde (2h) - Table & Pagination

**Checklist:**
```
Tabela:
  [ ] Header sticky (CSS position sticky)
  [ ] Sortable columns (onclick)
  [ ] Sortable icons (⬆ ⬇)
  [ ] Hover effect em rows
  [ ] Status badges com cores
  [ ] Truncate de textos longos
  [ ] Icons de ações (edit, delete, etc)
  [ ] Dropdown de mais ações
  
Paginação:
  [ ] Números de página
  [ ] Botões Anterior/Próximo
  [ ] Página atual highlighted
  [ ] Info "Mostrando 1-20 de 150"
  [ ] Onclick handlers
  [ ] Desabilitar prev em página 1
  [ ] Desabilitar next em última página
  
Responsividade:
  [ ] d-none d-md-table-cell para colunas
  [ ] Cards view em mobile
  [ ] Swipe para ações?
```

---

### Dia 9: Formulários Modernos (5 horas)

**Arquivo:** `templates/novo_cliente.html`, `novo_contrato.html`, `novo_tecnico.html`

#### Manhã (2h) - Progress Indicator

**Checklist:**
```
Visual:
  [ ] 3-5 steps círculos
  [ ] Linha conectando steps
  [ ] Step label
  [ ] Ícone de check em step completo
  [ ] Cor diferente para step ativo
  [ ] Animação suave

Interação:
  [ ] Clicável em steps (ir para trás)
  [ ] Next button vai para próximo
  [ ] Validação antes de avançar
  [ ] Desabilitar back em step 1
```

#### Tarde (3h) - Form Validation

**Checklist:**
```
Validação Real-time:
  [ ] Required fields (*)
  [ ] Email format
  [ ] CPF format & validation
  [ ] Telefone mask
  [ ] Data format
  [ ] Campo ativo = highlight
  [ ] Campo inválido = red border
  [ ] Campo válido = green icon
  [ ] Help text (small)
  [ ] Error message em vermelho
  [ ] Success message em verde
  
Máscaras:
  [ ] CPF: 000.000.000-00
  [ ] Telefone: (00) 00000-0000
  [ ] CEP: 00000-000
  [ ] Data: DD/MM/YYYY
  
Tab Navigation:
  [ ] Tab 1: Dados Básicos
  [ ] Tab 2: Endereço
  [ ] Tab 3: Contatos
  [ ] Tab 4: Confirmação
  [ ] Resumo em real-time
  [ ] Submit final
```

---

### Dia 10: Login Premium (3 horas)

**Arquivo:** `templates/login.html`

**Checklist:**
```
Design:
  [ ] Background gradient moderno
  [ ] Logo centr alizado
  [ ] Card com sombra
  [ ] Max-width: 450px
  [ ] Responsivo em mobile
  
Campos:
  [ ] Username/Email
  [ ] Password (com toggle show/hide)
  [ ] Icons nos campos (person, lock)
  [ ] Placeholder correto
  [ ] Required validation
  
Funcionalidades:
  [ ] "Manter conectado" checkbox
  [ ] "Esqueci minha senha" link
  [ ] Error message formatado
  [ ] Loading spinner no submit
  [ ] Redirect após sucesso
  
Footer:
  [ ] "Não tem conta? Criar"
  [ ] Links de suporte (Ajuda, Telefone)
  [ ] Links de documentação
```

---

## 🧪 SEMANA 3: QA & Deploy

### Dia 11: Responsividade (3-4 horas)

**Checklist Completo:**

```
Desktop (1920px):
  [ ] Sidebar 280px + content
  [ ] Tabelas com todas colunas
  [ ] 4-col grid em KPIs
  [ ] Modals centralizados
  [ ] Sem overflow horizontal

Tablet (768px):
  [ ] Sidebar 280px (não colapsado)
  [ ] Tabelas com colunas essenciais
  [ ] 2-col grid em KPIs
  [ ] Forms de 2 colunas
  [ ] Dropdown menus funcionam
  
Mobile (375px):
  [ ] Sidebar colapsado (60px)
  [ ] Menu expandível
  [ ] Tabelas em cards
  [ ] 1-col grid em KPIs
  [ ] Forms de 1 coluna
  [ ] Modals full-width
  [ ] Sem scroll horizontal
  [ ] Botões com 48px altura (acessibilidade)
  [ ] Touch targets adequados
```

**Teste Manual:**
- [ ] Chrome DevTools (F12) - Responsive Design Mode
- [ ] iPhone 12 (390x844)
- [ ] iPad (768x1024)
- [ ] Desktop Full (1920x1080)

**Teste em Browser Real:**
- [ ] Chrome (Desktop + Mobile)
- [ ] Firefox (Desktop + Mobile)
- [ ] Safari (se possível)
- [ ] Edge (se possível)

---

### Dia 12: Performance & Acessibilidade (2-3 horas)

**Performance:**
```
[ ] Minify CSS (production)
[ ] Lazy load images
[ ] Comprimir gráficos
[ ] Cache CSS/JS
[ ] Lighthouse score > 80
```

**Acessibilidade:**
```
[ ] Contrast ratio WCAG AA
[ ] Alt text em imagens
[ ] Labels em form inputs
[ ] ARIA labels em ícones
[ ] Navegação via TAB
[ ] Botões com :focus
[ ] Links distinguíveis (cor + underline)
[ ] Sem color only (use icon também)
```

**Testes:**
- [ ] Lighthouse (Chrome DevTools)
- [ ] Wave (WebAIM)
- [ ] axe DevTools

---

## 📈 Depois de Completo

### Documentação
- [ ] README atualizado com novas cores/componentes
- [ ] Componentes reusáveis documentados
- [ ] Guia de adição de novas páginas
- [ ] Exemplos de HTML/CSS para novos componentes

### Monitoramento
- [ ] Google Analytics (rastreamento de eventos)
- [ ] User feedback (Net Promoter Score)
- [ ] A/B test de novo design vs antigo
- [ ] Métricas de bounce rate

### Melhorias Futuras
- [ ] Dark mode (CSS variables facilitam!)
- [ ] Temas customizáveis
- [ ] Componentes storybook
- [ ] Design tokens Figma

---

## 📊 Planilha de Tempo Real

Copie isso em um editor (Trello, Notion, Excel):

```markdown
| Data | Tarefa | Esperado | Real | Status | Notas |
|------|--------|----------|------|--------|-------|
| 01/02 | Design System | 2h | - | ⬜ | |
| 01/02 | Importar em templates | 1h | - | ⬜ | |
| 02/02 | Sidebar Nova | 6h | - | ⬜ | |
| 03/02 | Duplicar Sidebar | 3h | - | ⬜ | |
| 04/02 | Ajustes de Cores | 2h | - | ⬜ | |
| 05/02 | Teste Geral | 2h | - | ⬜ | |
| 06/02 | Dashboard KPIs | 3h | - | ⬜ | |
| 06/02 | Dashboard Charts | 3h | - | ⬜ | |
| 07/02 | Dashboard Insights | 3h | - | ⬜ | |
| 08/02 | Tabelas Avançadas | 4h | - | ⬜ | |
| 09/02 | Forms Multi-step | 5h | - | ⬜ | |
| 10/02 | Login Premium | 3h | - | ⬜ | |
| 11/02 | Responsividade | 3h | - | ⬜ | |
| 12/02 | Performance & A11y | 2h | - | ⬜ | |
| **TOTAL** | | **42h** | - | | |
```

---

## 🎯 Marcos (Milestones)

### ✅ Marco 1: Foundation (Fim Semana 1)
- [x] Design System funcional
- [x] Sidebar nova em todos templates
- [x] Cores centralizadas
- [ ] **Resultado:** CRM visualmente coeso

### ✅ Marco 2: Componentes (Fim Semana 2)
- [ ] Dashboard executivo
- [ ] Tabelas avançadas
- [ ] Formulários multi-step
- [ ] Login premium
- [ ] **Resultado:** CRM com componentes profissionais

### ✅ Marco 3: Polimento (Fim Semana 3)
- [ ] Responsividade testada
- [ ] Performance otimizada
- [ ] Acessibilidade WCAG AA
- [ ] Documentação completa
- [ ] **Resultado:** CRM production-ready

---

## 🚨 Possíveis Armadilhas

| Armadilha | Como Evitar | Impacto |
|-----------|------------|--------|
| Quebrar links do menu | Testar cada submenu | Alto |
| CSS conflicts com Bootstrap | Testar antes de merge | Alto |
| Sidebar não colapsvel em mobile | Testar F12 responsive | Médio |
| Formulários não validam | Testar cada campo | Médio |
| Gráficos não carregam | Mock data fallback | Médio |
| Charts.js não instanciado | Verificar DOM ready | Baixo |
| Sem feedback visual em loading | Adicionar spinner | Baixo |

---

## ✨ Pronto?

1. Copie este checklist
2. Comece pelo Dia 1
3. Marque ✅ conforme completa
4. Reporte bloqueadores imediatamente

**Estimativa: 36-42 horas em 3 semanas**

Boa sorte! 🚀
