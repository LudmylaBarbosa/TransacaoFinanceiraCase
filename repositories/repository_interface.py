from abc import ABC
from abc import abstractmethod
from typing import Optional

from models.conta import Conta


class ContaRepositoryInterface(ABC):
    """Interface abstrata para acesso a dados de contas (Repository Pattern)."""

    @abstractmethod
    def buscar_por_numero(self, numero: str) -> Optional[Conta]:
        """Busca uma conta pelo numero."""

    @abstractmethod
    def atualizar(self, conta: Conta) -> bool:
        """Atualiza os dados de uma conta no repositorio."""

    @abstractmethod
    def listar_todas(self) -> list:
        """Lista todas as contas do repositorio."""