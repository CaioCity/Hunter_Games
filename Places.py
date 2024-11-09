"""
from abc import ABC, abstractmethod, abstractproperty
from ActionsClass import Actions
from random import choice
from GameClass import registro


class Place(Actions, ABC):
    def __init__(self):
        super().__init__()
        self.actions += [self.sair]


    @abstractmethod
    def sair(self,player):
        pass

    @abstractmethod
    @property
    def nome(self) -> str:
        pass






# vizinhança
# particularidades (adversidades e itens)

class Inicio(Place):

    def __init__(self):
        super().__init__()
        self.adj = []

    def nome(self) -> str:
        return "Início"

    def sair(self,player):
        destiny = choice(self.adj)
        registro.append(f"{player.name} foi de {player.local} para {destiny}.")
        player.local = destiny
"""