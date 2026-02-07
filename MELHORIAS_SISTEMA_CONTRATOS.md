# 🔧 Recomendações para Melhorar o Sistema de Contratos

## Problemas Identificados

### 1. **Desorganização na Estrutura de Diretórios**
- Templates HTML espalhados (na raiz do projeto)
- Arquivos de teste e configuração misturados
- Falta de pastas específicas para tipos de contrato

### 2. **Falta de Separação de Responsabilidades**
- `models.py` é muito grande
- `service.py` faz validação, PDF, auditoria - tudo junto
- Lógica de PDF acoplada ao serviço

### 3. **Problemas no Template HTML**
- Placeholders genéricos {{}} sem documentação
- Sem variação para tipos diferentes de contrato
- HTML sem versionamento

### 4. **Fluxo de Criação Confuso**
- PDF geração é opcional mas não está claro no código
- Histórico pode falhar silenciosamente
- Sem transações explícitas

---

## 🎯 Solução: Nova Estrutura

```
crm_modules/contratos/
├── __init__.py
├── api.py                          # Rotas FastAPI (mantém como está)
├── models.py                        # ✅ Bom - manter
├── repository.py                    # ✅ Bom - manter
│
├── domain/                          # ✨ NOVO
│   ├── __init__.py
│   ├── contrato.py                  # Entidade principal
│   ├── enums.py                     # StatusAssinatura, TipoContrato, etc
│   └── eventos.py                   # Eventos de domínio
│
├── application/                     # ✨ NOVO - Lógica de Aplicação
│   ├── __init__.py
│   ├── criar_contrato.py            # Use case: criar contrato
│   ├── assinar_contrato.py          # Use case: assinar contrato
│   ├── renovar_contrato.py          # Use case: renovar contrato
│   └── dto.py                       # Schemas/DTOs
│
├── infrastructure/                  # ✨ NOVO - Implementações
│   ├── __init__.py
│   ├── pdf/
│   │   ├── __init__.py
│   │   ├── generator.py             # Geração de PDF
│   │   ├── html_to_pdf.py           # WeasyPrint
│   │   └── templates/               # Templates por tipo
│   │       ├── servico.html
│   │       ├── assinatura.html
│   │       ├── manutencao.html
│   │       └── base.html
│   │
│   ├── signatures/
│   │   ├── __init__.py
│   │   ├── storage.py               # Armazenamento de assinaturas
│   │   └── validator.py             # Validação de assinatura
│   │
│   └── audit/
│       ├── __init__.py
│       └── logger.py                # Auditoria e logging
│
├── schemas.py                       # ✅ Manter (Pydantic schemas)
└── service.py                       # ⚠️ REFATORAR ou manter como façade
```

---

## 📋 Implementação Passo a Passo

### **PASSO 1: Refatorar Enums para Arquivo Específico**

**Criar: `crm_modules/contratos/domain/enums.py`**
```python
from enum import Enum

class StatusAssinatura(Enum):
    AGUARDANDO = "aguardando"
    ASSINADO = "assinado"
    LIBERADO = "liberado"

class TipoContrato(Enum):
    SERVICO = "servico"
    ASSINATURA = "assinatura"
    MANUTENCAO = "manutencao"
    SUPORTE = "suporte"
    OUTRO = "outro"

class StatusRenovacao(Enum):
    NAO_RENOVAVEL = "nao_renovavel"
    RENOVACAO_AUTOMATICA = "renovacao_automatica"
    RENOVACAO_MANUAL = "renovacao_manual"
    EXPIRADO = "expirado"
```

**Atualizar: `models.py`** para importar de enums.py:
```python
from crm_modules.contratos.domain.enums import (
    StatusAssinatura, TipoContrato, StatusRenovacao
)
```

---

### **PASSO 2: Separar Lógica de PDF**

