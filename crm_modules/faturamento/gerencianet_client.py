"""
Cliente para integração com API Gerencianet
Gerencianet é uma gateway de pagamento brasileira que permite:
- Gerar boletos
- Criar recorrências (carnês)
- Processar pagamentos
- Consultar status de transações
"""

import requests
import json
from typing import Optional, Dict, Any
from datetime import date
import os
from crm_core.utils.exceptions import ValidationException


class GerencianetClient:
    """Cliente para integração com Gerencianet"""
    
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        sandbox: bool = True
    ):
        """
        Inicializa o cliente Gerencianet
        
        Args:
            client_id: ID da aplicação Gerencianet
            client_secret: Secret da aplicação
            sandbox: Se True usa ambiente de teste, False usa produção
        """
        self.client_id = client_id or os.getenv("GERENCIANET_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("GERENCIANET_CLIENT_SECRET")
        self.sandbox = sandbox
        
        if not self.client_id or not self.client_secret:
            raise ValidationException(
                "GERENCIANET_CLIENT_ID e GERENCIANET_CLIENT_SECRET são obrigatórios"
            )
        
        self.base_url = (
            "https://sandbox.gerencianet.com.br" if sandbox
            else "https://api.gerencianet.com.br"
        )
        self.oauth_url = (
            "https://sandbox.gerencianet.com.br/oauth/authorize" if sandbox
            else "https://api.gerencianet.com.br/oauth/authorize"
        )
        self.token = None
        self._authenticate()
    
    def _authenticate(self) -> str:
        """Autentica com Gerencianet e obtém token de acesso"""
        url = f"{self.base_url}/oauth/token"
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        try:
            response = requests.post(url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            
            self.token = response.json()["access_token"]
            return self.token
        
        except requests.exceptions.RequestException as e:
            raise ValidationException(f"Erro ao autenticar com Gerencianet: {str(e)}")
    
    def _get_headers(self) -> Dict[str, str]:
        """Retorna headers padrão com autenticação"""
        if not self.token:
            self._authenticate()
        
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
    
    def gerar_boleto(
        self,
        cliente_nome: str,
        cliente_cpf: str,
        cliente_email: str,
        valor: float,
        data_vencimento: date,
        numero_referencia: str,
        descricao: Optional[str] = None,
        juros_dia: float = 0.0,
        multa_atraso: float = 0.0
    ) -> Dict[str, Any]:
        """
        Gera um boleto no Gerencianet
        
        Args:
            cliente_nome: Nome do cliente
            cliente_cpf: CPF do cliente
            cliente_email: Email do cliente
            valor: Valor do boleto em reais
            data_vencimento: Data de vencimento
            numero_referencia: Número único para referência
            descricao: Descrição do boleto
            juros_dia: Juros de mora por dia (%)
            multa_atraso: Multa por atraso (%)
            
        Returns:
            Dict com dados do boleto gerado (código de barras, linha digitável, etc)
        """
        
        url = f"{self.base_url}/v1/charge"
        
        # Formatar CPF
        cpf_limpo = cliente_cpf.replace(".", "").replace("-", "")
        
        payload = {
            "customers": [
                {
                    "name": cliente_nome,
                    "cpf": cpf_limpo,
                    "email": cliente_email,
                    "phone": None
                }
            ],
            "charges": [
                {
                    "description": descricao or f"Boleto {numero_referencia}",
                    "reference_id": numero_referencia,
                    "amount": int(valor * 100),  # Convertendo para centavos
                    "installments": 1,
                    "payment_method": "boleto",
                    "metadata": {
                        "notification_url": f"{os.getenv('APP_URL', 'http://localhost:8000')}/webhooks/gerencianet/boleto"
                    },
                    "split_items": [],
                    "billing": {
                        "name": cliente_nome,
                        "cpf": cpf_limpo,
                        "email": cliente_email,
                        "phone_number": None,
                        "street": None,
                        "number": None,
                        "neighborhood": None,
                        "city": None,
                        "state": None,
                        "zipcode": None
                    },
                    "services": [
                        {
                            "name": "Serviço",
                            "value": int(valor * 100),
                            "quantity": 1
                        }
                    ]
                }
            ],
            "options": {
                "boleto": {
                    "expire_at": data_vencimento.isoformat(),
                    "fine": {
                        "percentage": multa_atraso
                    },
                    "interest": {
                        "percentage": juros_dia
                    }
                }
            }
        }
        
        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=payload,
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Extrair informações relevantes
            charge_id = data.get("data", {}).get("charges", [{}])[0].get("id")
            
            # Buscar detalhes do boleto gerado
            boleto_details = self._get_boleto_details(charge_id)
            
            return {
                "charge_id": charge_id,
                "numero_referencia": numero_referencia,
                "codigo_barras": boleto_details.get("codigo_barras"),
                "linha_digitavel": boleto_details.get("linha_digitavel"),
                "url_boleto": boleto_details.get("url"),
                "valor": valor,
                "data_vencimento": data_vencimento.isoformat()
            }
        
        except requests.exceptions.RequestException as e:
            raise ValidationException(f"Erro ao gerar boleto: {str(e)}")
    
    def _get_boleto_details(self, charge_id: int) -> Dict[str, Any]:
        """Obtém detalhes do boleto após sua criação"""
        
        url = f"{self.base_url}/v1/charge/{charge_id}"
        
        try:
            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json().get("data", {})
            boleto_data = data.get("boleto", {})
            
            return {
                "codigo_barras": boleto_data.get("barcode"),
                "linha_digitavel": boleto_data.get("digitable_line"),
                "url": boleto_data.get("link")
            }
        
        except requests.exceptions.RequestException as e:
            # Se falhar, retorna dict vazio - será preenchido depois
            return {}
    
    def criar_recorrencia(
        self,
        cliente_nome: str,
        cliente_cpf: str,
        cliente_email: str,
        valor_parcela: float,
        quantidade_parcelas: int,
        data_primeira_parcela: date,
        intervalo_dias: int = 30,
        descricao: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Cria uma recorrência (carnê) no Gerencianet
        
        Args:
            cliente_nome: Nome do cliente
            cliente_cpf: CPF do cliente
            cliente_email: Email do cliente
            valor_parcela: Valor de cada parcela
            quantidade_parcelas: Quantas parcelas
            data_primeira_parcela: Data do primeiro vencimento
            intervalo_dias: Dias entre as parcelas
            descricao: Descrição
            
        Returns:
            Dict com ID da recorrência e dados das parcelas
        """
        
        url = f"{self.base_url}/v1/subscription"
        
        cpf_limpo = cliente_cpf.replace(".", "").replace("-", "")
        
        payload = {
            "customers": [
                {
                    "name": cliente_nome,
                    "cpf": cpf_limpo,
                    "email": cliente_email
                }
            ],
            "subscriptions": [
                {
                    "plan_id": None,  # Será criada manualmente
                    "interval": intervalo_dias,  # em dias
                    "repeats": quantidade_parcelas,
                    "metadata": {
                        "notification_url": f"{os.getenv('APP_URL', 'http://localhost:8000')}/webhooks/gerencianet/subscription"
                    }
                }
            ],
            "charges": [
                {
                    "description": descricao or "Parcela recorrente",
                    "amount": int(valor_parcela * 100),
                    "payment_method": "boleto",
                    "services": [
                        {
                            "name": descricao or "Serviço",
                            "value": int(valor_parcela * 100),
                            "quantity": 1
                        }
                    ]
                }
            ]
        }
        
        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=payload,
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json().get("data", {})
            
            return {
                "subscription_id": data.get("subscription", {}).get("id"),
                "valor_parcela": valor_parcela,
                "quantidade_parcelas": quantidade_parcelas,
                "data_primeira_parcela": data_primeira_parcela.isoformat(),
                "intervalo_dias": intervalo_dias
            }
        
        except requests.exceptions.RequestException as e:
            raise ValidationException(f"Erro ao criar recorrência: {str(e)}")
    
    def consultar_boleto(self, charge_id: int) -> Dict[str, Any]:
        """Consulta status de um boleto"""
        
        url = f"{self.base_url}/v1/charge/{charge_id}"
        
        try:
            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json().get("data", {})
            
            return {
                "charge_id": charge_id,
                "status": data.get("status"),
                "valor": data.get("amount", 0) / 100,
                "data_vencimento": data.get("duedate"),
                "boleto": data.get("boleto", {})
            }
        
        except requests.exceptions.RequestException as e:
            raise ValidationException(f"Erro ao consultar boleto: {str(e)}")
    
    def consultar_recorrencia(self, subscription_id: int) -> Dict[str, Any]:
        """Consulta status de uma recorrência"""
        
        url = f"{self.base_url}/v1/subscription/{subscription_id}"
        
        try:
            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            
            return response.json().get("data", {})
        
        except requests.exceptions.RequestException as e:
            raise ValidationException(f"Erro ao consultar recorrência: {str(e)}")
    
    def cancelar_boleto(self, charge_id: int) -> bool:
        """Cancela um boleto"""
        
        url = f"{self.base_url}/v1/charge/{charge_id}/cancel"
        
        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                json={},
                timeout=10
            )
            response.raise_for_status()
            return True
        
        except requests.exceptions.RequestException as e:
            raise ValidationException(f"Erro ao cancelar boleto: {str(e)}")
    
    def cancelar_recorrencia(self, subscription_id: int) -> bool:
        """Cancela uma recorrência"""
        
        url = f"{self.base_url}/v1/subscription/{subscription_id}/cancel"
        
        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                json={},
                timeout=10
            )
            response.raise_for_status()
            return True
        
        except requests.exceptions.RequestException as e:
            raise ValidationException(f"Erro ao cancelar recorrência: {str(e)}")
