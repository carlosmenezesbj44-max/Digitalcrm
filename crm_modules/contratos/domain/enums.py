"""Enumerações para o módulo de Contratos"""

from enum import Enum


class StatusAssinatura(Enum):
    """Status da assinatura de um contrato"""
    AGUARDANDO = "aguardando"      # Aguardando assinatura
    ASSINADO = "assinado"          # Já foi assinado
    LIBERADO = "liberado"          # Liberado para vigência


class TipoContrato(Enum):
    """Tipos de contratos disponíveis"""
    SERVICO = "servico"            # Contrato de Serviço
    ASSINATURA = "assinatura"      # Contrato de Assinatura
    MANUTENCAO = "manutencao"      # Contrato de Manutenção
    SUPORTE = "suporte"            # Contrato de Suporte
    OUTRO = "outro"                # Outro tipo


class StatusRenovacao(Enum):
    """Status de renovação do contrato"""
    NAO_RENOVAVEL = "nao_renovavel"           # Não é renovável
    RENOVACAO_AUTOMATICA = "renovacao_automatica"  # Renova automaticamente
    RENOVACAO_MANUAL = "renovacao_manual"    # Precisa renovar manualmente
    EXPIRADO = "expirado"                    # Expirou
