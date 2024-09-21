from src.domain.entities.transacao import Transacao


class Historico:
    def __init__(self):
        self._lista_transacao = []

    @property
    def lista_transacao(self) -> list:
        return self._lista_transacao

    def adicionar_transacao(self, transacao: Transacao, conta):
        self._lista_transacao.append(transacao.registrar(conta))


