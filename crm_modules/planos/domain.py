from typing import Optional


class Plano:
    def __init__(self, id: int, nome: str, velocidade_download: int, velocidade_upload: int, valor_mensal: float, descricao: Optional[str] = None, ativo: bool = True):
        self.id = id
        self.nome = nome
        self.velocidade_download = velocidade_download
        self.velocidade_upload = velocidade_upload
        self.valor_mensal = valor_mensal
        self.descricao = descricao
        self.ativo = ativo