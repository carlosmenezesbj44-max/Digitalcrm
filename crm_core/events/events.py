from abc import ABC, abstractmethod
from typing import Any


class Event(ABC):
    @abstractmethod
    def __init__(self, data: Any):
        self.data = data


class UserCreatedEvent(Event):
    def __init__(self, user_id: int, email: str):
        super().__init__({'user_id': user_id, 'email': email})


class ClientCreatedEvent(Event):
    def __init__(self, client_id: int, name: str):
        super().__init__({'client_id': client_id, 'name': name})


class OrdemServicoCreatedEvent(Event):
    def __init__(self, ordem_id: int, cliente_id: int):
        super().__init__({'ordem_id': ordem_id, 'cliente_id': cliente_id})


class ProdutoCreatedEvent(Event):
    def __init__(self, produto_id: int, nome: str):
        super().__init__({'produto_id': produto_id, 'nome': nome})
