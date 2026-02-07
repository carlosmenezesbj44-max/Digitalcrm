# Tutorial de Sincronização com MikroTik

Este tutorial ensina como configurar e usar a sincronização com MikroTik no CRM Provedor.

## 📋 Pré-requisitos

- MikroTik configurado e acessível via API
- Porta 8728 aberta no MikroTik
- Credenciais de administrador do MikroTik
- CRM Provedor instalado e configurado

## 🔧 Configuração Inicial

### 1. Configurar o MikroTik

No WinBox ou via terminal, configure o acesso à API:

```bash
# Habilitar API
/ip service set api disabled=no port=8728

# Verificar se está ativo
/ip service print
```

### 2. Configurar o .env

Edite o arquivo `.env` na raiz do projeto:

```env
# Configurações do MikroTik
MIKROTIK_HOST=192.168.1.1
MIKROTIK_USER=admin
MIKROTIK_PASSWORD=sua_senha_aqui
```

### 3. Configurar Servidor no Banco de Dados (Opcional)

Se preferir configurar via banco de dados:

```sql
INSERT INTO servidores (nome, ip, tipo_conexao, tipo_acesso, usuario, senha, ativo) 
VALUES ('MikroTik Principal', '192.168.1.1', 'mikrotik', 'api', 'admin', 'sua_senha', 1);
```

## 🚀 Como Sincronizar Clientes

### Via Dashboard (Interface Web)

1. **Acesse o Dashboard**
   - Abra o navegador e vá para `http://localhost:8000`
   - Faça login com suas credenciais

2. **Cadastre um Cliente**
   - No menu lateral, clique em "Cadastros" → "Novo Cliente"
   - Preencha os dados do cliente
   - Salve o cadastro

3. **Crie um Contrato**
   - No menu lateral, clique em "Provedor" → "Contratos"
   - Clique em "Novo Contrato"
   - Selecione o cliente criado
   - Preencha os dados do contrato:
     - Plano de internet
     - Velocidade de download/upload
     - Senha PPPoE
   - Salve o contrato

4. **Sincronize com MikroTik**
   - Após salvar o contrato, o sistema sincronizará automaticamente
   - Ou manualmente via API: `POST /api/v1/mikrotik/contratos/{id}/sync`

### Via API REST

#### Criar Profile PPPoE

```bash
curl -X POST "http://localhost:8000/api/v1/mikrotik/profiles" \
  -H "Authorization: Bearer seu_token_jwt" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "premium",
    "download_limit": 100,
    "upload_limit": 50
  }'
```

#### Sincronizar Cliente

```bash
curl -X POST "http://localhost:8000/api/v1/mikrotik/clients/sync" \
  -H "Authorization: Bearer seu_token_jwt" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": 1,
    "contrato_id": 1
  }'
```

#### Sincronizar Contrato

```bash
curl -X POST "http://localhost:8000/api/v1/mikrotik/contratos/1/sync" \
  -H "Authorization: Bearer seu_token_jwt"
```

## 📊 Monitoramento

### Visualizar Logs do MikroTik

```bash
# Logs do servidor padrao
curl -X GET "http://localhost:8000/api/v1/mikrotik/logs?limit=10" \
  -H "Authorization: Bearer seu_token_jwt"

# Logs de um servidor especifico (usando servidor_id)
curl -X GET "http://localhost:8000/api/v1/mikrotik/logs?limit=10&servidor_id=3" \
  -H "Authorization: Bearer seu_token_jwt"
```

### Verificar Sessões Ativas

```bash
# Sessoes do servidor padrao
curl -X GET "http://localhost:8000/api/v1/mikrotik/sessions" \
  -H "Authorization: Bearer seu_token_jwt"

# Sessoes de um servidor especifico
curl -X GET "http://localhost:8000/api/v1/mikrotik/sessions?servidor_id=3" \
  -H "Authorization: Bearer seu_token_jwt"
```

### Listar Servidores MikroTik

```bash
# Lista todos os servidores MikroTik cadastrados
curl -X GET "http://localhost:8000/api/v1/mikrotik/servers" \
  -H "Authorization: Bearer seu_token_jwt"
```

### Status do MikroTik

```bash
# Status do servidor padrao
curl -X GET "http://localhost:8000/api/v1/mikrotik/status" \
  -H "Authorization: Bearer seu_token_jwt"

# Status de um servidor especifico
curl -X GET "http://localhost:8000/api/v1/mikrotik/status?servidor_id=3" \
  -H "Authorization: Bearer seu_token_jwt"
```

## 🔒 Gerenciamento de Clientes

### Bloquear Cliente

```bash
curl -X POST "http://localhost:8000/api/v1/mikrotik/clients/block" \
  -H "Authorization: Bearer seu_token_jwt" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "cliente_teste_1"
  }'
```

### Desbloquear Cliente

```bash
curl -X POST "http://localhost:8000/api/v1/mikrotik/clients/unblock" \
  -H "Authorization: Bearer seu_token_jwt" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "cliente_teste_1"
  }'
```

### Atualizar Credenciais

```bash
curl -X PUT "http://localhost:8000/api/v1/mikrotik/clients/credentials" \
  -H "Authorization: Bearer seu_token_jwt" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "cliente_teste_1",
    "new_password": "nova_senha_segura",
    "new_profile": "premium"
  }'
```

## 🖥️ Suporte a Múltiplos Servidores

O sistema agora suporta múltiplos servidores MikroTik!

### Adicionar Novo Servidor

Para adicionar um novo servidor MikroTik ao sistema:

1. **Via Interface Web:**
   - Acesse **Cadastros** → **Novo Servidor**
   - Preencha os dados:
     - Nome: "Filial SP"
     - IP: "200.200.1.2"
     - Tipo de Conexão: "mikrotik"
     - Tipo de Acesso: "api"
     - Usuário e Senha do MikroTik
   - Salve o servidor

