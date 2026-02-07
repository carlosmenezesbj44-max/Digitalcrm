# 📋 Sistema de Contratos

Módulo centralizado para gerenciamento de contratos, assinaturas digitais e geração de PDFs.

## 📁 Estrutura do Módulo

```
contratos/
├── domain/                              # Camada de Domínio
│   ├── enums.py                        # Enumerações (Status, Tipos)
│   └── __init__.py
│
├── infrastructure/                      # Camada de Infraestrutura
│   ├── pdf/                            # Geração de PDFs
│   │   ├── generator.py                # Motor de geração
│   │   ├── templates/                  # Templates HTML
│   │   │   ├── base.html               # Template padrão
│   │   │   ├── servico.html            # Contrato de serviço
│   │   │   ├── assinatura.html         # Contrato de assinatura
│   │   │   ├── manutencao.html         # Contrato de manutenção
│   │   │   └── suporte.html            # Contrato de suporte
│   │   └── __init__.py
│   │
│   ├── signatures/                     # Armazenamento de assinaturas
│   │   └── __init__.py
│   │
│   └── audit/                          # Auditoria
│       └── __init__.py
│
├── models.py                           # Modelos SQLAlchemy
├── repository.py                       # Camada de Acesso a Dados
├── schemas.py                          # Pydantic DTOs
├── service.py                          # Lógica de Negócio
├── api.py                              # Rotas FastAPI
├── domain.py                           # Entidades de Domínio
└── README.md                           # Este arquivo
```

## 🔑 Enumerações (domain/enums.py)

### StatusAssinatura
- `AGUARDANDO` - Aguardando assinatura
- `ASSINADO` - Já foi assinado
- `LIBERADO` - Liberado para vigência

### TipoContrato
- `SERVICO` - Contrato de Serviço
- `ASSINATURA` - Contrato de Assinatura
- `MANUTENCAO` - Contrato de Manutenção
- `SUPORTE` - Contrato de Suporte
- `OUTRO` - Outro tipo

### StatusRenovacao
- `NAO_RENOVAVEL` - Não é renovável
- `RENOVACAO_AUTOMATICA` - Renova automaticamente
- `RENOVACAO_MANUAL` - Precisa renovar manualmente
- `EXPIRADO` - Expirou

## 📄 Templates HTML

Cada tipo de contrato possui um template específico. Os templates usam **Jinja2** para substituir placeholders.

### Placeholders Disponíveis

#### Dados do Contrato
| Placeholder | Descrição | Exemplo |
|------------|-----------|---------|
| `{{ contrato_id }}` | ID do contrato | `123` |
| `{{ contrato_titulo }}` | Título/Nome do contrato | `Plano Internet 100MB` |
| `{{ contrato_descricao }}` | Descrição completa | `Serviço de Internet de alta velocidade` |
| `{{ contrato_tipo }}` | Tipo do contrato | `servico` |
| `{{ contrato_valor }}` | Valor formatado em BRL | `R$ 99,90` |
| `{{ contrato_valor_numero }}` | Valor como número | `99.90` |
| `{{ data_vigencia_inicio }}` | Data início (DD/MM/YYYY) | `01/01/2024` |
| `{{ data_vigencia_fim }}` | Data fim (DD/MM/YYYY) | `31/12/2024` |
| `{{ data_criacao }}` | Data de criação (DD/MM/YYYY) | `15/01/2024` |
| `{{ data_atual }}` | Data atual (DD/MM/YYYY) | `15/01/2024` |

#### Dados do Cliente
| Placeholder | Descrição |
|------------|-----------|
| `{{ cliente_nome }}` | Nome completo |
| `{{ cliente_cpf }}` | CPF do cliente |
| `{{ cliente_cnpj }}` | CNPJ (se pessoa jurídica) |
| `{{ cliente_endereco }}` | Endereço completo |
| `{{ cliente_telefone }}` | Telefone de contato |
| `{{ cliente_email }}` | Email de contato |

