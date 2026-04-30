from dataclasses import dataclass
from enum import Enum


class StatusTransacao(Enum):
    """Enum que representa os possiveis status de uma transacao."""

    EFETIVADA = "efetivada"
    CANCELADA_SALDO_INSUFICIENTE = "cancelada_saldo_insuficiente"
    CANCELADA_CONTA_ORIGEM_NAO_ENCONTRADA = "cancelada_conta_origem_nao_encontrada"
    CANCELADA_CONTA_DESTINO_NAO_ENCONTRADA = "cancelada_conta_destino_nao_encontrada"


@dataclass(frozen=True)
class ResultadoTransacao:
    """Resultado imutavel de uma transacao financeira."""

    correlation_id: int
    status: StatusTransacao
    mensagem: str

    @property
    def sucesso(self) -> bool:
        """Retorna True se a transacao foi efetivada com sucesso."""
        return self.status == StatusTransacao.EFETIVADA