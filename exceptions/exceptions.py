class TransacaoFinanceiraError(Exception):
    """Excecao base para erros de transacao financeira."""


class SaldoInsuficienteError(TransacaoFinanceiraError):
    """Excecao lancada quando a conta nao possui saldo suficiente."""

    def __init__(self, conta: int, saldo_atual, valor_solicitado) -> None:
        self.conta = conta
        self.saldo_atual = saldo_atual
        self.valor_solicitado = valor_solicitado
        super().__init__(
            f"Conta {conta}: saldo insuficiente "
            f"(saldo={saldo_atual}, valor={valor_solicitado})"
        )


class ContaNaoEncontradaError(TransacaoFinanceiraError):
    """Excecao lancada quando a conta nao e encontrada no repositorio."""

    def __init__(self, conta: int) -> None:
        self.conta = conta
        super().__init__(f"Conta {conta} nao encontrada")