from src.domain.entities.transacao import Transacao
from src.domain.entities.pessoa_fisica import PessoaFisica
from datetime import datetime

class Cliente(PessoaFisica):
    def __init__(self, cpf: str, nome: str, data_nascimento: datetime, endereco: str, contas: list = None):
        super().__init__(cpf, nome, data_nascimento)
        self._endereco: endereco
        self._contas: contas

    @property
    def endereco(self) -> str:
        return self._endereco
    
    @endereco.setter
    def endereco(self, valor: str):
        self._endereco = valor

    @property
    def contas(self) -> list:
        return self._contas
    
    @contas.setter
    def contas(self, valor: list):
        self._contas = valor

    def realizar_transacao(self, conta, transacao: Transacao):
        match(transacao.__class__.__name__):
            case "Saque":
                conta.saldo -= transacao.valor
            case "Deposito":
                conta.saldo += transacao.valor

    def adicionar_conta(self, conta):
        self.contas.append(conta)
        return f"Conta adicionada: {';'.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"




if __name__ == "__main__":
    cliente = Cliente("1111", "jorge", datetime(day=20, month=4, year=1990), "rua jorge")
