from dataclasses import field, dataclass
from decimal import Decimal


@dataclass
class Conta:
    """Entidade que representa uma conta bancaria com seu saldo."""

    numero: str
    saldo: Decimal = field(default=Decimal("0"))

    def debitar(self, valor: Decimal) -> None:
        """Debita um valor do saldo da conta."""
        self.saldo -= valor

    def creditar(self, valor: Decimal) -> None:
        """Credita um valor ao saldo da conta."""
        self.saldo += valor

    def possui_saldo_suficiente(self, valor: Decimal) -> bool:
        """Verifica se a conta possui saldo suficiente para o valor informado."""
        return self.saldo >= valor