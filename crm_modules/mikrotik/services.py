#!/usr/bin/env python3
"""
Serviços de integração com MikroTik para operações em tempo real
"""

from typing import Optional, List, Dict, Any
from crm_core.config.settings import settings
from crm_modules.mikrotik.integration import (
    get_mikrotik_server,
    criar_profile_mikrotik,
    sincronizar_cliente_mikrotik,
    coletar_logs_mikrotik,
    monitorar_sessoes_mikrotik
)
from crm_modules.clientes.models import ClienteModel
from crm_modules.contratos.models import ContratoModel


class MikrotikService:
    """Serviço para operações em tempo real com MikroTik"""
    
    def __init__(self):
        self.server = get_mikrotik_server()
        
    def obter_configuracoes(self):
        """Obtém as configurações atuais do MikroTik"""
        if not self.server:
            return {
                'status': 'error',
                'message': 'Nenhum servidor MikroTik configurado'
            }
        
        try:
            import routeros_api
            
            connection = routeros_api.RouterOsApiPool(
                self.server.ip,
                username=self.server.usuario,
                password=self.server.senha,
                port=8728,
                plaintext_login=True
            )
            api = connection.get_api()
            
            # Obter informações do sistema
            system_resource = api.get_resource('/system/resource')
            system_info = system_resource.get()[0]
            
            # Obter pools de endereços
            pools = api.get_resource('/ip/pool').get()
            
            # Obter profiles PPPoE
            profiles = api.get_resource('/ppp/profile').get()
            
            # Obter secrets PPPoE
            secrets = api.get_resource('/ppp/secret').get()
            
            connection.disconnect()
            
            return {
                'status': 'success',
                'server': {
                    'name': self.server.nome,
                    'ip': self.server.ip,
                    'device': system_info.get('board-name', 'Desconhecido'),
                    'version': system_info.get('version', 'Desconhecido')
                },
                'pools': pools,
                'profiles': profiles,
                'secrets': secrets,
                'total_secrets': len(secrets)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erro ao obter configurações: {str(e)}'
            }
    
    def criar_profile_real_time(self, name: str, download_limit: int, upload_limit: int) -> Dict[str, Any]:
        """Cria um profile PPPoE em tempo real"""
        try:
            success = criar_profile_mikrotik(
                name=name,
                download_limit=download_limit,
                upload_limit=upload_limit,
                host=self.server.ip if self.server else None,
                user=self.server.usuario if self.server else None,
                secret=self.server.senha if self.server else None
            )
            
            return {
                'status': 'success' if success else 'error',
                'message': f'Profile {name} criado com sucesso' if success else f'Falha ao criar profile {name}'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erro ao criar profile: {str(e)}'
            }
    
    def sincronizar_cliente_real_time(self, cliente: ClienteModel, contrato: ContratoModel) -> Dict[str, Any]:
        """Sincroniza um cliente com o MikroTik em tempo real"""
        try:
            # Gerar credenciais baseadas no cliente
            username = f"{cliente.nome.replace(' ', '_').lower()}_{cliente.id}"
            password = contrato.senha_pppoe or "senha123"
            profile = contrato.plano_internet or "default"
            
            sincronizar_cliente_mikrotik(
                username=username,
                password=password,
                profile=profile,
                host=self.server.ip if self.server else None,
                user=self.server.usuario if self.server else None,
                secret=self.server.senha if self.server else None
            )
            
            return {
                'status': 'success',
                'message': f'Cliente {cliente.nome} sincronizado com sucesso',
                'credentials': {
                    'username': username,
                    'password': password,
                    'profile': profile
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erro ao sincronizar cliente: {str(e)}'
            }
    
    def bloquear_cliente_real_time(self, username: str) -> Dict[str, Any]:
        """Bloqueia um cliente no MikroTik em tempo real"""
        try:
            if not self.server:
                return {'status': 'error', 'message': 'Nenhum servidor MikroTik configurado'}
            
            import routeros_api
            
            connection = routeros_api.RouterOsApiPool(
                self.server.ip,
                username=self.server.usuario,
                password=self.server.senha,
                port=8728,
                plaintext_login=True
            )
            api = connection.get_api()
            
            # Verificar se o secret existe
            ppp_secrets = api.get_resource('/ppp/secret')
            existing = ppp_secrets.get(name=username)
            
            if existing:
                # Bloquear o secret
                ppp_secrets.set(id=existing[0]['id'], disabled='yes')
                connection.disconnect()
                return {
                    'status': 'success',
                    'message': f'Cliente {username} bloqueado com sucesso'
                }
            else:
                connection.disconnect()
                return {
                    'status': 'error',
                    'message': f'Cliente {username} não encontrado no MikroTik'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erro ao bloquear cliente: {str(e)}'
            }
    
    def desbloquear_cliente_real_time(self, username: str) -> Dict[str, Any]:
        """Desbloqueia um cliente no MikroTik em tempo real"""
        try:
            if not self.server:
                return {'status': 'error', 'message': 'Nenhum servidor MikroTik configurado'}
            
            import routeros_api
            
            connection = routeros_api.RouterOsApiPool(
                self.server.ip,
                username=self.server.usuario,
                password=self.server.senha,
                port=8728,
                plaintext_login=True
            )
            api = connection.get_api()
            
            # Verificar se o secret existe
            ppp_secrets = api.get_resource('/ppp/secret')
            existing = ppp_secrets.get(name=username)
            
            if existing:
                # Desbloquear o secret
                ppp_secrets.set(id=existing[0]['id'], disabled='no')
                connection.disconnect()
                return {
                    'status': 'success',
                    'message': f'Cliente {username} desbloqueado com sucesso'
                }
            else:
                connection.disconnect()
                return {
                    'status': 'error',
                    'message': f'Cliente {username} não encontrado no MikroTik'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erro ao desbloquear cliente: {str(e)}'
            }
    
    def obter_sessoes_ativas(self) -> Dict[str, Any]:
        """Obtém as sessões PPPoE ativas em tempo real"""
        try:
            sessions = monitorar_sessoes_mikrotik(
                host=self.server.ip if self.server else None,
                user=self.server.usuario if self.server else None,
                secret=self.server.senha if self.server else None
            )
            
            return {
                'status': 'success',
                'sessions': sessions,
                'total': len(sessions)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erro ao obter sessões: {str(e)}'
            }
    
    def obter_logs_recentes(self, limit: int = 50) -> Dict[str, Any]:
        """Obtém logs recentes do MikroTik"""
        try:
            logs = coletar_logs_mikrotik(
                host=self.server.ip if self.server else None,
                user=self.server.usuario if self.server else None,
                secret=self.server.senha if self.server else None
            )
            
            # Filtrar e ordenar logs
            recent_logs = sorted(logs, key=lambda x: x.get('time', ''), reverse=True)[:limit]
            
            return {
                'status': 'success',
                'logs': recent_logs,
                'total': len(recent_logs)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erro ao obter logs: {str(e)}'
            }
    
    def atualizar_credential_cliente(self, username: str, new_password: str, new_profile: str = None) -> Dict[str, Any]:
        """Atualiza as credenciais de um cliente no MikroTik"""
        try:
            if not self.server:
                return {'status': 'error', 'message': 'Nenhum servidor MikroTik configurado'}
            
            import routeros_api
            
            connection = routeros_api.RouterOsApiPool(
                self.server.ip,
                username=self.server.usuario,
                password=self.server.senha,
                port=8728,
                plaintext_login=True
            )
            api = connection.get_api()
            
            # Verificar se o secret existe
            ppp_secrets = api.get_resource('/ppp/secret')
            existing = ppp_secrets.get(name=username)
            
            if existing:
                # Atualizar as credenciais
                update_data = {'password': new_password}
                if new_profile:
                    update_data['profile'] = new_profile
                
                ppp_secrets.set(id=existing[0]['id'], **update_data)
                connection.disconnect()
                
                return {
                    'status': 'success',
                    'message': f'Credenciais do cliente {username} atualizadas com sucesso'
                }
            else:
                connection.disconnect()
                return {
                    'status': 'error',
                    'message': f'Cliente {username} não encontrado no MikroTik'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erro ao atualizar credenciais: {str(e)}'
            }

    def desconectar_sessao(self, session_id: str) -> Dict[str, Any]:
        """Desconecta uma sessão ativa no MikroTik"""
        try:
            if not self.server:
                return {'status': 'error', 'message': 'Nenhum servidor MikroTik configurado'}
            
            import routeros_api
            
            connection = routeros_api.RouterOsApiPool(
                self.server.ip,
                username=self.server.usuario,
                password=self.server.senha,
                port=8728,
                plaintext_login=True
            )
            api = connection.get_api()
            
            # Remover a sessão ativa (geralmente em /ppp/active)
            ppp_active = api.get_resource('/ppp/active')
            ppp_active.remove(id=session_id)
            
            connection.disconnect()
            
            return {
                'status': 'success',
                'message': f'Sessão {session_id} desconectada com sucesso'
            }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erro ao desconectar sessão: {str(e)}'
            }


