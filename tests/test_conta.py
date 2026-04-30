from decimal import Decimal

import pytest

from models.conta import Conta
from models.transacao import Transacao
from models.resultado_transacao import ResultadoTransacao
from models.resultado_transacao import StatusTransacao


class TestContaCriacao:
    def test_criar_conta_com_valores_validos(self):
        conta = Conta(numero="123456", saldo=Decimal("1000"))
        assert conta.numero == "123456"
        assert conta.saldo == Decimal("1000")

    def test_criar_conta_com_saldo_zero(self):
        conta = Conta(numero="999", saldo=Decimal("0"))
        assert conta.saldo == Decimal("0")

    def test_criar_conta_com_saldo_padrao(self):
        conta = Conta(numero="999")
        assert conta.saldo == Decimal("0")

    def test_criar_conta_com_numero_grande(self):
        conta = Conta(numero="2147483649", saldo=Decimal("500"))
        assert conta.numero == "2147483649"

    def test_criar_conta_com_saldo_decimal(self):
        conta = Conta(numero="100", saldo=Decimal("1234.56"))
        assert conta.saldo == Decimal("1234.56")


class TestContaOperacoes:
    def test_debitar_valor(self):
        conta = Conta(numero="123", saldo=Decimal("500"))
        conta.debitar(Decimal("150"))
        assert conta.saldo == Decimal("350")

    def test_creditar_valor(self):
        conta = Conta(numero="123", saldo=Decimal("500"))
        conta.creditar(Decimal("250"))
        assert conta.saldo == Decimal("750")

    def test_debitar_saldo_total(self):
        conta = Conta(numero="123", saldo=Decimal("200"))
        conta.debitar(Decimal("200"))
        assert conta.saldo == Decimal("0")

    def test_possui_saldo_suficiente_verdadeiro(self):
        conta = Conta(numero="123", saldo=Decimal("500"))
        assert conta.possui_saldo_suficiente(Decimal("300")) is True

    def test_possui_saldo_suficiente_valor_exato(self):
        conta = Conta(numero="123", saldo=Decimal("500"))
        assert conta.possui_saldo_suficiente(Decimal("500")) is True

    def test_possui_saldo_insuficiente(self):
        conta = Conta(numero="123", saldo=Decimal("100"))
        assert conta.possui_saldo_suficiente(Decimal("500")) is False

    def test_possui_saldo_insuficiente_saldo_zero(self):
        conta = Conta(numero="123", saldo=Decimal("0"))
        assert conta.possui_saldo_suficiente(Decimal("1")) is False


class TestContaRepresentacao:
    def test_igualdade_contas_iguais(self):
        conta_a = Conta(numero="123", saldo=Decimal("100"))
        conta_b = Conta(numero="123", saldo=Decimal("100"))
        assert conta_a == conta_b

    def test_igualdade_contas_diferentes(self):
        conta_a = Conta(numero="123", saldo=Decimal("100"))
        conta_b = Conta(numero="456", saldo=Decimal("100"))
        assert conta_a != conta_b


class TestTransacaoCriacao:
    def test_criar_transacao_valida(self):
        transacao = Transacao(
            correlation_id=1,
            data_hora="09/09/2023 14:15:00",
            conta_origem="938485762",
            conta_destino="2147483649",
            valor=Decimal("150"),
        )
        assert transacao.correlation_id == 1
        assert transacao.data_hora == "09/09/2023 14:15:00"
        assert transacao.conta_origem == "938485762"
        assert transacao.conta_destino == "2147483649"
        assert transacao.valor == Decimal("150")

    def test_transacao_imutavel(self):
        transacao = Transacao(
            correlation_id=1,
            data_hora="09/09/2023 14:15:00",
            conta_origem="100",
            conta_destino="200",
            valor=Decimal("50"),
        )

        with pytest.raises(AttributeError):
            setattr(transacao, "valor", Decimal("999"))

    def test_transacoes_iguais(self):
        transacao_a = Transacao(
            correlation_id=1,
            data_hora="09/09/2023 14:15:00",
            conta_origem="100",
            conta_destino="200",
            valor=Decimal("50"),
        )
        transacao_b = Transacao(
            correlation_id=1,
            data_hora="09/09/2023 14:15:00",
            conta_origem="100",
            conta_destino="200",
            valor=Decimal("50"),
        )
        assert transacao_a == transacao_b


class TestResultadoTransacao:
    def test_resultado_efetivada(self):
        resultado = ResultadoTransacao(
            correlation_id=1,
            status=StatusTransacao.EFETIVADA,
            mensagem="Transacao efetivada",
        )
        assert resultado.sucesso is True
        assert resultado.correlation_id == 1

    def test_resultado_cancelada_saldo(self):
        resultado = ResultadoTransacao(
            correlation_id=2,
            status=StatusTransacao.CANCELADA_SALDO_INSUFICIENTE,
            mensagem="Saldo insuficiente",
        )
        assert resultado.sucesso is False

    def test_resultado_cancelada_conta_nao_encontrada(self):
        resultado = ResultadoTransacao(
            correlation_id=3,
            status=StatusTransacao.CANCELADA_CONTA_ORIGEM_NAO_ENCONTRADA,
            mensagem="Conta nao encontrada",
        )
        assert resultado.sucesso is False

    def test_resultado_cancelada_conta_destino_nao_encontrada(self):
        resultado = ResultadoTransacao(
            correlation_id=4,
            status=StatusTransacao.CANCELADA_CONTA_DESTINO_NAO_ENCONTRADA,
            mensagem="Conta destino nao encontrada",
        )
        assert resultado.sucesso is False

    def test_resultado_imutavel(self):
        resultado = ResultadoTransacao(
            correlation_id=1,
            status=StatusTransacao.EFETIVADA,
            mensagem="OK",
        )

        with pytest.raises(AttributeError):
            setattr(
                resultado,
                "status",
                StatusTransacao.CANCELADA_SALDO_INSUFICIENTE,
            )

    def test_status_transacao_valores(self):
        assert StatusTransacao.EFETIVADA.value == "efetivada"
        assert StatusTransacao.CANCELADA_SALDO_INSUFICIENTE.value == "cancelada_saldo_insuficiente"
        assert StatusTransacao.CANCELADA_CONTA_ORIGEM_NAO_ENCONTRADA.value == "cancelada_conta_origem_nao_encontrada"
        assert StatusTransacao.CANCELADA_CONTA_DESTINO_NAO_ENCONTRADA.value == "cancelada_conta_destino_nao_encontrada"