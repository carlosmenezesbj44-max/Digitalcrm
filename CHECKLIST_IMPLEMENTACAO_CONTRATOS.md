# ✅ Checklist: Implementação de Contratos Reorganizados

## 📌 Fase 1: Validação (30 min)

### 1.1 Verificar Estrutura de Diretórios
```bash
# Execute este comando para validar
ls -la crm_modules/contratos/domain/
ls -la crm_modules/contratos/infrastructure/pdf/
ls -la crm_modules/contratos/infrastructure/pdf/templates/
```

**Esperado:**
- [ ] `domain/` contém: `__init__.py`, `enums.py`
- [ ] `infrastructure/` contém: `__init__.py`, `pdf/`, `signatures/`, `audit/`
- [ ] `infrastructure/pdf/templates/` contém: 5 arquivos `.html`

### 1.2 Verificar Arquivos Criados
```bash
# Liste todos os arquivos novos
find crm_modules/contratos -type f -name "*.py" | grep -E "(domain|infrastructure)"
find crm_modules/contratos -type f -name "*.html"
```

**Esperado:**
- [ ] `domain/__init__.py` ✅
- [ ] `domain/enums.py` ✅
- [ ] `infrastructure/__init__.py` ✅
- [ ] `infrastructure/pdf/__init__.py` ✅
- [ ] `infrastructure/pdf/generator.py` ✅
- [ ] `infrastructure/pdf/templates/__init__.py` ✅
- [ ] 5 arquivos `.html` ✅

### 1.3 Verificar Documentação
```bash
# Verificar documentação criada
ls -la crm_modules/contratos/README.md
ls -la crm_modules/contratos/PLACEHOLDERS_REFERENCE.md
ls -la GUIA_TEMPLATES_CONTRATOS.md
ls -la MELHORIAS_SISTEMA_CONTRATOS.md
ls -la IMPLEMENTACAO_REORGANIZACAO_CONTRATOS.md
```

**Esperado:**
- [ ] `crm_modules/contratos/README.md` ✅
- [ ] `crm_modules/contratos/PLACEHOLDERS_REFERENCE.md` ✅
- [ ] `GUIA_TEMPLATES_CONTRATOS.md` ✅
- [ ] `MELHORIAS_SISTEMA_CONTRATOS.md` ✅
- [ ] `IMPLEMENTACAO_REORGANIZACAO_CONTRATOS.md` ✅

---

## 🔧 Fase 2: Testes Básicos (45 min)

### 2.1 Testar Importação de Enums

Criar arquivo: `test_contratos_estrutura.py`

```python
# test_contratos_estrutura.py

# Teste 1: Importar enums do novo local
try:
    from crm_modules.contratos.domain.enums import (
        StatusAssinatura,
        TipoContrato,
        StatusRenovacao
    )
    print("✅ Enums importadas com sucesso!")
    
    # Verificar valores
    assert StatusAssinatura.AGUARDANDO.value == "aguardando"
    assert TipoContrato.SERVICO.value == "servico"
    assert StatusRenovacao.RENOVACAO_MANUAL.value == "renovacao_manual"
    print("✅ Valores de enums corretos!")
    
except Exception as e:
    print(f"❌ Erro ao importar enums: {e}")

# Teste 2: Importar gerador PDF
try:
    from crm_modules.contratos.infrastructure.pdf.generator import (
        ContratosPDFGenerator,
        TemplateResolver
    )
    print("✅ Gerador PDF importado com sucesso!")
    
except Exception as e:
    print(f"❌ Erro ao importar gerador: {e}")

# Teste 3: Verificar templates
try:
    from crm_modules.contratos.infrastructure.pdf.generator import TemplateResolver
    import os
    
    templates_dir = TemplateResolver.TEMPLATES_DIR
    templates = [f for f in os.listdir(templates_dir) if f.endswith('.html')]
    
    print(f"✅ Templates encontrados: {templates}")
    assert len(templates) >= 5, "Deve haver pelo menos 5 templates"
    print(f"✅ Total de templates: {len(templates)}")
    
except Exception as e:
    print(f"❌ Erro ao verificar templates: {e}")

print("\n" + "="*50)
print("Se todos os testes passaram, estrutura está OK!")
print("="*50)
```

Executar:
```bash
python test_contratos_estrutura.py
```

**Resultado esperado:**
- [ ] ✅ Enums importadas com sucesso!
- [ ] ✅ Valores de enums corretos!
- [ ] ✅ Gerador PDF importado com sucesso!
- [ ] ✅ Templates encontrados: [...]
- [ ] ✅ Total de templates: 5