# Funções de utilidade para integração com outros módulos
def sincronizar_contrato_com_mikrotik(contrato: ContratoModel) -> Dict[str, Any]:
    """Função de utilidade para sincronizar um contrato com o MikroTik"""
    service = MikrotikService()
    
    # Verificar se o contrato tem cliente associado
    if not contrato.cliente:
        return {
            'status': 'error',
            'message': 'Contrato não possui cliente associado'
        }
    
    # Criar profile se necessário
    if contrato.plano_internet and contrato.velocidade_download and contrato.velocidade_upload:
        profile_result = service.criar_profile_real_time(
            name=contrato.plano_internet,
            download_limit=contrato.velocidade_download,
            upload_limit=contrato.velocidade_upload
        )
        
        if profile_result['status'] == 'error':
            # Não falhar a sincronização por erro no profile
            print(f"Aviso: Não foi possível criar profile: {profile_result['message']}")
    
    # Sincronizar cliente
    return service.sincronizar_cliente_real_time(contrato.cliente, contrato)


def bloquear_contrato_no_mikrotik(contrato: ContratoModel) -> Dict[str, Any]:
    """Função de utilidade para bloquear um contrato no MikroTik"""
    service = MikrotikService()
    
    # Gerar username baseado no cliente
    username = f"{contrato.cliente.nome.replace(' ', '_').lower()}_{contrato.cliente.id}"
    
    return service.bloquear_cliente_real_time(username)


def desbloquear_contrato_no_mikrotik(contrato: ContratoModel) -> Dict[str, Any]:
    """Função de utilidade para desbloquear um contrato no MikroTik"""
    service = MikrotikService()
    
    # Gerar username baseado no cliente
    username = f"{contrato.cliente.nome.replace(' ', '_').lower()}_{contrato.cliente.id}"
    
    return service.desbloquear_cliente_real_time(username)