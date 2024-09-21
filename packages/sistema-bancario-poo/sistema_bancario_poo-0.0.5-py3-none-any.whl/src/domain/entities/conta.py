from src.domain.entities.cliente import Cliente
from src.domain.entities.historico import Historico

class Conta:
    def __init__(self, saldo: float = 0, numero: int = 0, agencia: str = None, cliente: Cliente = None):
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int):
        return cls(cliente=cliente, numero=numero)

    @property
    def historico(self) -> Historico:
        return self._historico
    @property
    def saldo(self) -> float:
        return self._saldo

    @saldo.setter
    def saldo(self, valor: float):
        self._saldo = valor

    @property
    def numero(self) -> int:
        return self._numero

    @numero.setter
    def numero(self, valor: int):
        self._numero = valor

    @property
    def agencia(self) -> str:
        return self._agencia

    @agencia.setter
    def agencia(self, valor: str):
        self._agencia = valor

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @cliente.setter
    def cliente(self, novo: Cliente):
        self._cliente = novo

    def get_saldo(self):
        return self._saldo

    def sacar(self, valor: float) -> bool:
        if 0 < valor < self._saldo:
            self._saldo -= valor
            return True
        else:
            return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            return True
        else:
            return False


