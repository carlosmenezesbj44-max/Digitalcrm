"""Gerador de PDF para Contratos"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
)
from datetime import datetime
import io
import os


class ContratosPDFGenerator:
    """Gera PDFs profissionais de contratos"""

    def __init__(self, contrato, template_html=None):
        self.contrato = contrato
        self.template_html = template_html
        self.styles = getSampleStyleSheet()
        self._criar_estilos_customizados()
    
    def _criar_estilos_customizados(self):
        """Cria estilos customizados para o documento"""
        # Estilo para título
        self.style_titulo = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=20,
            alignment=1,  # Center
            fontName='Helvetica-Bold'
        )
        
        # Estilo para subtítulo
        self.style_subtitulo = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#0d47a1'),
            spaceBefore=15,
            spaceAfter=8,
            fontName='Helvetica-Bold',
            borderPadding=2,
            borderWidth=0,
            borderColor=colors.white
        )
        
        # Estilo para texto normal
        self.style_normal = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=4,  # Justify
            spaceAfter=8,
            fontName='Helvetica',
            leading=12
        )

        # Estilo para cláusulas
        self.style_clausula = ParagraphStyle(
            'Clausula',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=4,
            spaceBefore=10,
            spaceAfter=5,
            fontName='Helvetica-Bold',
            leading=12
        )
    
    def gerar_pdf(self) -> bytes:
        """Gera PDF completo do contrato"""
        if self.template_html:
            return self._gerar_pdf_from_template()
        else:
            return self._gerar_pdf_padrao()

    def _gerar_pdf_padrao(self) -> bytes:
        """Gera PDF com layout padrão"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=inch*0.75,
            leftMargin=inch*0.75,
            topMargin=inch*0.75,
            bottomMargin=inch*0.75
        )

        story = []

        # Cabeçalho Profissional
        story.append(self._criar_cabecalho_profissional())
        story.append(Spacer(1, 20))

        # Título Central
        story.append(Paragraph("CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE COMUNICAÇÃO MULTIMÍDIA (SCM)", self.style_titulo))
        story.append(Spacer(1, 10))

        # Seção 1: Identificação das Partes
        story.append(Paragraph("1. DAS PARTES", self.style_subtitulo))
        story.append(self._criar_secao_partes())
        story.append(Spacer(1, 10))

        # Seção 2: Objeto
        story.append(Paragraph("2. DO OBJETO", self.style_subtitulo))
        objeto_text = f"O presente contrato tem por objeto a prestação, pela CONTRATADA ao CONTRATANTE, de serviços de Comunicação Multimídia (Internet), através do plano <b>{self.contrato.titulo}</b>, com as características técnicas e valores descritos neste instrumento."
        story.append(Paragraph(objeto_text, self.style_normal))

        # Detalhes do Plano
        story.append(self._criar_secao_plano())
        story.append(Spacer(1, 10))

        # Cláusulas Padrão de Provedor
        self._adicionar_clausulas_padrao(story)

        # Área de Assinatura
        story.append(Spacer(1, 30))
        story.append(self._criar_area_assinatura_elegante())

        # Rodapé
        story.append(Spacer(1, 20))
        story.append(self._criar_rodape_elegante())

        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    def _gerar_pdf_from_template(self) -> bytes:
        """Gera PDF a partir de template HTML personalizado"""
        try:
            import weasyprint
        except ImportError:
            # Se weasyprint não estiver disponível, usar o layout padrão
            print("Aviso: weasyprint não disponível, usando layout padrão")
            return self._gerar_pdf_padrao()

        if not self.template_html:
            return self._gerar_pdf_padrao()

        try:
            # Substituir placeholders
            html_content = self._substituir_placeholders(self.template_html)

            # Gerar PDF
            pdf_bytes = weasyprint.HTML(string=html_content).write_pdf()
            return pdf_bytes
        except Exception as e:
            # Se houver erro ao gerar PDF com weasyprint, usar layout padrão
            print(f"Aviso: Erro ao gerar PDF com weasyprint: {e}, usando layout padrão")
            return self._gerar_pdf_padrao()

    def _substituir_placeholders(self, template: str) -> str:
        """Substitui placeholders no template"""
        from crm_core.config.settings import settings

        cliente = self.contrato.cliente

        replacements = {
            '{{empresa_nome}}': settings.company_name,
            '{{empresa_razao_social}}': settings.company_razao_social,
            '{{empresa_logo}}': f'<img src="{settings.company_logo}" alt="Logo" style="max-width: 200px;">' if settings.company_logo else '',
            '{{empresa_cnpj}}': settings.company_cnpj or '00.000.000/0001-00',
            '{{empresa_ie}}': settings.company_ie,
            '{{empresa_telefone}}': settings.company_telefone or '(00) 0000-0000',
            '{{empresa_email}}': settings.company_email or 'contato@empresa.com',
            '{{empresa_endereco}}': settings.company_endereco or 'Rua Exemplo, 123 - Centro',
            '{{cliente_nome}}': cliente.nome,
            '{{cliente_cpf}}': cliente.cpf or cliente.cnpj or 'N/A',
            '{{cliente_endereco}}': f"{cliente.rua or cliente.endereco}, {cliente.numero or 'S/N'} - {cliente.bairro or ''}, {cliente.cidade or ''}",
            '{{contrato_titulo}}': self.contrato.titulo,
            '{{contrato_valor}}': f"{self.contrato.valor_contrato:,.2f}" if self.contrato.valor_contrato else 'N/A',
            '{{contrato_data_inicio}}': self.contrato.data_vigencia_inicio.strftime('%d/%m/%Y') if self.contrato.data_vigencia_inicio else 'N/A',
            '{{contrato_data_fim}}': self.contrato.data_vigencia_fim.strftime('%d/%m/%Y') if self.contrato.data_vigencia_fim else 'N/A',
            '{{contrato_id}}': str(self.contrato.id),
            '{{data_atual}}': datetime.now().strftime('%d/%m/%Y'),
            '{{contrato_velocidade}}': getattr(self.contrato, 'velocidade', '100'),  # Default 100 Mbps
            '{{contrato_prazo_aviso}}': getattr(self.contrato, 'prazo_aviso', '30'),  # Default 30 dias
            '{{contrato_dia_vencimento}}': getattr(self.contrato, 'dia_vencimento', '10'),  # Default dia 10
            '{{contrato_dias_inadimplencia}}': getattr(self.contrato, 'dias_inadimplencia', '15'),  # Default 15 dias
            '{{contrato_cidade_foro}}': getattr(self.contrato, 'cidade_foro', cliente.cidade or 'São Paulo'),  # Default cidade do cliente
        }

        for placeholder, value in replacements.items():
            template = template.replace(placeholder, str(value) if value is not None else '')

        return template

    def _criar_cabecalho_profissional(self):
        """Cria um cabeçalho mais profissional"""
        from crm_core.config.settings import settings
        data_atual = datetime.now().strftime('%d/%m/%Y')
        
        # Usar dados da empresa configurados
        nome_empresa = settings.company_name or "PROVEDOR DE INTERNET"
        cnpj = settings.company_cnpj or "00.000.000/0001-00"
        endereco = settings.company_endereco or "Endereço não configurado"
        
        data = [[
            Paragraph(f"<b>{nome_empresa}</b><br/><font size=8>CNPJ: {cnpj}<br/>{endereco}</font>", self.style_normal),
            Paragraph(f"<div align='right'><b>CONTRATO Nº: {self.contrato.id:06d}</b><br/>Data: {data_atual}</div>", self.style_normal)
        ]]
        
        table = Table(data, colWidths=[3.5*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LINEBELOW', (0, 0), (-1, -1), 1, colors.HexColor('#1a237e')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        return table

    def _criar_secao_partes(self):
        """Cria seção de identificação das partes"""
        from crm_core.config.settings import settings
        cliente = self.contrato.cliente
        cliente_nome = cliente.nome
        cliente_doc = getattr(cliente, 'cnpj', None) or cliente.cpf or 'N/A'
        cliente_end = f"{cliente.rua or cliente.endereco}, {cliente.numero or 'S/N'} - {cliente.bairro or ''}, {cliente.cidade or ''}/{cliente.estado or ''}"
        
        # Dados da empresa
        empresa_razao = settings.company_razao_social or settings.company_name or "PROVEDOR DE INTERNET"
        empresa_cnpj = settings.company_cnpj or "00.000.000/0001-00"
        empresa_end = settings.company_endereco or "Endereço não configurado"
        
        text = f"""
        <b>CONTRATADA:</b> {empresa_razao}, com sede na {empresa_end}, inscrita no CNPJ sob o nº {empresa_cnpj}.<br/><br/>
        <b>CONTRATANTE:</b> {cliente_nome}, portador(a) do CPF/CNPJ nº {cliente_doc}, residente e domiciliado(a) em {cliente_end}.
        """
        return Paragraph(text, self.style_normal)

    def _criar_secao_plano(self):
        """Tabela com detalhes do plano"""
        valor = f"R$ {self.contrato.valor_contrato:,.2f}" if self.contrato.valor_contrato else "Consulte"
        inicio = self.contrato.data_vigencia_inicio.strftime('%d/%m/%Y') if self.contrato.data_vigencia_inicio else "-"
        
        data = [
            [Paragraph("<b>Plano/Serviço</b>", self.style_normal), Paragraph("<b>Mensalidade</b>", self.style_normal), Paragraph("<b>Início</b>", self.style_normal)],
            [self.contrato.titulo, valor, inicio]
        ]
        
        table = Table(data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f5f5f5')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        return table

    def _adicionar_clausulas_padrao(self, story):
        """Adiciona cláusulas padrão de um provedor de internet"""
        clausulas = [
            ("3. DA DISPONIBILIDADE DO SERVIÇO", 
             "A CONTRATADA compromete-se a envidar seus melhores esforços para manter a disponibilidade do serviço em 99% do tempo mensal, ressalvadas as interrupções para manutenção preventiva ou corretiva."),
            
            ("4. DO EQUIPAMENTO (COMODATO)", 
             "Caso a CONTRATADA forneça equipamentos para a prestação do serviço, estes são entregues em regime de COMODATO, devendo ser devolvidos em perfeito estado de conservação em caso de rescisão contratual."),
            
            ("5. DAS OBRIGAÇÕES DO CONTRATANTE", 
             "O CONTRATANTE obriga-se a utilizar o serviço de forma lícita, sendo vedada a comercialização, compartilhamento ou redistribuição do sinal de internet a terceiros."),
            
            ("6. DO PAGAMENTO E MULTA", 
             "O pagamento deverá ser efetuado até a data de vencimento escolhida. O atraso superior a 15 dias poderá acarretar na redução da velocidade e, após 30 dias, na suspensão total dos serviços."),
            
            ("7. DA VIGÊNCIA E FIDELIDADE", 
             "O presente contrato tem vigência de 12 meses. Em caso de rescisão antecipada por parte do CONTRATANTE, poderá ser aplicada multa proprocional conforme normas da ANATEL.")
        ]
        
        for titulo, corpo in clausulas:
            story.append(Paragraph(titulo, self.style_subtitulo))
            story.append(Paragraph(corpo, self.style_normal))

    def _criar_area_assinatura_elegante(self):
        """Área de assinatura mais limpa"""
        data = [
            [
                Paragraph("<br/><br/>__________________________<br/><b>CONTRATADA</b>", self.style_normal),
                Paragraph("<br/><br/>__________________________<br/><b>CONTRATANTE</b>", self.style_normal)
            ]
        ]
        table = Table(data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        return table

    def _criar_rodape_elegante(self):
        """Rodapé discreto"""
        text = f"Documento gerado eletronicamente em {datetime.now().strftime('%d/%m/%Y %H:%M')} | ID: {self.contrato.id}"
        return Paragraph(f"<font size=7 color='grey'>{text}</font>", self.style_normal)

    def _calcular_duracao(self) -> str:
        """Calcula duração do contrato em dias/meses"""
        if not self.contrato.data_vigencia_inicio or not self.contrato.data_vigencia_fim:
            return 'Não calculada'
        
        duracao = (self.contrato.data_vigencia_fim - self.contrato.data_vigencia_inicio).days
        
        if duracao < 30:
            return f"{duracao} dias"
        elif duracao < 365:
            meses = duracao // 30
            return f"{meses} meses"
        else:
            anos = duracao // 365
            return f"{anos} ano(s)"