**Criar: `crm_modules/contratos/infrastructure/pdf/generator.py`**
```python
"""Gerador de PDFs para contratos"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import os
from datetime import datetime

class TemplateResolver:
    """Resolve qual template usar baseado no tipo de contrato"""
    
    TEMPLATES_DIR = "crm_modules/contratos/infrastructure/pdf/templates"
    
    @staticmethod
    def obter_template(tipo_contrato: str) -> str:
        """Retorna caminho do template HTML"""
        template_file = f"{tipo_contrato}.html"
        template_path = os.path.join(TemplateResolver.TEMPLATES_DIR, template_file)
        
        if not os.path.exists(template_path):
            # Fallback para template base
            template_path = os.path.join(TemplateResolver.TEMPLATES_DIR, "base.html")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()

class RendererPDF(ABC):
    """Interface para renderizadores de PDF"""
    
    @abstractmethod
    def renderizar(self, html: str, filename: str) -> bytes:
        pass

class WeasyPrintRenderer(RendererPDF):
    """Renderiza HTML para PDF usando WeasyPrint"""
    
    def renderizar(self, html: str, filename: str) -> bytes:
        from weasyprint import HTML
        from io import BytesIO
        
        pdf_bytes = HTML(string=html).write_pdf()
        return pdf_bytes

class ContratosPDFGenerator:
    """Gerador de contratos em PDF com suporte a templates"""
    
    def __init__(self, contrato_model, renderer: RendererPDF = None):
        self.contrato = contrato_model
        self.renderer = renderer or WeasyPrintRenderer()
    
    def gerar_pdf(self) -> bytes:
        """Gera PDF do contrato"""
        # 1. Obter template baseado no tipo
        template_html = TemplateResolver.obter_template(
            self.contrato.tipo_contrato.value
        )
        
        # 2. Substituir placeholders
        html_preenchido = self._preencher_template(template_html)
        
        # 3. Renderizar
        pdf_bytes = self.renderer.renderizar(
            html_preenchido,
            f"contrato_{self.contrato.id}"
        )
        
        return pdf_bytes
    
    def _preencher_template(self, html: str) -> str:
        """Substitui placeholders no template"""
        from jinja2 import Template
        
        template = Template(html)
        
        # Preparar contexto
        contexto = {
            'contrato_id': self.contrato.id,
            'contrato_titulo': self.contrato.titulo,
            'contrato_valor': self.contrato.valor_contrato,
            'data_atual': datetime.now().strftime('%d/%m/%Y'),
            'cliente_nome': self.contrato.cliente.nome if self.contrato.cliente else 'N/A',
            'cliente_cpf': self.contrato.cliente.cpf if self.contrato.cliente else 'N/A',
            'cliente_endereco': self.contrato.cliente.endereco if self.contrato.cliente else 'N/A',
            'empresa_nome': 'Sua Empresa', # From settings
            'data_vigencia_inicio': self.contrato.data_vigencia_inicio.strftime('%d/%m/%Y') if self.contrato.data_vigencia_inicio else '',
            'data_vigencia_fim': self.contrato.data_vigencia_fim.strftime('%d/%m/%Y') if self.contrato.data_vigencia_fim else '',
        }
        
        return template.render(contexto)
```

---

### **PASSO 3: Criar Use Cases (Padrão Limpo)**

**Criar: `crm_modules/contratos/application/criar_contrato.py`**
```python
"""Use case: Criar novo contrato"""

from typing import Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class CriarContratoInput:
    cliente_id: int
    titulo: str
    tipo_contrato: str
    valor: float
    data_inicio: datetime
    data_fim: datetime
    incluir_pdf: bool = True

@dataclass
class CriarContratoOutput:
    contrato_id: int
    status: str
    pdf_gerado: bool
    mensagem: str

class CriarContratoUseCase:
    """Caso de uso: Criar contrato"""
    
    def __init__(self, repository, pdf_generator, audit_service, usuario_id: str):
        self.repository = repository
        self.pdf_generator = pdf_generator
        self.audit_service = audit_service
        self.usuario_id = usuario_id
    
    def executar(self, input_dto: CriarContratoInput) -> CriarContratoOutput:
        """Executa criação de contrato"""
        try:
            # 1. Validar entrada
            self._validar_entrada(input_dto)
            
            # 2. Criar modelo
            contrato_model = self._criar_modelo(input_dto)
            
            # 3. Salvar no banco (transação)
            contrato_salvo = self.repository.create(contrato_model)
            
            # 4. Gerar PDF se solicitado
            pdf_gerado = False
            if input_dto.incluir_pdf:
                pdf_gerado = self._gerar_pdf_contrato(contrato_salvo)
            
            # 5. Registrar auditoria
            self.audit_service.registrar(
                "CONTRATO_CRIADO",
                contrato_salvo.id,
                self.usuario_id,
                {"tipo": input_dto.tipo_contrato, "valor": input_dto.valor}
            )
            
            return CriarContratoOutput(
                contrato_id=contrato_salvo.id,
                status="sucesso",
                pdf_gerado=pdf_gerado,
                mensagem=f"Contrato {contrato_salvo.id} criado com sucesso"
            )
        
        except Exception as e:
            self.audit_service.registrar(
                "CONTRATO_CRIACAO_FALHOU",
                None,
                self.usuario_id,
                {"erro": str(e)}
            )
            raise
    
    def _validar_entrada(self, input_dto: CriarContratoInput):
        """Validações de negócio"""
        if input_dto.valor <= 0:
            raise ValueError("Valor do contrato deve ser positivo")
        
        if input_dto.data_fim <= input_dto.data_inicio:
            raise ValueError("Data de fim deve ser depois da data de início")
    
    def _criar_modelo(self, input_dto: CriarContratoInput):
        """Cria modelo ORM"""
        from crm_modules.contratos.models import ContratoModel, StatusAssinatura
        
        return ContratoModel(
            cliente_id=input_dto.cliente_id,
            titulo=input_dto.titulo,
            tipo_contrato=input_dto.tipo_contrato,
            valor_contrato=input_dto.valor,
            data_vigencia_inicio=input_dto.data_inicio,
            data_vigencia_fim=input_dto.data_fim,
            status_assinatura=StatusAssinatura.AGUARDANDO,
            criado_por=self.usuario_id
        )
    
    def _gerar_pdf_contrato(self, contrato_model) -> bool:
        """Gera e salva PDF"""
        try:
            # Usar novo gerador
            pdf_bytes = self.pdf_generator.gerar_pdf_contrato(contrato_model)
            
            # Salvar arquivo
            path = self._salvar_arquivo_pdf(contrato_model.id, pdf_bytes)
            
            # Atualizar referência
            contrato_model.arquivo_contrato = path
            self.repository.update(contrato_model)
            
            return True
        except Exception as e:
            print(f"⚠️ Erro ao gerar PDF: {e}")
            return False
    
    def _salvar_arquivo_pdf(self, contrato_id: int, pdf_bytes: bytes) -> str:
        """Salva PDF em disco"""
        import os
        
        os.makedirs("interfaces/web/static/contratos", exist_ok=True)
        filename = f"contrato_{contrato_id}_{datetime.now().timestamp()}.pdf"
        filepath = os.path.join("interfaces/web/static/contratos", filename)
        
        with open(filepath, 'wb') as f:
            f.write(pdf_bytes)
        
        return filepath
```

