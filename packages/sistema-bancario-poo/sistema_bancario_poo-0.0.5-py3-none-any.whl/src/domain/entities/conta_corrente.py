from src.domain.entities.conta import Conta
from src.domain.entities.cliente import Cliente
from src.domain.entities.historico import Historico

class ContaCorrente(Conta):
    def __init__(self, limite: float, limite_saques: int, saldo: float, numero: int, agencia: str,
                 cliente: Cliente, historico: Historico):
        super().__init__(saldo, numero, agencia, cliente, historico)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self) -> float:
        return self._limite

    @property
    def limite_saques(self) -> int:
        return self._limite_saques

    @limite.setter
    def limite(self, valor: float):
        self._limite = valor

    @limite_saques.setter
    def limite_saques(self, valor: int):
        self._limite_saques = valor
