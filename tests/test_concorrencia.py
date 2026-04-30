from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor

from models.conta import Conta
from models.transacao import Transacao
from repositories.repository_memory import ContaRepositoryMemory
from services.transacao_service import TransacaoService


def _criar_transacao(correlation_id: int, origem: str, destino: str, valor: str):
    return Transacao(
        correlation_id=correlation_id,
        data_hora="01/01/2024 00:00:00",
        conta_origem=origem,
        conta_destino=destino,
        valor=Decimal(valor),
    )


class TestConcorrenciaRaceCondition:
    def test_transferencias_paralelas_mesma_conta_origem(self):
        contas = [
            Conta(numero="100", saldo=Decimal("180")),
            Conta(numero="200", saldo=Decimal("0")),
            Conta(numero="300", saldo=Decimal("0")),
        ]
        repositorio = ContaRepositoryMemory(contas)
        servico = TransacaoService(repositorio)

        with ThreadPoolExecutor(max_workers=2) as executor:
            futuro_a = executor.submit(
                servico.transferir, _criar_transacao(1, "100", "200", "150")
            )
            futuro_b = executor.submit(
                servico.transferir, _criar_transacao(2, "100", "300", "150")
            )

        resultado_a = futuro_a.result()
        resultado_b = futuro_b.result()

        uma_sucesso_outra_falha = (
            (resultado_a.sucesso and not resultado_b.sucesso) or
            (not resultado_a.sucesso and resultado_b.sucesso)
        )
        assert uma_sucesso_outra_falha, (
            "Apenas uma transferência deveria ter sucesso com saldo de 180"
        )

        saldo_final = repositorio.buscar_por_numero("100").saldo
        assert saldo_final == Decimal("30")


    def test_transferencias_paralelas_contas_diferentes(self):
        contas = [
            Conta(numero="100", saldo=Decimal("500")),
            Conta(numero="200", saldo=Decimal("500")),
            Conta(numero="300", saldo=Decimal("0")),
            Conta(numero="400", saldo=Decimal("0")),
        ]

        repositorio = ContaRepositoryMemory(contas)
        servico = TransacaoService(repositorio)

        with ThreadPoolExecutor(max_workers=2) as executor:
            futuro_a = executor.submit(
                servico.transferir, _criar_transacao(1, "100", "300", "100")
            )
            futuro_b = executor.submit(
                servico.transferir, _criar_transacao(2, "200", "400", "200")
            )

        assert futuro_a.result().sucesso is True
        assert futuro_b.result().sucesso is True

        assert repositorio.buscar_por_numero("100").saldo == Decimal("400")
        assert repositorio.buscar_por_numero("200").saldo == Decimal("300")
        assert repositorio.buscar_por_numero("300").saldo == Decimal("100")
        assert repositorio.buscar_por_numero("400").saldo == Decimal("200")


    def test_cenario_completo_oito_transacoes(self):
        contas = [
            Conta(numero="938485762", saldo=Decimal("180")),
            Conta(numero="347586970", saldo=Decimal("1200")),
            Conta(numero="2147483649", saldo=Decimal("0")),
            Conta(numero="675869708", saldo=Decimal("4900")),
            Conta(numero="238596054", saldo=Decimal("478")),
            Conta(numero="573659065", saldo=Decimal("787")),
            Conta(numero="210385733", saldo=Decimal("10")),
            Conta(numero="674038564", saldo=Decimal("400")),
            Conta(numero="563856300", saldo=Decimal("1200")),
        ]

        soma_inicial = sum(c.saldo for c in contas)

        repositorio = ContaRepositoryMemory(contas)
        servico = TransacaoService(repositorio)

        transacoes = [
            _criar_transacao(1, "938485762", "2147483649", "150"),
            _criar_transacao(2, "2147483649", "210385733", "149"),
            _criar_transacao(3, "347586970", "238596054", "1100"),
            _criar_transacao(4, "675869708", "210385733", "5300"),
            _criar_transacao(5, "238596054", "674038564", "1489"),
            _criar_transacao(6, "573659065", "563856300", "49"),
            _criar_transacao(7, "938485762", "2147483649", "44"),
            _criar_transacao(8, "573659065", "675869708", "150"),
        ]

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(servico.transferir, t) for t in transacoes
            ]

        resultados = [f.result() for f in futures]

        soma_final = sum(c.saldo for c in repositorio.listar_todas())

        assert soma_final == soma_inicial, (
        )

        efetivadas = [r for r in resultados if r.sucesso]
        canceladas = [r for r in resultados if not r.sucesso]

        assert len(efetivadas) + len(canceladas) == 8


    def test_muitas_transferencias_paralelas_saldo_nao_fica_negativo(self):
        contas = [
            Conta(numero="100", saldo=Decimal("100")),
            Conta(numero="200", saldo=Decimal("0")),
        ]

        repositorio = ContaRepositoryMemory(contas)
        servico = TransacaoService(repositorio)

        transacoes = [
            _criar_transacao(i, "100", "200", "10") for i in range(20)
        ]

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(servico.transferir, t) for t in transacoes
            ]

        resultados = [f.result() for f in futures]

        efetivadas = [r for r in resultados if r.sucesso]

        assert len(efetivadas) == 10

        saldo_origem = repositorio.buscar_por_numero("100").saldo
        assert saldo_origem == Decimal("0")
        assert saldo_origem >= Decimal("0"), "Saldo nao pode ficar negativo"

        saldo_destino = repositorio.buscar_por_numero("200").saldo
        assert saldo_destino == Decimal("100")
