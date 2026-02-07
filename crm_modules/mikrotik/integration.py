from crm_core.config.settings import settings
from typing import Optional


def get_mikrotik_server():
    """Obtém o servidor Mikrotik ativo do banco de dados."""
    from crm_core.db.base import get_db_session
    from crm_modules.servidores.repository import ServidorRepository
    from crm_modules.servidores.models import ServidorModel
    
    db = get_db_session()
    try:
        repo = ServidorRepository(db)
        servidores = repo.listar_servidores_ativos()
        mikrotik_servers = [s for s in servidores if s.tipo_conexao.lower() == 'mikrotik']
        if mikrotik_servers:
            return mikrotik_servers[0]  # Usa o primeiro
        return None
    finally:
        db.close()


def criar_profile_mikrotik(name: str, download_limit: int, upload_limit: int, host: Optional[str] = None, user: Optional[str] = None, secret: Optional[str] = None):
    """
    Cria ou atualiza um profile PPPoE no MikroTik com limitações de velocidade.
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
        print("MikroTik não configurado, pulando criação de profile")
        return False

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

        ppp_profiles = api.get_resource('/ppp/profile')
        existing = ppp_profiles.get(name=name)

        # Verificar se há pools disponíveis
        pools = api.get_resource('/ip/pool').get()
        pool_name = None
        
        if pools:
            # Usa o primeiro pool encontrado
            pool_name = pools[0]['name']
        else:
            # Cria um pool padrão se não existir
            pool_name = "pppoe-pool"
            api.get_resource('/ip/pool').add(
                name=pool_name,
                ranges="192.168.1.100-192.168.1.200"
            )

        if existing:
            # Atualizar profile
            ppp_profiles.set(
                id=existing[0]['id'],
                rate_limit=f"{upload_limit}M/{download_limit}M",
                local_address="192.168.1.1",
                remote_address=pool_name
            )
            print(f"Profile PPPoE atualizado: {name}")
        else:
            # Criar novo profile
            ppp_profiles.add(
                name=name,
                rate_limit=f"{upload_limit}M/{download_limit}M",
                local_address="192.168.1.1",
                remote_address=pool_name
            )
            print(f"Profile PPPoE criado: {name}")

        connection.disconnect()
        return True

    except Exception as e:
        print(f"Erro ao criar profile no MikroTik: {e}")
        return False


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

        log_resource = api.get_resource('/log')
        logs = log_resource.get()
        connection.disconnect()
        return logs

    except Exception as e:
        error_msg = f"Erro ao conectar ao MikroTik ({host}): {str(e)}"
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
        import librouteros

        # Usar librouteros para alternativa
        api = librouteros.connect(
            host=host,
            username=user,
            password=secret
        )

        active_sessions = api('/ppp/active/print')
        api.close()
        return list(active_sessions)

    except Exception as e:
        print(f"Erro ao monitorar sessões: {e}")
        return []