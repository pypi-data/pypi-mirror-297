from datetime import datetime
class PessoaFisica:
    def __init__(self, cpf: str, nome: str, data_nascimento: datetime):
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento.strftime("%d/%m/%y")

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, valor: str):
        self._cpf = valor

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str):
        self._nome = valor

    @property
    def data_nascimento(self) -> str:
        return self._data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, valor: str):
        self._data_nascimento = valor