#### Dados da Empresa
| Placeholder | Descrição |
|------------|-----------|
| `{{ empresa_nome }}` | Nome da empresa |
| `{{ empresa_cnpj }}` | CNPJ da empresa |
| `{{ empresa_endereco }}` | Endereço da empresa |
| `{{ empresa_telefone }}` | Telefone da empresa |
| `{{ empresa_email }}` | Email da empresa |
| `{{ empresa_logo }}` | URL da logo (se aplicável) |

### Exemplo de Uso em Template

```html
<!DOCTYPE html>
<html>
<body>
    <h1>CONTRATO {{ contrato_id }}</h1>
    
    <p>
        <strong>CONTRATADA:</strong> {{ empresa_nome }}<br/>
        <strong>CNPJ:</strong> {{ empresa_cnpj }}
    </p>
    
    <p>
        <strong>CONTRATANTE:</strong> {{ cliente_nome }}<br/>
        <strong>CPF:</strong> {{ cliente_cpf }}
    </p>
    
    <p>
        <strong>Serviço:</strong> {{ contrato_titulo }}<br/>
        <strong>Valor:</strong> {{ contrato_valor }}<br/>
        <strong>Vigência:</strong> {{ data_vigencia_inicio }} a {{ data_vigencia_fim }}
    </p>
</body>
</html>
```

## 🔧 Usando o Gerador de PDFs

### Importar

```python
from crm_modules.contratos.infrastructure.pdf.generator import ContratosPDFGenerator

# Com renderer padrão (WeasyPrint)
generator = ContratosPDFGenerator(
    contrato_model=contrato,
    empresa_dados={
        'nome': 'Minha Empresa',
        'cnpj': '00.000.000/0000-00',
        'endereco': 'Rua X, 123',
        'telefone': '(11) 0000-0000',
        'email': 'contato@empresa.com'
    }
)

# Gerar PDF
pdf_bytes = generator.gerar_pdf()

# Salvar em arquivo
with open(f'contrato_{contrato.id}.pdf', 'wb') as f:
    f.write(pdf_bytes)
```

### Como Funciona

1. **Seleciona template** baseado em `contrato.tipo_contrato`
2. **Preenche placeholders** com dados do contrato, cliente e empresa
3. **Renderiza para PDF** usando WeasyPrint
4. **Retorna bytes** do PDF pronto para salvar ou baixar

## 📊 Fluxo de Criação de Contrato

```
1. Cliente cria novo contrato
   ↓
2. Valida dados (cliente existe? datas válidas?)
   ↓
3. Salva no banco de dados
   ↓
4. [OPCIONAL] Gera PDF
   ├─ Seleciona template do tipo
   ├─ Preenche placeholders
   └─ Renderiza para arquivo
   ↓
5. Registra auditoria (histórico)
   ↓
6. Retorna contrato criado
```

## 🔐 Enumerações no Banco

Os valores das enums são armazenados como **strings** no banco de dados:

```python
# No BD, será armazenado:
status_assinatura = "aguardando"      # Não: 0 ou true/false
tipo_contrato = "servico"              # Não: 1 ou outro número
status_renovacao = "renovacao_manual"   # Não: true/false
```

Isso facilita leitura e debugging.

## 🚀 Próximas Melhorias

- [ ] Implementar use cases (padrão Clean Architecture)
- [ ] Assinatura digital com certificado
- [ ] Integração com serviços de e-signature
- [ ] Dashboard de contratos vencendo
- [ ] Notificações automáticas
- [ ] Histórico completo com audit log

## 📞 Troubleshooting

### "Template não encontrado"
Verifique se o arquivo existe em `infrastructure/pdf/templates/{tipo_contrato}.html`

### "WeasyPrint não instalado"
```bash
pip install weasyprint
```

### PDF gerado em branco
Verifique se os placeholders estão corretos no template.

---

**Última atualização:** Janeiro 2024
