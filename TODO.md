# TODO - Adicionar Gráficos ao Dashboard

## Status: Em Andamento

### ✅ Concluído
- [x] Análise do dashboard atual
- [x] Identificação dos campos de status dos clientes
- [x] Criação do plano de implementação

### 🔄 Em Andamento
- [ ] Adicionar métodos de gráfico no DashboardService
- [ ] Adicionar endpoints da API
- [ ] Atualizar frontend (HTML + JavaScript)

### 📋 Pendente
- [ ] Testar novos gráficos
- [ ] Verificar renderização no frontend

## Gráficos Implementados
1. **✅ Clientes Bloqueados** - Contar clientes com status_cliente == "bloqueio"
2. **✅ Status de Conexão** - Distribuição por status (conectado/pendencia/bloqueio)
3. **✅ Uptime de Conexão** - Tendência online/offline ao longo do tempo
4. **✅ Receita por Plano** - Receita gerada por cada plano de serviço

## Gráficos Sugeridos para Futuro
- 📊 Pagamentos em Atraso - Faturas vencidas vs pagas
- 🗺️ Distribuição Geográfica - Clientes por cidade/estado
- 📈 Backlog de Instalações - Ordens de serviço pendentes

## Arquivos a Modificar
- `crm_modules/dashboard/service.py`
- `crm_modules/dashboard/api.py`
- `interfaces/web/templates/index.html`
