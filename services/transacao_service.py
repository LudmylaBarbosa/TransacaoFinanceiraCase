import threading

from models.transacao import Transacao
from models.resultado_transacao import ResultadoTransacao
from models.resultado_transacao import StatusTransacao
from repositories.repository_interface import ContaRepositoryInterface
from exceptions.exceptions import ContaNaoEncontradaError
from exceptions.exceptions import SaldoInsuficienteError


class TransacaoService:
    """Servico responsavel pela execucao de transacoes financeiras.

    Utiliza lock para garantir atomicidade das operacoes em contexto
    de execucao paralela, evitando race conditions nos saldos.
    """

    def __init__(self, repositorio: ContaRepositoryInterface) -> None:
        self._repositorio = repositorio
        self._lock = threading.Lock()

    def transferir(self, transacao: Transacao) -> ResultadoTransacao:
        """Executa uma transferencia entre duas contas.

        Retorna um ResultadoTransacao com o status e mensagem da operacao.
        """
        with self._lock:
            return self._executar_transferencia(transacao)

    def _executar_transferencia(self, transacao: Transacao) -> ResultadoTransacao:
        """Logica interna de transferencia, executada dentro do lock."""
        try:
            conta_origem = self._obter_conta(
                transacao.conta_origem
            )
            conta_destino = self._obter_conta(
                transacao.conta_destino
            )
            self._validar_saldo(transacao)

            conta_origem.debitar(transacao.valor)
            conta_destino.creditar(transacao.valor)

            self._repositorio.atualizar(conta_origem)
            self._repositorio.atualizar(conta_destino)

            mensagem = (
                f"Transacao numero {transacao.correlation_id} foi efetivada "
                f"com sucesso! Novos saldos: "
                f"Conta Origem: {conta_origem.saldo} "
                f"| Conta Destino: {conta_destino.saldo}"
            )
            print(mensagem)
            return ResultadoTransacao(
                correlation_id=transacao.correlation_id,
                status=StatusTransacao.EFETIVADA,
                mensagem=mensagem,
            )

        except ContaNaoEncontradaError as erro:
            return self._criar_resultado_cancelado(
                transacao.correlation_id, erro
            )

        except SaldoInsuficienteError as erro:
            return self._criar_resultado_cancelado(
                transacao.correlation_id, erro
            )

    def _obter_conta(self, numero_conta: str):
        """Busca uma conta no repositorio. Lanca excecao se nao encontrada."""
        conta = self._repositorio.buscar_por_numero(numero_conta)
        if conta is None:
            raise ContaNaoEncontradaError(numero_conta)
        return conta

    def _validar_saldo(self, transacao: Transacao) -> None:
        """Valida se a conta de origem possui saldo suficiente."""
        conta_origem = self._repositorio.buscar_por_numero(transacao.conta_origem)
        if not conta_origem.possui_saldo_suficiente(transacao.valor):
            raise SaldoInsuficienteError(
                conta=transacao.conta_origem,
                saldo_atual=conta_origem.saldo,
                valor_solicitado=transacao.valor,
            )

    def _criar_resultado_cancelado(
        self, correlation_id: int, erro: Exception
    ) -> ResultadoTransacao:
        """Cria um resultado de transacao cancelada a partir de uma excecao."""
        if isinstance(erro, SaldoInsuficienteError):
            status = StatusTransacao.CANCELADA_SALDO_INSUFICIENTE
        else:
            status = StatusTransacao.CANCELADA_CONTA_ORIGEM_NAO_ENCONTRADA

        mensagem = (
            f"Transacao numero {correlation_id} foi cancelada: {erro}"
        )
        print(mensagem)
        return ResultadoTransacao(
            correlation_id=correlation_id,
            status=status,
            mensagem=mensagem,
        )