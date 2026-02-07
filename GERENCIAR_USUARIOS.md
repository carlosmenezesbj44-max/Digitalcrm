# Gerenciamento de Usuários

## Acessar a Página

**URL**: http://localhost:8001/usuarios

⚠️ **Requer autenticação como Admin**

## Recursos

### 1. Visualizar Usuários
- Lista completa de todos os usuários do sistema
- Filtrar por username
- Filtrar por role (admin, gerente, técnico, cliente)

### 2. Criar Novo Usuário
Clique em "+ Novo Usuário" e preencha:
- **Username**: Identificador único (mínimo 3 caracteres)
- **Email**: Endereço de email válido (único)
- **Nome Completo**: Nome do usuário
- **Senha**: Mínimo 8 caracteres
- **Role**: admin, gerente, técnico ou cliente
- **Ativo**: Checkbox para ativar/desativar

### 3. Editar Usuário
1. Clique no botão "Editar" na linha do usuário
2. Modifique:
   - Email
   - Nome Completo
   - Status (Ativo/Inativo)
3. Clique "Salvar"

### 4. Deletar Usuário
1. Clique no botão "Deletar" na linha do usuário
2. Confirme a exclusão

## Roles e Permissões

| Role | Descrição | Acesso |
|------|-----------|--------|
| **Admin** | Administrador do sistema | Acesso total, pode gerenciar todos |
| **Gerente** | Gerente de operações | Acesso a relatórios e clientes |
| **Técnico** | Técnico de suporte | Acesso a ordens de serviço |
| **Cliente** | Cliente final | Acesso limitado ao próprio perfil |

## API Endpoints

### Listar Usuários
```bash
GET /api/usuarios/lista
Authorization: Bearer {token}
```

### Obter Usuário por ID
```bash
GET /api/usuarios/{usuario_id}
Authorization: Bearer {token}
```

### Registrar Novo Usuário
```bash
POST /api/usuarios/registrar
Content-Type: application/json

{
  "username": "novo_usuario",
  "email": "novo@example.com",
  "nome_completo": "Nome do Usuário",
  "senha": "senha123456",
  "role": "cliente"
}
```

### Editar Usuário
```bash
PUT /api/usuarios/{usuario_id}/editar
Authorization: Bearer {token}
Content-Type: application/json

{
  "email": "novo_email@example.com",
  "nome_completo": "Nome Atualizado",
  "ativo": true
}
```

### Deletar Usuário
```bash
DELETE /api/usuarios/{usuario_id}
Authorization: Bearer {token}
```

### Login
```bash
POST /api/usuarios/login
Content-Type: application/json

{
  "username": "admin",
  "senha": "senha123456"
}

# Resposta
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "usuario": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "nome_completo": "Administrador",
    "role": "admin",
    "ativo": true,
    "criado_em": "2026-01-18T...",
    "ultimo_acesso": null,
    "permissoes": []
  }
}
```

### Obter Perfil Autenticado
```bash
GET /api/usuarios/me
Authorization: Bearer {token}
```

## Exemplo com cURL

### Criar usuário
```bash
curl -X POST "http://localhost:8001/api/usuarios/registrar" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao",
    "email": "joao@example.com",
    "nome_completo": "João Silva",
    "senha": "senha123456",
    "role": "tecnico"
  }'
```

### Listar usuários
```bash
curl -X GET "http://localhost:8001/api/usuarios/lista" \
  -H "Authorization: Bearer seu_token_aqui"
```

### Editar usuário
```bash
curl -X PUT "http://localhost:8001/api/usuarios/2/editar" \
  -H "Authorization: Bearer seu_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "novo_email@example.com",
    "nome_completo": "Novo Nome",
    "ativo": true
  }'
```

## Segurança

- ✅ Senhas criptografadas com bcrypt (12 rounds)
- ✅ Tokens JWT com expiração de 24h
- ✅ Validação de permissões por role
- ✅ Auditoria de login (IP registrado)
- ✅ Usuários inativos não conseguem fazer login

## Dicas

1. **Primeira Vez**: Crie um usuário admin para gerenciar o sistema
2. **Segurança**: Use senhas fortes (mínimo 8 caracteres)
3. **Filtros**: Use os filtros para encontrar rapidamente um usuário
4. **Auditoria**: Todos os logins são registrados com timestamp e IP
5. **Permissões**: Apenas admins podem acessar a página de gerenciamento

## Troubleshooting

### "Acesso restrito a administradores"
- Faça login com uma conta admin
- Se necessário, peça ao admin para promover sua conta

### "Token inválido ou expirado"
- Faça login novamente para gerar um novo token
- Token expira a cada 24 horas

### "Email já está registrado"
- Cada email deve ser único
- Use um email diferente ou edite o usuário existente

### Usuário não consegue fazer login
- Verifique se o usuário está ativo
- Verifique username e senha
- Confira se o email foi confirmado (se aplicável)
