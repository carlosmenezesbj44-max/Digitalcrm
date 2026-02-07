"""Gerador de PDFs para Contratos"""

import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class TemplateResolver:
    """Resolve qual template usar baseado no tipo de contrato"""
    
    TEMPLATES_DIR = os.path.join(
        os.path.dirname(__file__),
        "templates"
    )
    
    @staticmethod
    def obter_template(tipo_contrato: str) -> str:
        """
        Retorna conteúdo do template HTML baseado no tipo de contrato
        
        Args:
            tipo_contrato: Tipo do contrato (servico, assinatura, manutencao, suporte, outro)
            
        Returns:
            str: Conteúdo HTML do template
            
        Raises:
            FileNotFoundError: Se template não existir
        """
        template_file = f"{tipo_contrato}.html"
        template_path = os.path.join(TemplateResolver.TEMPLATES_DIR, template_file)
        
        # Tentar com tipo específico
        if os.path.exists(template_path):
            logger.info(f"Template encontrado: {template_file}")
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        # Fallback para template base
        template_path = os.path.join(TemplateResolver.TEMPLATES_DIR, "base.html")
        if os.path.exists(template_path):
            logger.warning(f"Template {template_file} não encontrado, usando base.html")
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        raise FileNotFoundError(
            f"Nenhum template encontrado. "
            f"Esperado: {template_file} ou base.html"
        )


class RendererPDF(ABC):
    """Interface para renderizadores de PDF"""
    
    @abstractmethod
    def renderizar(self, html: str, filename: str) -> bytes:
        """
        Renderiza HTML para PDF
        
        Args:
            html: Conteúdo HTML
            filename: Nome do arquivo (sem extensão)
            
        Returns:
            bytes: Conteúdo do PDF
        """
        pass


class WeasyPrintRenderer(RendererPDF):
    """Renderiza HTML para PDF usando WeasyPrint"""
    
    def renderizar(self, html: str, filename: str) -> bytes:
        """Renderiza HTML para PDF usando WeasyPrint"""
        try:
            from weasyprint import HTML, CSS
            from io import BytesIO
            
            # Renderizar HTML para PDF
            pdf_bytes = HTML(string=html).write_pdf()
            
            logger.info(f"PDF gerado com sucesso: {filename}")
            return pdf_bytes
            
        except ImportError:
            raise ImportError(
                "WeasyPrint não está instalado. "
                "Instale com: pip install weasyprint"
            )
        except Exception as e:
            logger.error(f"Erro ao renderizar PDF: {e}")
            raise