### 2.2 Testar Geração de PDF (com dados reais)

```python
# test_gerar_pdf.py

from crm_modules.contratos.infrastructure.pdf.generator import ContratosPDFGenerator
from datetime import datetime, timedelta

# Simular um contrato (mock)
class MockCliente:
    nome = "João Silva"
    cpf = "000.000.000-00"
    cnpj = "00.000.000/0000-00"
    endereco = "Rua X, 123"
    telefone = "(11) 99999-9999"
    email = "joao@email.com"

class MockContrato:
    id = 123
    cliente_id = 1
    titulo = "Plano Internet 100MB"
    descricao = "Serviço de Internet de alta velocidade"
    tipo_contrato = type('obj', (object,), {'value': 'servico'})()
    valor_contrato = 99.90
    data_vigencia_inicio = datetime.now()
    data_vigencia_fim = datetime.now() + timedelta(days=365)
    data_criacao = datetime.now()
    cliente = MockCliente()

# Testar
try:
    contrato = MockContrato()
    
    empresa_dados = {
        'nome': 'Sua Empresa LTDA',
        'cnpj': '00.000.000/0000-00',
        'endereco': 'Rua Teste, 456',
        'telefone': '(11) 3000-0000',
        'email': 'contato@empresa.com'
    }
    
    generator = ContratosPDFGenerator(
        contrato_model=contrato,
        empresa_dados=empresa_dados
    )
    
    print("✅ Gerador criado com sucesso!")
    
    # Tentar gerar PDF
    pdf_bytes = generator.gerar_pdf()
    
    if pdf_bytes and len(pdf_bytes) > 0:
        print(f"✅ PDF gerado com sucesso! Tamanho: {len(pdf_bytes)} bytes")
        
        # Salvar para teste
        with open('/tmp/test_contrato.pdf', 'wb') as f:
            f.write(pdf_bytes)
        print("✅ PDF salvo em: /tmp/test_contrato.pdf")
    else:
        print("❌ PDF vazio!")
        
except Exception as e:
    print(f"❌ Erro ao gerar PDF: {e}")
    import traceback
    traceback.print_exc()
```

Executar:
```bash
python test_gerar_pdf.py
```

**Resultado esperado:**
- [ ] ✅ Gerador criado com sucesso!
- [ ] ✅ PDF gerado com sucesso!
- [ ] ✅ PDF salvo em: /tmp/test_contrato.pdf

---

## 📖 Fase 3: Validação de Documentação (20 min)

### 3.1 Verificar README

Abrir: `crm_modules/contratos/README.md`

- [ ] Seção de estrutura de diretórios está clara?
- [ ] Enumerações estão documentadas?
- [ ] Placeholders estão listados?
- [ ] Exemplo de uso está presente?

### 3.2 Verificar Guia de Templates

Abrir: `GUIA_TEMPLATES_CONTRATOS.md`

- [ ] Seção "Como Funciona" está clara?
- [ ] Exemplos práticos estão presentes?
- [ ] Seção de troubleshooting cobre casos comuns?
- [ ] Checklist de criação está completo?

### 3.3 Verificar Referência de Placeholders

Abrir: `crm_modules/contratos/PLACEHOLDERS_REFERENCE.md`

- [ ] Todos os placeholders estão listados?
- [ ] Há exemplos de uso?
- [ ] Há seção de sintaxe Jinja2?

---

## 🎯 Fase 4: Testes de Caso Real (1-2 horas)

### 4.1 Teste com Contrato de Verdade do BD

