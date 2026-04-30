from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Transacao:
    "Modelo imutavel que representa uma transacao finaceira"
    
    correlation_id: int
    data_hora: str
    conta_origem: str
    conta_destino: str
    valor: Decimal