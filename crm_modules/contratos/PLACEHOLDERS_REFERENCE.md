# 🔍 Referência Completa de Placeholders

## Como Usar Este Documento

Ao editar um template, copie e cole os placeholders abaixo.

---

## 📋 CONTRATO

### IDs
```jinja2
{{ contrato_id }}              {# ID único do contrato #}
{{ cliente_id }}               {# ID do cliente #}
```

### Texto
```jinja2
{{ contrato_titulo }}          {# Ex: "Plano Internet 100MB" #}
{{ contrato_descricao }}       {# Descrição completa do serviço #}
{{ contrato_tipo }}            {# Ex: "servico", "assinatura" #}
```

### Valores Financeiros
```jinja2
{{ contrato_valor }}           {# Formatado: "R$ 99,90" #}
{{ contrato_valor_numero }}    {# Número puro: 99.90 #}
```

### Datas
```jinja2
{{ data_vigencia_inicio }}     {# Formato: "01/01/2024" #}
{{ data_vigencia_fim }}        {# Formato: "31/12/2024" #}
{{ data_criacao }}             {# Quando contrato foi criado #}
{{ data_atual }}               {# Data de geração do PDF #}
```

---

## 👤 CLIENTE

### Identificação
```jinja2
{{ cliente_nome }}             {# Nome completo ou razão social #}
{{ cliente_cpf }}              {# "000.000.000-00" #}
{{ cliente_cnpj }}             {# "00.000.000/0000-00" #}
```

### Contato
```jinja2
{{ cliente_endereco }}         {# "Rua X, 123, Centro, Cidade" #}
{{ cliente_telefone }}         {# "(11) 99999-9999" #}
{{ cliente_email }}            {# "cliente@email.com" #}
```

---

## 🏢 EMPRESA

### Identificação
```jinja2
{{ empresa_nome }}             {# Nome da sua empresa #}
{{ empresa_cnpj }}             {# CNPJ da empresa #}
```

### Contato
```jinja2
{{ empresa_endereco }}         {# Endereço completo #}
{{ empresa_telefone }}         {# Telefone para contato #}
{{ empresa_email }}            {# Email para contato #}
{{ empresa_logo }}             {# URL para imagem da logo #}
```

---

## 📝 Exemplos de Uso

### Cabeçalho Simples
```html
<h1>CONTRATO {{ contrato_id }}</h1>
<p>Data: {{ data_atual }}</p>
```

### Dados das Partes
```html
<p>
    <strong>Empresa:</strong> {{ empresa_nome }}<br/>
    <strong>CNPJ:</strong> {{ empresa_cnpj }}
</p>

<p>
    <strong>Cliente:</strong> {{ cliente_nome }}<br/>
    <strong>CPF:</strong> {{ cliente_cpf }}
</p>
```

### Valor e Datas
```html
<p>
    <strong>Serviço:</strong> {{ contrato_titulo }}<br/>
    <strong>Valor:</strong> {{ contrato_valor }}<br/>
    <strong>Período:</strong> {{ data_vigencia_inicio }} a {{ data_vigencia_fim }}
</p>
```

### Condicional (Pessoa ou Empresa)
```html
{% if cliente_cnpj != 'N/A' %}
    <p>Contratante: {{ cliente_nome }} (Empresa)</p>
    <p>CNPJ: {{ cliente_cnpj }}</p>
{% else %}
    <p>Contratante: {{ cliente_nome }} (Pessoa Física)</p>
    <p>CPF: {{ cliente_cpf }}</p>
{% endif %}
```

---

## ⚠️ Valores Padrão

Se um campo não estiver preenchido, usa-se:

| Placeholder | Valor Padrão |
|------------|-------------|
| `cliente_nome` | `"N/A"` |
| `cliente_cpf` | `"N/A"` |
| `cliente_cnpj` | `"N/A"` |
| `cliente_endereco` | `"N/A"` |
| `cliente_telefone` | `"N/A"` |
| `cliente_email` | `"N/A"` |
| `contrato_titulo` | `""` (vazio) |
| `contrato_descricao` | `""` (vazio) |
| `contrato_valor` | `"R$ 0,00"` |

---

## 🔧 Sintaxe Jinja2 Útil

### Comentários
```jinja2
{# Isto não aparecerá no PDF #}
```

### Condicionais
```jinja2
{% if cliente_cpf != 'N/A' %}
    CPF: {{ cliente_cpf }}
{% endif %}
```

### Loops (se dados suportam)
```jinja2
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
```

### Filtros
```jinja2
{{ texto|upper }}              {# Maiúsculas #}
{{ texto|lower }}              {# Minúsculas #}
{{ numero|int }}               {# Converte para inteiro #}
```

---

## 📞 Não Encontrou?

Se um placeholder que você precisa não está neste documento, você pode:

1. **Abrir uma issue** com a sugestão
2. **Editar `generator.py`** para adicionar o placeholder
3. **Consultar os logs** para ver quais placeholders foram enviados

---

**Última atualização:** Janeiro 2024
