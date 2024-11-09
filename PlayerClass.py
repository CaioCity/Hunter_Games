from random import randrange
from random import choice
from enum import Enum


class Raridade(Enum):
  LENDARIO = range(50, 50)
  EPICO = range(45, 50)
  RARO = range(35, 45)
  INCOMUM = range(21, 35)
  COMUM = range(1, 21)

  @classmethod
  def _missing_(cls, value):
    for member in cls:
      if value in member.value:
        return member

    return None



class Player:

  def __init__(self, name: str):
    # r = Raridade(20)
    # if r == Raridade.LENDARIO:
    #  pass
    self.name = name
    self.hp = 100
    self.status = f"Vivo ({self.hp}/100)"
    self.strength = randrange(40, 81)
    self.qi = randrange(40, 91)
    self.stamina = randrange(40, 101)
    self.local = "Base"
    self.friends = {}
    # setar sistema de compatibilidades

  def print_data(self):
    print("\nFicha Técnica:")
    print(f"Nome: {self.name}")
    print(f"Status: {self.status}")
    print(f"Localização: {self.local}")
    print(f"Força: {self.strength}")
    print(f"Inteligência: {self.qi}")
    print(f"Fôlego: {self.stamina}\n")

  def turn(self):
    rarity = Raridade(randrange(1,51))
    act = choice(self.local.actions_map.keys())
    self.local.actions_map[act]


