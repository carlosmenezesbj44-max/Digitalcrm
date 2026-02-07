class Servidor:
    def __init__(self, id: int, nome: str, ip: str, tipo_conexao: str, tipo_acesso: str, usuario: str, senha: str, alterar_nome: bool, ativo: bool):
        self.id = id
        self.nome = nome
        self.ip = ip
        self.tipo_conexao = tipo_conexao
        self.tipo_acesso = tipo_acesso
        self.usuario = usuario
        self.senha = senha
        self.alterar_nome = alterar_nome
        self.ativo = ativo