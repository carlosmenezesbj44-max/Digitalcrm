import sys
sys.path.append('.')

from crm_core.db.base import get_db_session
from crm_modules.usuarios.models import Permissao, Usuario

def populate_permissions():
    db = get_db_session()
    try:
        # Criar permissões padrão
        permissoes = [
            {"nome": "read_clientes", "descricao": "Ler clientes", "modulo": "clientes"},
            {"nome": "write_clientes", "descricao": "Editar clientes", "modulo": "clientes"},
            {"nome": "create_clientes", "descricao": "Criar clientes", "modulo": "clientes"},
            {"nome": "delete_clientes", "descricao": "Excluir clientes", "modulo": "clientes"},

            {"nome": "read_planos", "descricao": "Ler planos", "modulo": "planos"},
            {"nome": "write_planos", "descricao": "Editar planos", "modulo": "planos"},
            {"nome": "create_planos", "descricao": "Criar planos", "modulo": "planos"},

            {"nome": "read_ordens", "descricao": "Ler ordens de serviço", "modulo": "ordens"},
            {"nome": "write_ordens", "descricao": "Editar ordens", "modulo": "ordens"},
            {"nome": "create_ordens", "descricao": "Criar ordens", "modulo": "ordens"},

            {"nome": "read_dashboard", "descricao": "Acessar dashboard", "modulo": "dashboard"},
            {"nome": "manage_usuarios", "descricao": "Gerenciar usuários", "modulo": "usuarios"},
        ]

        for perm_data in permissoes:
            existing = db.query(Permissao).filter(Permissao.nome == perm_data["nome"]).first()
            if not existing:
                perm = Permissao(**perm_data)
                db.add(perm)
                print(f"Criada permissão: {perm_data['nome']}")

        # Atribuir permissões ao admin
        admin = db.query(Usuario).filter(Usuario.username == "admin").first()
        if admin:
            for perm_nome in ["manage_usuarios", "read_dashboard"]:
                perm = db.query(Permissao).filter(Permissao.nome == perm_nome).first()
                if perm and perm not in admin.permissoes:
                    admin.permissoes.append(perm)
                    print(f"Atribuída permissão {perm_nome} ao admin")

        db.commit()
        print("Permissões populadas com sucesso!")

    except Exception as e:
        db.rollback()
        print(f"Erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_permissions()