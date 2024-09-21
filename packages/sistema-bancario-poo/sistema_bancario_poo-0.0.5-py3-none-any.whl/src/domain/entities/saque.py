from src.domain.entities.transacao import Transacao
from src.domain.entities.conta import Conta
from datetime import datetime

class Saque(Transacao):
    def __init__(self, valor: float = 0):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor
    
    @valor.setter
    def valor(self, n: float):
        self._valor = n

    def registrar(self, conta: Conta):
        return f"Saldo: {conta.saldo} \n{self.__class__.__name__}: {self._valor} \nData: {datetime.now().strftime('%d/%m/%y %M:%H')}"