---

### **PASSO 4: Organizar Templates HTML**

**Criar estrutura:**
```
crm_modules/contratos/infrastructure/pdf/templates/
├── base.html                # Template padrão
├── servico.html            # Contrato de serviço
├── assinatura.html         # Contrato de assinatura
├── manutencao.html         # Contrato de manutenção
└── suporte.html            # Contrato de suporte
```

**Exemplo: `servico.html`**
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>CONTRATO DE PRESTAÇÃO DE SERVIÇOS</title>
    <style>
        body { 
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
        }
        .header { 
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 2px solid #000;
            padding-bottom: 20px;
        }
        .section { 
            margin-bottom: 30px;
        }
        .signature { 
            margin-top: 60px;
            display: flex;
            justify-content: space-between;
        }
        .sig-block { 
            width: 45%;
            text-align: center;
            border-top: 1px solid #000;
            padding-top: 10px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>CONTRATO DE PRESTAÇÃO DE SERVIÇOS</h1>
        <p><strong>Contrato nº:</strong> {{ contrato_id }}</p>
        <p><strong>Data:</strong> {{ data_atual }}</p>
    </div>

    <div class="section">
        <h2>1. DAS PARTES</h2>
        <p>
            <strong>CONTRATADA:</strong> {{ empresa_nome }}<br/>
            <strong>CONTRATANTE:</strong> {{ cliente_nome }}, CPF: {{ cliente_cpf }}<br/>
            <strong>Endereço:</strong> {{ cliente_endereco }}
        </p>
    </div>

    <div class="section">
        <h2>2. DO OBJETO</h2>
        <p>{{ contrato_titulo }}</p>
        <p><strong>Valor:</strong> R$ {{ contrato_valor }}</p>
        <p><strong>Vigência:</strong> {{ data_vigencia_inicio }} a {{ data_vigencia_fim }}</p>
    </div>

    <div class="section">
        <h2>3. DAS OBRIGAÇÕES</h2>
        <p>Conforme descrito neste instrumento...</p>
    </div>

    <div class="signature">
        <div class="sig-block">
            <p>{{ empresa_nome }}</p>
            <p>CONTRATADA</p>
        </div>
        <div class="sig-block">
            <p>{{ cliente_nome }}</p>
            <p>CONTRATANTE</p>
        </div>
    </div>
</body>
</html>
```

---

## 🚀 Próximas Etapas

### QUICK WIN (1-2 dias)
1. ✅ Mover enums para arquivo próprio
2. ✅ Criar pasta `/infrastructure/pdf/templates`
3. ✅ Documentar placeholders disponíveis
4. ✅ Criar um README.md para contratos

### MÉDIO PRAZO (1 semana)
5. Refatorar PDF generator (separar de service)
6. Implementar use cases (CriarContrato, AssinarContrato, etc)
7. Melhorar testes unitários

### LONGO PRAZO (2+ semanas)
8. Implementar event sourcing para auditoria
9. Criar dashboard de contratos
10. Integração com e-signature (DocuSign, etc)

---

## 📊 Benefícios da Nova Arquitetura

| Aspecto | Antes | Depois |
|---------|-------|--------|
| **Encontrar código** | Espalhado | Organizado em pastas claras |
| **Testar** | Difícil (tudo acoplado) | Fácil (separado por camada) |
| **Adicionar tipo contrato** | Modificar service | Criar novo template |
| **Auditoria** | Silenciosa | Explícita com eventos |
| **Manutenção** | Confusa | Clara e modular |

---

## 🔍 Checklist de Implementação

- [ ] Criar estrutura de diretórios
- [ ] Mover enums
- [ ] Copiar/reorganizar templates HTML
- [ ] Refatorar PDF generator
- [ ] Implementar primeiro use case (CriarContrato)
- [ ] Atualizar testes
- [ ] Documentar no README.md
- [ ] Testar fluxo completo

