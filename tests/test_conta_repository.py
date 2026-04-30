from decimal import Decimal

from models.conta import Conta
from repositories.repository_memory import ContaRepositoryMemory
from repositories.repository_interface import ContaRepositoryInterface


class TestContaRepositoryMemoryCriacao:
    def test_criar_repositorio_com_contas_iniciais(self):
        contas = [
            Conta(numero="100", saldo=Decimal("500")),
            Conta(numero="200", saldo=Decimal("1000")),
        ]
        repositorio = ContaRepositoryMemory(contas)
        assert repositorio.buscar_por_numero("100") is not None
        assert repositorio.buscar_por_numero("200") is not None

    def test_criar_repositorio_vazio(self):
        repositorio = ContaRepositoryMemory([])
        assert repositorio.buscar_por_numero("100") is None

    def test_repositorio_implementa_interface(self):
        repositorio = ContaRepositoryMemory([])
        assert isinstance(repositorio, ContaRepositoryInterface)


class TestContaRepositoryMemoryBuscar:
    def test_buscar_conta_existente(self):
        contas = [Conta(numero="100", saldo=Decimal("500"))]
        repositorio = ContaRepositoryMemory(contas)
        resultado = repositorio.buscar_por_numero("100")
        assert resultado is not None
        assert resultado.numero == "100"
        assert resultado.saldo == Decimal("500")

    def test_buscar_conta_inexistente(self):
        contas = [Conta(numero="100", saldo=Decimal("500"))]
        repositorio = ContaRepositoryMemory(contas)
        resultado = repositorio.buscar_por_numero("999")
        assert resultado is None

    def test_buscar_conta_com_numero_grande(self):
        contas = [Conta(numero="2147483649", saldo=Decimal("0"))]
        repositorio = ContaRepositoryMemory(contas)
        resultado = repositorio.buscar_por_numero("2147483649")
        assert resultado is not None
        assert resultado.saldo == Decimal("0")

    def test_buscar_retorna_referencia_ao_objeto(self):
        contas = [Conta(numero="100", saldo=Decimal("500"))]
        repositorio = ContaRepositoryMemory(contas)
        resultado = repositorio.buscar_por_numero("100")
        resultado.saldo = Decimal("999")
        resultado_atualizado = repositorio.buscar_por_numero("100")
        assert resultado_atualizado.saldo == Decimal("999")


class TestContaRepositoryMemoryAtualizar:
    def test_atualizar_conta_existente(self):
        contas = [Conta(numero="100", saldo=Decimal("500"))]
        repositorio = ContaRepositoryMemory(contas)
        conta_atualizada = Conta(numero="100", saldo=Decimal("300"))
        resultado = repositorio.atualizar(conta_atualizada)
        assert resultado is True
        assert repositorio.buscar_por_numero("100").saldo == Decimal("300")

    def test_atualizar_conta_nova(self):
        repositorio = ContaRepositoryMemory([])
        nova_conta = Conta(numero="999", saldo=Decimal("100"))
        resultado = repositorio.atualizar(nova_conta)
        assert resultado is True
        assert repositorio.buscar_por_numero("999").saldo == Decimal("100")

    def test_atualizar_preserva_outras_contas(self):
        contas = [
            Conta(numero="100", saldo=Decimal("500")),
            Conta(numero="200", saldo=Decimal("1000")),
        ]
        repositorio = ContaRepositoryMemory(contas)
        conta_atualizada = Conta(numero="100", saldo=Decimal("300"))
        repositorio.atualizar(conta_atualizada)
        assert repositorio.buscar_por_numero("200").saldo == Decimal("1000")


class TestContaRepositoryMemoryListar:
    def test_listar_todas_as_contas(self):
        contas = [
            Conta(numero="100", saldo=Decimal("500")),
            Conta(numero="200", saldo=Decimal("1000")),
        ]
        repositorio = ContaRepositoryMemory(contas)
        todas = repositorio.listar_todas()
        assert len(todas) == 2

    def test_listar_repositorio_vazio(self):
        repositorio = ContaRepositoryMemory([])
        todas = repositorio.listar_todas()
        assert len(todas) == 0