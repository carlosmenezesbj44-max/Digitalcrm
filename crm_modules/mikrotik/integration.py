from crm_core.config.settings import settings
from typing import Optional


def get_mikrotik_server(servidor_id: int = None):
    """
    Obtém o servidor Mikrotik do banco de dados.
    
    Args:
        servidor_id: ID opcional do servidor. Se None, retorna o primeiro servidor ativo.
    """
    from crm_core.db.base import get_db_session
    from crm_modules.servidores.repository import ServidorRepository
    from crm_modules.servidores.models import ServidorModel
    
    db = get_db_session()
    try:
        repo = ServidorRepository(db)
        
        # Se foi fornecido ID, busca o servidor específico
        if servidor_id:
            servidor = repo.get_by_id(servidor_id)
            if servidor and servidor.tipo_conexao and servidor.tipo_conexao.lower() == 'mikrotik':
                return servidor
            return None
        
        # Caso contrário, busca o primeiro servidor ativo
        servidores = repo.listar_servidores_ativos()
        mikrotik_servers = [s for s in servidores if s.tipo_conexao and s.tipo_conexao.lower() == 'mikrotik']
        if mikrotik_servers:
            return mikrotik_servers[0]  # Usa o primeiro
        return None
    finally:
        db.close()


def criar_profile_mikrotik(name: str, download_limit: int, upload_limit: int, host: Optional[str] = None, user: Optional[str] = None, secret: Optional[str] = None):
    """
    Cria ou atualiza um profile PPPoE no MikroTik com limitacoes de velocidade.
    Retorna (success, message)
    """
    if not any([host, user, secret]):
        server = get_mikrotik_server()
        if server:
            host = server.ip
            user = server.usuario
            secret = server.senha
        else:
            host = settings.mikrotik_host
            user = settings.mikrotik_user
            secret = settings.mikrotik_password

    if not all([host, user, secret]):
        msg = "MikroTik nao configurado, pulando criacao de profile"
        print(msg)
        return False, msg

    try:
        import routeros_api
    except ImportError:
        error_msg = "Biblioteca 'routeros-api' nao instalada. Execute 'pip install routeros-api'."
        print(error_msg)
        return False, error_msg

    try:
        connection = routeros_api.RouterOsApiPool(
            host,
            username=user,
            password=secret,
            port=8728,
            plaintext_login=True
        )
        api = connection.get_api()

        ppp_profiles = api.get_resource('/ppp/profile')
        existing = ppp_profiles.get(name=name)

        # Verificar se ha pools disponiveis
        pools = api.get_resource('/ip/pool').get()
        pool_name = None

        if pools:
            # Usa o primeiro pool encontrado
            pool_name = pools[0]['name']
        else:
            # Cria um pool padrao se nao existir
            pool_name = "pppoe-pool"
            api.get_resource('/ip/pool').add(
                name=pool_name,
                ranges="192.168.1.100-192.168.1.200"
            )

        if existing:
            # Atualizar profile
            update_params = {
                'rate_limit': f"{upload_limit}M/{download_limit}M",
                'remote_address': pool_name
            }
            # Opcionalmente, adiciona local_address se configurado
            if settings.mikrotik_local_address:
                update_params['local_address'] = settings.mikrotik_local_address

            ppp_profiles.set(
                id=existing[0]['id'],
                **update_params
            )
            msg = f"Profile PPPoE atualizado: {name}"
            print(msg)
            connection.disconnect()
            return True, msg
        else:
            # Criar novo profile
            create_params = {
                'name': name,
                'rate_limit': f"{upload_limit}M/{download_limit}M",
                'remote_address': pool_name
            }
            # Opcionalmente, adiciona local_address se configurado
            if settings.mikrotik_local_address:
                create_params['local_address'] = settings.mikrotik_local_address

            ppp_profiles.add(
                **create_params
            )
            msg = f"Profile PPPoE criado: {name}"
            print(msg)
            connection.disconnect()
            return True, msg

    except Exception as e:
        msg = f"Erro ao criar profile no MikroTik: {e}"
        print(msg)
        return False, msg


