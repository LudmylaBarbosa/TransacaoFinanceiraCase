from typing import List, Optional

from models.conta import Conta
from repositories.repository_interface import ContaRepositoryInterface


class ContaRepositoryMemory(ContaRepositoryInterface):

    def __init__(self, contas_iniciais: List[Conta]) -> None:
        self._contas: dict = {}
        for conta in contas_iniciais:
            self._contas[conta.numero] = conta

    def buscar_por_numero(self, numero: str) -> Optional[Conta]:
        return self._contas.get(numero)

    def atualizar(self, conta: Conta) -> bool:
        try:
            self._contas[conta.numero] = conta
            return True
        except Exception as erro:
            print(f"Erro ao atualizar conta: {erro}")
            return False

    def listar_todas(self) -> List[Conta]:
        return list(self._contas.values())