class ContratosPDFGenerator:
    """
    Gerador de contratos em PDF com suporte a templates
    
    Responsabilidades:
    - Selecionar template apropriado
    - Preencher placeholders
    - Renderizar para PDF
    """
    
    def __init__(
        self,
        contrato_model,
        renderer: Optional[RendererPDF] = None,
        empresa_dados: Optional[dict] = None
    ):
        """
        Inicializa o gerador
        
        Args:
            contrato_model: Modelo do contrato (com dados da BD)
            renderer: Renderizador de PDF (padrão: WeasyPrint)
            empresa_dados: Dados da empresa (nome, CNPJ, endereço, etc)
        """
        self.contrato = contrato_model
        self.renderer = renderer or WeasyPrintRenderer()
        self.empresa_dados = empresa_dados or {}
    
    def gerar_pdf(self) -> bytes:
        """
        Gera PDF do contrato completo
        
        Returns:
            bytes: Conteúdo do PDF
            
        Raises:
            ValueError: Se dados obrigatórios estão faltando
            FileNotFoundError: Se template não existir
        """
        logger.info(f"Gerando PDF para contrato ID {self.contrato.id}")
        
        # 1. Obter template baseado no tipo
        tipo_contrato = self.contrato.tipo_contrato.value if hasattr(
            self.contrato.tipo_contrato, 'value'
        ) else self.contrato.tipo_contrato
        
        template_html = TemplateResolver.obter_template(tipo_contrato)
        
        # 2. Preencher placeholders
        html_preenchido = self._preencher_template(template_html)
        
        # 3. Renderizar
        pdf_bytes = self.renderer.renderizar(
            html_preenchido,
            f"contrato_{self.contrato.id}"
        )
        
        return pdf_bytes
    
    def _preencher_template(self, html: str) -> str:
        """
        Substitui placeholders no template com dados do contrato
        
        Args:
            html: Template HTML com placeholders
            
        Returns:
            str: HTML com placeholders preenchidos
        """
        try:
            from jinja2 import Template
            
            template = Template(html)
            
            # Preparar contexto com dados do contrato
            contexto = self._preparar_contexto()
            
            # Renderizar
            html_renderizado = template.render(contexto)
            
            return html_renderizado
            
        except Exception as e:
            logger.error(f"Erro ao preencher template: {e}")
            raise
    
    def _preparar_contexto(self) -> dict:
        """
        Prepara dados para Jinja2 renderizar
        
        Returns:
            dict: Contexto com todos os placeholders
        """
        from crm_core.config.settings import settings
        
        # Dados do contrato
        contexto = {
            # IDs
            'contrato_id': self.contrato.id,
            'cliente_id': self.contrato.cliente_id,
            
            # Títulos e descritivos
            'contrato_titulo': self.contrato.titulo or '',
            'contrato_descricao': self.contrato.descricao or '',
            'contrato_tipo': self.contrato.tipo_contrato.value if hasattr(
                self.contrato.tipo_contrato, 'value'
            ) else self.contrato.tipo_contrato,
            
            # Valores
            'contrato_valor': self._formatar_moeda(self.contrato.valor_contrato),
            'contrato_valor_numero': self.contrato.valor_contrato or 0,
            
            # Datas
            'data_atual': datetime.now().strftime('%d/%m/%Y'),
            'data_vigencia_inicio': self._formatar_data(
                self.contrato.data_vigencia_inicio
            ),
            'data_vigencia_fim': self._formatar_data(
                self.contrato.data_vigencia_fim
            ),
            'data_criacao': self._formatar_data(
                self.contrato.data_criacao
            ),
        }
        
        # Dados do cliente (se carregado)
        if hasattr(self.contrato, 'cliente') and self.contrato.cliente:
            cliente = self.contrato.cliente
            contexto.update({
                'cliente_nome': cliente.nome or '',
                'cliente_cpf': cliente.cpf or '',
                'cliente_cnpj': getattr(cliente, 'cnpj', None) or '',
                'cliente_endereco': cliente.endereco or '',
                'cliente_telefone': cliente.telefone or '',
                'cliente_email': cliente.email or '',
            })
        else:
            # Valores padrão se cliente não carregado
            contexto.update({
                'cliente_nome': 'N/A',
                'cliente_cpf': 'N/A',
                'cliente_cnpj': 'N/A',
                'cliente_endereco': 'N/A',
                'cliente_telefone': 'N/A',
                'cliente_email': 'N/A',
            })
        
        # Dados da empresa (prioridade para empresa_dados passada, senão usa settings)
        contexto.update({
            'empresa_nome': self.empresa_dados.get('nome') or settings.company_name or 'Sua Empresa',
            'empresa_razao_social': self.empresa_dados.get('razao_social') or settings.company_razao_social or '',
            'empresa_cnpj': self.empresa_dados.get('cnpj') or settings.company_cnpj or '00.000.000/0000-00',
            'empresa_ie': self.empresa_dados.get('ie') or settings.company_ie or '',
            'empresa_endereco': self.empresa_dados.get('endereco') or settings.company_endereco or 'Rua Exemplo, 123',
            'empresa_telefone': self.empresa_dados.get('telefone') or settings.company_telefone or '(00) 0000-0000',
            'empresa_email': self.empresa_dados.get('email') or settings.company_email or 'contato@empresa.com',
            'empresa_logo': self.empresa_dados.get('logo_url') or settings.company_logo or '',
        })
        
        return contexto
    
    @staticmethod
    def _formatar_data(data) -> str:
        """Formata data para formato brasileiro"""
        if not data:
            return ''
        try:
            return data.strftime('%d/%m/%Y')
        except:
            return str(data)
    
    @staticmethod
    def _formatar_moeda(valor) -> str:
        """Formata valor em moeda brasileira"""
        if not valor:
            return 'R$ 0,00'
        try:
            return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        except:
            return f'R$ {valor}'
