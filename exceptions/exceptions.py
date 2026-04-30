class TransacaoFinanceiraError(Exception):    
    pass
    
class SaldoInsuficienteError(TransacaoFinanceiraError):
    def __init__(self, conta: int, saldo_atual, valor_solicitado) -> None:
        self.conta = conta
        self.saldo_atual = saldo_atual
        self.valor_solicitado = valor_solicitado
        super().__init__(
            f"Conta {conta}: saldo insuficiente "
            f"(saldo={saldo_atual}, valor={valor_solicitado})"
        )


class ContaNaoEncontradaError(TransacaoFinanceiraError):
    def __init__(self, conta: int) -> None:
        self.conta = conta
        super().__init__(f"Conta {conta} nao encontrada")
