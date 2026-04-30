from decimal import Decimal
from unittest.mock import MagicMock

from models.conta import Conta
from models.transacao import Transacao
from models.resultado_transacao import StatusTransacao
from repositories.repository_memory import ContaRepositoryMemory
from services.transacao_service import TransacaoService


def _criar_transacao(correlation_id, origem, destino, valor):
    return Transacao(
        correlation_id=correlation_id,
        data_hora="01/01/2024 00:00:00",
        conta_origem=origem,
        conta_destino=destino,
        valor=Decimal(str(valor)),
    )


class TestTransacaoServiceTransferirSucesso:
    def test_transferencia_com_saldo_suficiente(self):
        contas = [
            Conta(numero="100", saldo=Decimal("500")),
            Conta(numero="200", saldo=Decimal("100")),
        ]
        repositorio = ContaRepositoryMemory(contas)
        servico = TransacaoService(repositorio)

        resultado = servico.transferir(_criar_transacao(1, "100", "200", "150"))

        assert resultado.sucesso is True
        assert resultado.status == StatusTransacao.EFETIVADA
        assert repositorio.buscar_por_numero("100").saldo == Decimal("350")
        assert repositorio.buscar_por_numero("200").saldo == Decimal("250")

    def test_transferencia_com_saldo_exato(self):
        contas = [
            Conta(numero="100", saldo=Decimal("200")),
            Conta(numero="200", saldo=Decimal("0")),
        ]
        repositorio = ContaRepositoryMemory(contas)
        servico = TransacaoService(repositorio)

        resultado = servico.transferir(_criar_transacao(1, "100", "200", "200"))

        assert resultado.sucesso is True
        assert repositorio.buscar_por_numero("100").saldo == Decimal("0")
        assert repositorio.buscar_por_numero("200").saldo == Decimal("200")

def test_transferencia_atualiza_repositorio():
    repositorio_mock = MagicMock()
    conta_origem = Conta(numero="100", saldo=Decimal("500"))
    conta_destino = Conta(numero="200", saldo=Decimal("100"))
    repositorio_mock.buscar_por_numero.side_effect = lambda n: (
        conta_origem if n == "100" else conta_destino
    )
    repositorio_mock.atualizar.return_value = True

    servico = TransacaoService(repositorio_mock)
    servico.transferir(_criar_transacao(1, "100", "200", "150"))

    assert repositorio_mock.atualizar.call_count == 2

def test_mensagem_contem_novos_saldos():
    contas = [
        Conta(numero="100", saldo=Decimal("500")),
        Conta(numero="200", saldo=Decimal("100")),
    ]
    repositorio = ContaRepositoryMemory(contas)
    servico = TransacaoService(repositorio)

    resultado = servico.transferir(_criar_transacao(1, "100", "200", "150"))

    assert "350" in resultado.mensagem
    assert "250" in resultado.mensagem


class TestTransacaoServiceTransferirFalha:
    def test_transferencia_saldo_insuficiente(self):
        contas = [
            Conta(numero="100", saldo=Decimal("50")),
            Conta(numero="200", saldo=Decimal("100")),
        ]
        repositorio = ContaRepositoryMemory(contas)
        servico = TransacaoService(repositorio)

        resultado = servico.transferir(_criar_transacao(1, "100", "200", "150"))

        assert resultado.sucesso is False
        assert resultado.status == StatusTransacao.CANCELADA_SALDO_INSUFICIENTE
        assert repositorio.buscar_por_numero("100").saldo == Decimal("50")
        assert repositorio.buscar_por_numero("200").saldo == Decimal("100")

    def test_transferencia_conta_origem_inexistente(self):
        contas = [Conta(numero="200", saldo=Decimal("100"))]
        repositorio = ContaRepositoryMemory(contas)
        servico = TransacaoService(repositorio)

        resultado = servico.transferir(_criar_transacao(1, "999", "200", "50"))

        assert resultado.sucesso is False
        assert resultado.status == StatusTransacao.CANCELADA_CONTA_ORIGEM_NAO_ENCONTRADA

    def test_transferencia_conta_destino_inexistente(self):
        contas = [Conta(numero="100", saldo=Decimal("500"))]
        repositorio = ContaRepositoryMemory(contas)
        servico = TransacaoService(repositorio)

        resultado = servico.transferir(_criar_transacao(1, "100", "999", "50"))

        assert resultado.sucesso is False
        assert repositorio.buscar_por_numero("100").saldo == Decimal("500")

    def test_transferencia_saldo_zero(self):
        contas = [
            Conta(numero="100", saldo=Decimal("0")),
            Conta(numero="200", saldo=Decimal("100")),
        ]
        repositorio = ContaRepositoryMemory(contas)
        servico = TransacaoService(repositorio)

        resultado = servico.transferir(_criar_transacao(1, "100", "200", "50"))

        assert resultado.sucesso is False
        assert resultado.status == StatusTransacao.CANCELADA_SALDO_INSUFICIENTE


class TestTransacaoServiceInjecaoDependencia:
    def test_aceita_qualquer_implementacao_de_repositorio(self):
        repositorio_mock = MagicMock()

        conta = Conta(numero="100", saldo=Decimal("500"))
        repositorio_mock.buscar_por_numero.return_value = conta
        repositorio_mock.atualizar.return_value = True

        servico = TransacaoService(repositorio_mock)
        resultado = servico.transferir(_criar_transacao(1, "100", "200", "50"))

        assert resultado.sucesso is True
        repositorio_mock.buscar_por_numero.assert_called()
        repositorio_mock.atualizar.assert_called()
