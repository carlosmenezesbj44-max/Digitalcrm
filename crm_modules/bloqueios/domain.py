from typing import Optional


class PlanoBloqueio:
    def __init__(self, id: int, nome: str, ip_privado: str, reduzir_velocidade: bool = False, dias_bloqueio: int = 0, tipo_bloqueio: str = "bloqueio_total", ativo: bool = True):
        self.id = id
        self.nome = nome
        self.ip_privado = ip_privado
        self.reduzir_velocidade = reduzir_velocidade
        self.dias_bloqueio = dias_bloqueio
        self.tipo_bloqueio = tipo_bloqueio
        self.ativo = ativo