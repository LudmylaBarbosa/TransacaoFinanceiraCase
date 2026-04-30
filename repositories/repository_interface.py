from abc import ABC
from abc import abstractmethod
from typing import Optional

from models.conta import Conta


class ContaRepositoryInterface(ABC):

    @abstractmethod
    def buscar_por_numero(self, numero: str) -> Optional[Conta]:

    @abstractmethod
    def atualizar(self, conta: Conta) -> bool:

    @abstractmethod
    def listar_todas(self) -> list:
