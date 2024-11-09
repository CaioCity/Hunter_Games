from random import randrange
from random import choice
from enum import Enum
from GameClass import alive

class Raridade(Enum):
  LENDARIO = range(50, 51)
  EPICO = range(45, 50)
  RARO = range(35, 45)
  INCOMUM = range(21, 35)
  COMUM = range(1, 21)

  @classmethod
  def _missing_(cls, value):
    for member in cls:
      if value in member.value:
        # vini gay viado baitola kkkkkkkkkkkkkkkkkkkkkkkkkk
        return member

    return None

LOCAIS = {
  "MONTANHA": {
    Raridade.RARO: {lambda: "// achar caverna"}
  },
  "PRAIA": {
    Raridade.COMUM: {lambda: "se afogar", lambda: "comprar drogas"},
    Raridade.INCOMUM: {lambda: "pescar"}
  }  
}


class Player:
  def __init__(self, name: str):
    super().__init__()

    self.name = name
    self.hp = 100
    self.status = f"Vivo ({self.hp}/100)"
    self.strength = randrange(40, 81)
    self.qi = randrange(40, 91)
    self.stamina = randrange(40, 101)
    self.local = "Início"
    self.friends = {}
    self.itens = set()
    self.actions: dict[Raridade, set] = {
      Raridade.LENDARIO: {self.morteBosta},
      Raridade.EPICO: set(),
      Raridade.RARO: set(),
      Raridade.INCOMUM: set(),
      Raridade.COMUM: set()
    }

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
    # Escolher a raridade
    # Da raridade, escolher o conjunto de ações
    # Das ações, rodar alguma
    rarity = Raridade(randrange(1,51))
    func = choice(list(self.actions[rarity]))
    # self.actions[Raridade.LENDARIO] = [self.turn]
    #self.game.dead.append(sla porra)
    func()

  # ========================== Actions Manager ===========================
  # gerado via print(f"# {' Actions Manager ':=^70}")
  def addAction(self, function, rarity):
    self.actions[rarity].add(function)

  def removeAction(self, function, rarity):
    self.actions[rarity].remove(function)

  """
  def irPraBucetaDoCaralhoDoDeserto:
    for raridade, func in listaDeAçõesDoDeserto:
      self.addAction(func, raridade)
  """

  # ===================== Métodos de ações de turno ======================
  def morrer(self):
    self.hp = 0
    self.status = "Morto"
    print(f"{self.name} morreu.")

  def morteBosta(self):
    # função nativa
    print(f"{self.name} pisou numa mina terrestre")
    self.morrer()

  def assassinar(self, morto: 'Player'):
    print(f"{self.name} passou o ruim em {morto.name}.")
    morto.morrer()

  def afogamento(self):
    print(f"{self.name} se afogou.")
    self.morrer()

  def pescar(self):
    peixes = ["pirarucu", "cará", "baiacu", "bota usada", "porra nenhuma"]
    item = choice(peixes)
    print(f"{self.name} pescou {item}")
    if item == "pirarucu" or item == "cará":
      print(f"{self.name} comeu um {item}.")
    if item == "baiacu":
      print(f"{self.name} extraiu o veneno do baiacu e o guardou na bolsa.")
      self.itens.add("veneno")

  def dormir(self):
    print(f"{self.name} dormiu tranquilamente como um neném.")

  def olhar_ao_redor(self):
    for player in alive:
      if player!=self and player.local == self.local:
        self.interagir(player)

  def interagir(self, player2: 'Player'):
    pass

  def furtar(self, player2: 'Player'):
    item = choice(player2.itens)
    self.itens.add(item)
    player2.itens.remove(item)
    print(f"{self.name} furtou {item} de {player2.name}.")
    print(f"{self.name} riu de {player2.name}.")

  def comer(self):
    if "cogumelo" in self.itens:
      print(f"{self.name} comeu um cogumelo e ficou brisadão.")
      self.brisa()
    elif "food" in self.itens:
      print(f"{self.name} comeu, descansou e recuperou 4 pnts de vida.")
      self.itens.remove("food")
    self.hp += 4
    if self.hp > 100:
      self.hp = 100

  def brisa(self):
    bonus = choice([5, -10])
    self.hp += bonus
    print(f"{self.name} {"ganhou" if bonus > 0 else "perdeu"} {bonus} pnts de vida")
    if self.hp <= 0:
      self.morrer()
    elif self.hp > 100:
      self.hp = 100











"""
  def f1
  def f2
  def f3
  
  def movePlace(self, new):
    self.removeOld(old)
    self.addNew(new)
  
  def removeOld(self, old):
      match old:
        case "Deserto":
        case "Floresta":
        case "Lago":
        case "Início":
        case "Praia":
        case "Montanha"
        

"""