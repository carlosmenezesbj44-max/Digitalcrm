"""Geração e Renderização de PDFs para Contratos"""

from crm_modules.contratos.infrastructure.pdf.generator import (
    ContratosPDFGenerator,
    TemplateResolver,
)

__all__ = [
    "ContratosPDFGenerator",
    "TemplateResolver",
]
