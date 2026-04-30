from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

from models.conta import Conta
from models.transacao import Transacao
from repositories.repository_memory import ContaRepositoryMemory
from services.transacao_service import TransacaoService


def criar_contas_iniciais():
    return [
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


def criar_transacoes():
    return [
        Transacao(correlation_id=1, data_hora="09/09/2023 14:15:00", conta_origem="938485762", conta_destino="2147483649", valor=Decimal("150")),
        Transacao(correlation_id=2, data_hora="09/09/2023 14:15:05", conta_origem="2147483649", conta_destino="210385733", valor=Decimal("149")),
        Transacao(correlation_id=3, data_hora="09/09/2023 14:15:29", conta_origem="347586970", conta_destino="238596054", valor=Decimal("1100")),
        Transacao(correlation_id=4, data_hora="09/09/2023 14:17:00", conta_origem="675869708", conta_destino="210385733", valor=Decimal("5300")),
        Transacao(correlation_id=5, data_hora="09/09/2023 14:18:00", conta_origem="238596054", conta_destino="674038564", valor=Decimal("1489")),
        Transacao(correlation_id=6, data_hora="09/09/2023 14:18:20", conta_origem="573659065", conta_destino="563856300", valor=Decimal("49")),
        Transacao(correlation_id=7, data_hora="09/09/2023 14:19:00", conta_origem="938485762", conta_destino="2147483649", valor=Decimal("44")),
        Transacao(correlation_id=8, data_hora="09/09/2023 14:19:01", conta_origem="573659065", conta_destino="675869708", valor=Decimal("150")),
    ]


def main():
    contas_iniciais = criar_contas_iniciais()
    repositorio = ContaRepositoryMemory(contas_iniciais)
    servico = TransacaoService(repositorio)
    transacoes = criar_transacoes()

    with ThreadPoolExecutor() as executor:
        for transacao in transacoes:
            executor.submit(servico.transferir, transacao)


if __name__ == "__main__":
    main()