2. **Via Banco de Dados:**
```sql
INSERT INTO servidores (nome, ip, tipo_conexao, tipo_acesso, usuario, senha, ativo)
VALUES ('Filial SP', '200.200.1.2', 'mikrotik', 'api', 'admin', 'senha123', 1);
```

### Selecionar Servidor

- Na interface web, há um dropdown para selecionar qual servidor visualizar
- Na API, use o parâmetro `servidor_id` para especificar qual servidor consultar

### Servidores Cadastrados

```bash
# Listar todos os servidores MikroTik
python debug_db.py

# Ou via API:
curl -X GET "http://localhost:8000/api/v1/mikrotik/servers" \
  -H "Authorization: Bearer seu_token_jwt"
```

## 🐛 Resolução de Problemas

### Erro: "MikroTik não configurado"

**Causa:** As variáveis de ambiente não estão definidas corretamente.

**Solução:**
1. Verifique o arquivo `.env`
2. Confira se as credenciais estão corretas
3. Reinicie o servidor

### Erro: "Conexão recusada"

**Causa:** Porta 8728 bloqueada ou MikroTik inacessível.

**Solução:**
1. Verifique se a API está habilitada no MikroTik
2. Confira o firewall
3. Teste a conexão com `telnet 192.168.1.1 8728`

### Erro: "Credenciais inválidas"

**Causa:** Usuário ou senha incorretos.

**Solução:**
1. Verifique as credenciais no MikroTik
2. Teste o login via WinBox
3. Atualize o `.env` com credenciais corretas

### Erro: "Logs não estão sendo coletados"

**Causa 1:** O usuário não tem permissão para ler logs no MikroTik.

**Solução:**
1. No MikroTik, vá em **System** → **Users**
2. Verifique se o usuário tem a policy **read** habilitada
3. Ou adicione o usuário ao grupo **full** temporariamente para teste

**Causa 2:** Os logs estão desabilitados no MikroTik.

**Solução:**
1. No MikroTik, vá em **System** → **Logging**
2. Verifique se há regras de log ativas
3. Adicione uma regra para registrar eventos importantes:
```bash
/system logging add topics=info action=memory
/system logging add topics=warning action=memory
/system logging add topics=error action=memory
```

**Causa 3:** Não há logs registrados ainda.

**Solução:**
1. Gere algum tráfego ou evento no MikroTik
2. Aguarde alguns segundos para os logs serem gerados
3. Tente novamente coletar os logs

### Erro: "Profile já existe"

**Causa:** O profile já foi criado anteriormente.

**Solução:** O sistema atualiza automaticamente o profile existente.

## 📈 Fluxo de Trabalho Recomendado

### 1. Configuração Inicial
```mermaid
graph TD
    A[Configurar MikroTik] --> B[Configurar .env]
    B --> C[Iniciar CRM]
    C --> D[Testar conexão]
```

### 2. Cadastro de Novo Cliente
```mermaid
graph TD
    A[Cadastrar Cliente] --> B[Criar Contrato]
    B --> C[Sincronizar com MikroTik]
    C --> D[Verificar no MikroTik]
```

### 3. Gerenciamento de Clientes
```mermaid
graph TD
    A[Verificar Sessões] --> B{Cliente Ativo?}
    B -->|Sim| C[Monitorar]
    B -->|Não| D[Bloquear/Desbloquear]
    D --> E[Atualizar Status]
```

## 🛠️ Comandos Úteis

### Testar Conexão Manualmente

```python
from crm_modules.mikrotik.services import MikrotikService

service = MikrotikService()
result = service.obter_configuracoes()
print(result)
```

### Verificar Logs no Terminal

```bash
# Iniciar o servidor com logs detalhados
python -m uvicorn interfaces.api.main:app --host 0.0.0.0 --port 8000 --log-level debug
```

### Testar API Localmente

```bash
# Testar status
curl -X GET "http://localhost:8000/api/v1/mikrotik/status"

# Testar criação de profile
curl -X POST "http://localhost:8000/api/v1/mikrotik/profiles" \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "download_limit": 10, "upload_limit": 5}'
```

## 📞 Suporte

Se encontrar problemas:

1. **Verifique os logs** do CRM
2. **Teste a conexão** com o MikroTik
3. **Consulte o dashboard** para status
4. **Use os endpoints** de teste

### Comandos de Diagnóstico

```bash
# Testar conexão com MikroTik via script
python test_mikrotik_connection.py

# Testar coleta de logs via script
python test_mikrotik_logs.py

# Verificar status do MikroTik via API
curl -X GET "http://localhost:8000/api/v1/mikrotik/status"

# Verificar logs recentes via API
curl -X GET "http://localhost:8000/api/v1/mikrotik/logs?limit=5"

# Testar criação de profile
curl -X POST "http://localhost:8000/api/v1/mikrotik/profiles" \
  -H "Content-Type: application/json" \
  -d '{"name": "diagnostico", "download_limit": 1, "upload_limit": 1}'
```

## ✅ Checklist de Configuração

- [ ] MikroTik com API habilitada na porta 8728
- [ ] Credenciais de administrador corretas
- [ ] Usuário com permissão de leitura (policy: read)
- [ ] Logging habilitado no MikroTik (System → Logging)
- [ ] Arquivo `.env` configurado
- [ ] CRM Provedor iniciado
- [ ] Teste de conexão realizado
- [ ] Teste de coleta de logs realizado
- [ ] Primeiro cliente sincronizado
- [ ] Dashboard acessível
- [ ] Logs sendo coletados

Pronto! Agora você tem tudo configurado para sincronizar clientes com o MikroTik de forma automática e em tempo real.