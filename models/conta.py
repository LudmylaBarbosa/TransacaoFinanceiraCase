from dataclasses import field, dataclass
from decimal import Decimal


@dataclass
class Conta:

    numero: str
    saldo: Decimal = field(default=Decimal("0"))

    def debitar(self, valor: Decimal) -> None:
        self.saldo -= valor

    def creditar(self, valor: Decimal) -> None:
        self.saldo += valor

    def possui_saldo_suficiente(self, valor: Decimal) -> bool:
        return self.saldo >= valor