```python
# test_contrato_real.py

from sqlalchemy.orm import Session
from crm_modules.contratos.repository import ContratoRepository
from crm_modules.contratos.infrastructure.pdf.generator import ContratosPDFGenerator

# Conectar ao BD
session = Session()  # Configure conforme seu setup
repo = ContratoRepository(session=session)

# Buscar um contrato real
contrato = repo.get_by_id(1)  # ID de um contrato existente

if contrato:
    print(f"📋 Testando contrato ID: {contrato.id}")
    print(f"   Tipo: {contrato.tipo_contrato}")
    print(f"   Cliente: {contrato.cliente.nome if contrato.cliente else 'N/A'}")
    
    try:
        # Configurar dados da empresa
        empresa_dados = {
            'nome': 'Sua Empresa',
            'cnpj': '00.000.000/0000-00',
            'endereco': 'Rua Y, 789',
            'telefone': '(11) 3000-0000',
            'email': 'contato@empresa.com'
        }
        
        # Gerar PDF
        generator = ContratosPDFGenerator(
            contrato_model=contrato,
            empresa_dados=empresa_dados
        )
        
        pdf_bytes = generator.gerar_pdf()
        
        # Salvar
        filename = f"contrato_{contrato.id}_teste.pdf"
        with open(filename, 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"✅ PDF gerado com sucesso!")
        print(f"   Arquivo: {filename}")
        print(f"   Tamanho: {len(pdf_bytes)} bytes")
        
    except Exception as e:
        print(f"❌ Erro ao gerar PDF: {e}")
        import traceback
        traceback.print_exc()
else:
    print("❌ Contrato não encontrado")
```

**Validar:**
- [ ] PDF gerado sem erros
- [ ] Arquivo salvo com sucesso
- [ ] Abrir PDF e verificar dados estão preenchidos corretamente
- [ ] Verificar formatação visual

### 4.2 Teste de Novo Tipo de Contrato

1. [ ] Editar `domain/enums.py` e adicionar novo tipo
2. [ ] Criar novo arquivo `.html` em `templates/`
3. [ ] Criar contrato com novo tipo
4. [ ] Gerar PDF e validar

---

## 📝 Fase 5: Integração com Código Existente (2-4 horas)

### 5.1 Revisar `service.py`

Abrir: `crm_modules/contratos/service.py`

- [ ] Linha ~283: Método `_gerar_pdf_contrato`
- [ ] Está usando `ContratosPDFGenerator`?
- [ ] Se não, considerar migrar (opcional por enquanto)

### 5.2 Revisar `models.py`

Abrir: `crm_modules/contratos/models.py`

- [ ] Importações de enums estão corretas?
- [ ] Podem importar de `domain/enums.py` agora?

### 5.3 Validar Compatibilidade

```python
# test_compatibilidade.py

# Teste que código antigo ainda funciona
try:
    # Importação antiga (models.py)
    from crm_modules.contratos.models import ContratoModel, StatusAssinatura
    print("✅ Importação antiga (models.py) ainda funciona!")
    
except ImportError as e:
    print(f"⚠️ Verificar: {e}")

try:
    # Importação nova (domain/enums.py)
    from crm_modules.contratos.domain.enums import StatusAssinatura
    print("✅ Importação nova (domain/enums.py) funciona!")
    
except ImportError as e:
    print(f"❌ Erro: {e}")
```

---

## ✨ Fase 6: Demo/Apresentação (30 min)

Preparar para mostrar:

- [ ] Estrutura de diretórios (print screen)
- [ ] Documentação (abrir README.md)
- [ ] Exemplo de template (abrir servico.html)
- [ ] PDF gerado (abrir PDF em reader)
- [ ] Comparação antes vs depois

---

## 📊 Resumo de Validação

```
Fase 1: Estrutura de Diretórios      [_______________]  Status: ✅/❌
Fase 2: Testes Básicos               [_______________]  Status: ✅/❌
Fase 3: Documentação                 [_______________]  Status: ✅/❌
Fase 4: Testes de Caso Real          [_______________]  Status: ✅/❌
Fase 5: Integração Existente         [_______________]  Status: ✅/❌
Fase 6: Demo                         [_______________]  Status: ✅/❌
```

---

## 🚀 Quando Tudo Estiver ✅

### Próximas Ações
1. [ ] Documentar qualquer customização realizada
2. [ ] Fazer commit dos arquivos novos
3. [ ] Atualizar CHANGELOG.md
4. [ ] Agendar Fase 2 (Use Cases)

### Benefícios Conquistados
- ✅ Estrutura clara e organizada
- ✅ Documentação completa
- ✅ Fácil manutenção e expansão
- ✅ Templates reutilizáveis
- ✅ Código profissional

---

## 📞 Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| Módulo não encontrado | Adicione `crm_provedor` ao PYTHONPATH |
| WeasyPrint erro | `pip install weasyprint` |
| Template não encontrado | Verifique nome exato (case-sensitive) |
| Placeholder vazio | Verifique dados no contrato/cliente |
| Erro de formatação PDF | Simplifique CSS/HTML no template |

---

## 📝 Notas

- Data de criação: Janeiro 2024
- Responsável: [Seu nome]
- Status: 🟢 Implementado
- Próxima revisão: 30 dias