def sincronizar_cliente_mikrotik(username: str, password: str, profile: str = "default", host: Optional[str] = None, user: Optional[str] = None, secret: Optional[str] = None):
    """
    Sincroniza credenciais do cliente com MikroTik PPPoE secrets.
    """
    if not any([host, user, secret]):
        server = get_mikrotik_server()
        if server:
            host = server.ip
            user = server.usuario
            secret = server.senha
        else:
            host = settings.mikrotik_host
            user = settings.mikrotik_user
            secret = settings.mikrotik_password

    if not all([host, user, secret]):
        print("MikroTik não configurado, pulando sincronização")
        return

    try:
        import routeros_api
    except ImportError:
        error_msg = "Biblioteca 'routeros-api' não instalada. Execute 'pip install routeros-api'."
        print(error_msg)
        raise Exception(error_msg)

    try:
        connection = routeros_api.RouterOsApiPool(
            host,
            username=user,
            password=secret,
            port=8728,
            plaintext_login=True
        )
        api = connection.get_api()

        # Verificar se o secret já existe
        ppp_secrets = api.get_resource('/ppp/secret')
        existing = ppp_secrets.get(name=username)

        if existing:
            # Atualizar
            ppp_secrets.set(id=existing[0]['id'], password=password, profile=profile)
            print(f"Secret PPPoE atualizado: {username}")
        else:
            # Criar novo
            ppp_secrets.add(name=username, password=password, profile=profile, service="pppoe")
            print(f"Secret PPPoE criado: {username}")

        connection.disconnect()

    except Exception as e:
        print(f"Erro ao sincronizar com MikroTik: {e}")
        # Não falhar o cadastro por erro na sincronização


def coletar_logs_mikrotik(host: Optional[str] = None, user: Optional[str] = None, secret: Optional[str] = None):
    """
    Coleta logs do MikroTik.
    Tenta múltiplas abordagens para obter os logs.
    """
    if not any([host, user, secret]):
        server = get_mikrotik_server()
        if server:
            host = server.ip
            user = server.usuario
            secret = server.senha
        else:
            host = settings.mikrotik_host
            user = settings.mikrotik_user
            secret = settings.mikrotik_password

    if not all([host, user, secret]):
        error_msg = "MikroTik não configurado. Verifique as configurações no menu Servidores."
        print(error_msg)
        raise Exception(error_msg)

    try:
        import routeros_api

        connection = routeros_api.RouterOsApiPool(
            host,
            username=user,
            password=secret,
            port=8728,
            plaintext_login=True
        )
        api = connection.get_api()
        
        logs = []
        
        # Tentar endpoint /log primeiro
        try:
            log_resource = api.get_resource('/log')
            logs = log_resource.get()
        except Exception as e:
            print(f"Erro ao acessar /log: {e}")
            
            # Tentar alternativa: /system/history
            try:
                history_resource = api.get_resource('/system/history')
                logs = history_resource.get()
                # Converter formato do history para formato de log
                if logs:
                    logs = [
                        {
                            'time': log.get('time', ''),
                            'topics': 'system',
                            'message': log.get('message', ''),
                            'id': log.get('id', '')
                        }
                        for log in logs
                    ]
            except Exception as e2:
                print(f"Erro ao acessar /system/history: {e2}")
        
        connection.disconnect()
        
        # Processar logs para garantir formato consistente
        processed_logs = []
        for log in logs:
            processed_logs.append({
                'time': log.get('time', log.get('data_hora', '')),
                'topics': log.get('topics', log.get('tipo', 'INFO')),
                'message': log.get('message', log.get('mensagem', '')),
                'id': log.get('id', ''),
                'servidor_nome': log.get('servidor_nome', 'MikroTik')
            })
        
        return processed_logs

    except Exception as e:
        error_msg = f"Erro ao conectar ao MikroTalk ({host}): {str(e)}"
        print(error_msg)
        raise Exception(error_msg)


def monitorar_sessoes_mikrotik(host: Optional[str] = None, user: Optional[str] = None, secret: Optional[str] = None):
    """
    Monitora sessões PPPoE ativas no MikroTik.
    """
    if not any([host, user, secret]):
        server = get_mikrotik_server()
        if server:
            host = server.ip
            user = server.usuario
            secret = server.senha
        else:
            host = settings.mikrotik_host
            user = settings.mikrotik_user
            secret = settings.mikrotik_password

    if not all([host, user, secret]):
        print("MikroTik não configurado")
        return []

    try:
        import routeros_api

        connection = routeros_api.RouterOsApiPool(
            host,
            username=user,
            password=secret,
            port=8728,
            plaintext_login=True
        )
        api = connection.get_api()

        active_sessions = api.get_resource('/ppp/active').get()
        connection.disconnect()
        return active_sessions

    except Exception as e:
        print(f"Erro ao monitorar sessões: {e}")
        return []
