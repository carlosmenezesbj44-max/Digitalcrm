from crm_core.config.settings import settings
from typing import Optional
import paramiko
import time


def get_huawei_server():
    """Obtém o servidor Huawei ativo do banco de dados."""
    try:
        from crm_core.db.base import get_db_session
        from crm_modules.servidores.repository import ServidorRepository
        from crm_modules.servidores.models import ServidorModel

        db = get_db_session()
        try:
            repo = ServidorRepository(db)
            servidores = repo.listar_servidores_ativos()
            huawei_servers = [s for s in servidores if s.tipo_conexao.lower() == 'huawei']
            if huawei_servers:
                return huawei_servers[0]  # Usa o primeiro
            return None
        finally:
            db.close()
    except Exception as e:
        print(f"Erro ao obter servidor Huawei: {e}")
        return None


def sincronizar_cliente_huawei(username: str, password: str, profile: str = "default", host: Optional[str] = None, user: Optional[str] = None, secret: Optional[str] = None):
    """
    Sincroniza credenciais do cliente com Huawei PPPoE.
    """
    if not any([host, user, secret]):
        server = get_huawei_server()
        if server:
            host = server.ip
            user = server.usuario
            secret = server.senha
        else:
            host = settings.huawei_host
            user = settings.huawei_user
            secret = settings.huawei_password

    if not all([host, user, secret]):
        print("Huawei não configurado, pulando sincronização")
        return

    try:
        # Conectar via SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=secret, timeout=10)

        # Entrar no modo de configuração
        shell = ssh.invoke_shell()
        time.sleep(1)

        # Comandos Huawei para configurar PPPoE
        commands = [
            "system-view",
            f"aaa",
            f"local-user {username} password cipher {password}",
            f"local-user {username} service-type ppp",
            f"local-user {username} access-limit 1",
            "commit",
            "quit",
            "quit"
        ]

        for cmd in commands:
            shell.send(cmd + '\n')
            time.sleep(0.5)

        output = shell.recv(65535).decode('utf-8')
        ssh.close()

        if "Error" not in output:
            print(f"Usuário PPPoE criado: {username}")
        else:
            print(f"Erro ao criar usuário: {output}")

    except Exception as e:
        print(f"Erro ao sincronizar com Huawei: {e}")


def coletar_logs_huawei(host: Optional[str] = None, user: Optional[str] = None, secret: Optional[str] = None):
    """
    Coleta logs do Huawei via SSH.
    """
    try:
        if not any([host, user, secret]):
            server = get_huawei_server()
            if server:
                host = server.ip
                user = server.usuario
                secret = server.senha
            else:
                host = settings.huawei_host
                user = settings.huawei_user
                secret = settings.huawei_password

        if not all([host, user, secret]):
            print("Huawei não configurado")
            return []

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=secret, timeout=10)

        stdin, stdout, stderr = ssh.exec_command("display logbuffer")
        logs = stdout.read().decode('utf-8')
        ssh.close()

        # Processar logs (simplificado)
        log_lines = logs.split('\n')
        return log_lines

    except Exception as e:
        print(f"Erro ao coletar logs: {e}")
        return []


def monitorar_sessoes_huawei(host: Optional[str] = None, user: Optional[str] = None, secret: Optional[str] = None):
    """
    Monitora sessões PPPoE ativas no Huawei.
    """
    try:
        if not any([host, user, secret]):
            server = get_huawei_server()
            if server:
                host = server.ip
                user = server.usuario
                secret = server.senha
            else:
                host = settings.huawei_host
                user = settings.huawei_user
                secret = settings.huawei_password

        if not all([host, user, secret]):
            print("Huawei não configurado")
            return []

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=secret, timeout=10)

        stdin, stdout, stderr = ssh.exec_command("display access-user")
        sessions = stdout.read().decode('utf-8')
        ssh.close()

        # Processar sessões (simplificado)
        session_lines = sessions.split('\n')
        return session_lines

    except Exception as e:
        print(f"Erro ao monitorar sessões: {e}")
        return []
