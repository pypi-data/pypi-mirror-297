from datetime import datetime
from src.domain.entities.cliente import Cliente
from src.domain.entities.conta import Conta
from src.domain.entities.deposito import Deposito
from src.domain.entities.saque import Saque


class RepositoryBankManegement:
    @classmethod
    def validar_cpf(cls, lista_clientes: list, cpf: str):
        for cliente in lista_clientes:
            if cliente.cpf == cpf or cpf == "":
                return False
        else:
            return True

    @classmethod
    def criar_cliente(cls, lista_clientes):
        cpf = input("Insira o cpf do cliente: \n").lower().strip()
        validacao = cls.validar_cpf(lista_clientes, cpf)
        if validacao:
            nome = input("Insira o nome do cliente: \n").lower().strip()
            dia_nascimento = int(input("Insira o dia de nascimento do cliente: \n"))
            mes_nascimento = int(input("Insira o mes de nascimento do cliente: \n"))
            ano_nascimento = int(input("Insira o ano de nascimento do cliente: \n"))
            data_nascimento = datetime(day=dia_nascimento, month=mes_nascimento, year=ano_nascimento)
            endereco = input("Insira o endereço do cliente: \n").lower().strip()
            novo_cliente = Cliente(cpf, nome, data_nascimento, endereco)
            return novo_cliente
        else:
            if cpf == "":  # não coloquei validação por tamanho e formato de cpf
                return "Coloque um cpf válido!!\n"
            else:
                return "Já existem clientes cadastrados com o cpf inserido!!"

    @classmethod
    def exibir_clientes(cls, lista_clientes: list):
        for cliente in lista_clientes:
            print(f"Nome:{cliente.nome} cpf: {cliente.cpf}\n")

    @classmethod
    def get_cliente(cls, lista_clientes: list, cpf: str):
        for cliente in lista_clientes:
            if cliente.cpf == cpf:
                return cliente
        return "Não existe clientes cadastrados com o cpf informado!\n"

    @classmethod
    def get_conta(cls, lista_contas: list, numero: int):
        for conta in lista_contas:
            if conta.numero == numero:
                return conta
        return "Não existe contas com o número informado!\n"

    @classmethod
    def nova_conta(cls, cliente, numero_conta: int):
        nova_conta = Conta.nova_conta(cliente, numero_conta)
        return nova_conta

    @classmethod
    def get_all_contas(cls, lista_contas: list):
        for conta in lista_contas:
            print(f"Titular: {conta.cliente.nome} Numero: {conta.numero}\n"
                  f"------------------------------------------------------")

    @classmethod
    def deposito(cls, conta, valor):
        deposito = conta.depositar(valor)
        if deposito:
            deposito_conta = Deposito(valor)
            conta.historico.adicionar_transacao(deposito_conta, conta)
            return f"Deposito de: {deposito_conta.valor} feito com sucesso!\n"
        else:
            return "Erro! Valor igual ou menor a zero\n"

    @classmethod
    def saque(cls, conta, valor):
        saque = conta.sacar(valor)
        if saque:
            saque_conta = Saque(valor)
            conta.historico.adicionar_transacao(saque_conta, conta)
            return f"Saque de: {saque_conta.valor} feito com sucesso!\n"
        else:
            return "Erro! Não tem saldo o suficiente para realizar este saque!\n"

    @classmethod
    def extrato(cls, conta):
        record = conta.historico.lista_transacao
        for historico in record:
            print(f"--------------------------------------------\n"
                  f"{conta.cliente.nome} {historico}\n")






