# 📖 Guia Completo de Templates de Contratos

## Visão Geral

O sistema de contratos foi reorganizado para usar **templates HTML organizados** com Jinja2, facilitando:

- ✅ Criar novos tipos de contrato
- ✅ Modificar templates sem alterar código Python
- ✅ Reutilizar dados automaticamente
- ✅ Gerar PDFs profissionais

## 📍 Localização dos Templates

```
crm_modules/contratos/infrastructure/pdf/templates/
├── base.html        ← Template genérico (fallback)
├── servico.html     ← Contrato de Serviço
├── assinatura.html  ← Contrato de Assinatura
├── manutencao.html  ← Contrato de Manutenção
└── suporte.html     ← Contrato de Suporte
```

## 🔄 Como Funciona

### 1. Seleção de Template

Quando um contrato é criado, o sistema escolhe o template baseado em `tipo_contrato`:

```python
contrato = Contrato(
    tipo_contrato="servico",  # ← Procura: servico.html
    titulo="Plano Internet 100MB",
    cliente_id=1
)
```

Se o template específico não existir, usa `base.html`.

### 2. Preenchimento Automático

O gerador extrai dados do contrato e preenche os placeholders:

```html
<!-- No template -->
<p>Cliente: {{ cliente_nome }}</p>

<!-- No PDF resultante -->
<p>Cliente: João Silva</p>
```

### 3. Renderização para PDF

WeasyPrint converte HTML + dados → PDF pronto para download/impressão.

---

## 📝 Todos os Placeholders

### CONTRATO
```
{{ contrato_id }}              # ID único (ex: 123)
{{ contrato_titulo }}          # Título (ex: "Plano Internet 100MB")
{{ contrato_descricao }}       # Descrição detalhada
{{ contrato_tipo }}            # Tipo (servico/assinatura/etc)
{{ contrato_valor }}           # Valor formatado (ex: "R$ 99,90")
{{ contrato_valor_numero }}    # Número puro (ex: 99.90)
{{ data_vigencia_inicio }}     # Início (ex: "01/01/2024")
{{ data_vigencia_fim }}        # Fim (ex: "31/12/2024")
{{ data_criacao }}             # Quando foi criado
{{ data_atual }}               # Data de geração do PDF
```

### CLIENTE
```
{{ cliente_nome }}             # "João Silva"
{{ cliente_cpf }}              # "000.000.000-00"
{{ cliente_cnpj }}             # "00.000.000/0000-00" (se empresa)
{{ cliente_endereco }}         # "Rua X, 123, Centro"
{{ cliente_telefone }}         # "(11) 99999-9999"
{{ cliente_email }}            # "joao@email.com"
```

### EMPRESA
```
{{ empresa_nome }}             # Nome da sua empresa
{{ empresa_cnpj }}             # CNPJ da empresa
{{ empresa_endereco }}         # Endereço da empresa
{{ empresa_telefone }}         # Telefone para contato
{{ empresa_email }}            # Email para contato
{{ empresa_logo }}             # URL da logo (opcional)
```

---

## ✏️ Editando um Template

### Exemplo: Personalizar Contrato de Serviço

Abra: `crm_modules/contratos/infrastructure/pdf/templates/servico.html`

**Antes:**
```html
<p>CNPJ: {{ empresa_cnpj }}</p>
```

**Depois:**
```html
<p>
    <strong>CNPJ:</strong> {{ empresa_cnpj }}<br/>
    <strong>Inscrição Estadual:</strong> 123.456.789.012
</p>
```

Salve o arquivo. **Próximo contrato de serviço gerará com a mudança.**

---

## ➕ Criando um Novo Template

### Passo 1: Criar o arquivo

Novo arquivo: `contratos/infrastructure/pdf/templates/novo_tipo.html`

### Passo 2: Copiar estrutura base

Use qualquer template existente como referência.

### Passo 3: Personalizar

Adapte para seu tipo de contrato específico.

### Passo 4: Registrar o tipo

Adicione a enum em `domain/enums.py`:

```python
class TipoContrato(Enum):
    SERVICO = "servico"
    ASSINATURA = "assinatura"
    NOVO_TIPO = "novo_tipo"  # ← Novo
```

### Passo 5: Usar

```python
contrato = Contrato(
    tipo_contrato="novo_tipo",  # ← Sistema procurará novo_tipo.html
    titulo="...",
    ...
)
```

---

## 🎨 Dicas de Design

### CSS Funciona Normalmente

```html
<style>
    .header {
        text-align: center;
        margin-bottom: 30px;
        border-bottom: 2px solid #000;
    }
</style>
```

### Quebra de Página

```html
<div style="page-break-after: always;"></div>
```

### Formato de Moeda

Use `{{ contrato_valor }}` - já vem formatado como "R$ 99,90"

Se precisar só do número: `{{ contrato_valor_numero }}`

### Datas

Use `{{ data_vigencia_inicio }}` - já vem como "01/01/2024"

---

## 🔍 Exemplos Práticos

### Exemplo 1: Condicional (Se cliente for empresa)

```html
<p>
    {% if cliente_cnpj != 'N/A' %}
        CNPJ: {{ cliente_cnpj }}
    {% else %}
        CPF: {{ cliente_cpf }}
    {% endif %}
</p>
```

### Exemplo 2: Loop (Listar itens)

```html
<ul>
    {% for item in servicos %}
        <li>{{ item }}</li>
    {% endfor %}
</ul>
```

**Nota:** Para loops, você precisa passar dados no contexto.

### Exemplo 3: Data Formatada

```html
<!-- Sistema já formata automaticamente -->
<p>Válido até: {{ data_vigencia_fim }}</p>

<!-- Output -->
<p>Válido até: 31/12/2024</p>
```

---

## 🐛 Troubleshooting

### Placeholder não apareceu no PDF

**Causa:** Placeholder digitado errado ou não preenchido.

**Solução:**
1. Verifique ortografia exata
2. Verifique se o dados existe no contrato
3. Veja logs da aplicação

### Formatação quebrada no PDF

**Causa:** CSS ou HTML inválido.

**Solução:**
1. Teste o HTML em um navegador primeiro
2. Use classes simples (evite estilos inline complexos)
3. Teste em WeasyPrint: não suporta tudo que CSS3 suporta

### PDF em branco

**Causa:** Erro na renderização.

**Solução:**
1. Verifique se WeasyPrint está instalado
2. Veja a mensagem de erro nos logs
3. Simplifique o HTML para debug

---

## 📋 Checklist: Criar Contrato Personalizado

- [ ] Identifiquei o tipo de contrato necessário
- [ ] Criei/editei o arquivo `.html` apropriado
- [ ] Testei os placeholders {{ }} disponíveis
- [ ] Verifiquei formatação CSS
- [ ] Gerei um contrato teste em PDF
- [ ] Validei que todos os dados aparecem corretamente
- [ ] Ajustei espaçamento e margens conforme necessário
- [ ] Documentei quaisquer campos customizados

---

## 🚀 Próximos Passos

1. **Assinatura Digital:** Adicionar campo para assinatura eletrônica
2. **QR Code:** Incluir QR code do contrato para rastreamento
3. **Numeração:** Auto-numerar contratos
4. **Histórico:** Versionar templates com data

---

**Última atualização:** Janeiro 2024
**Versão:** 1.0
