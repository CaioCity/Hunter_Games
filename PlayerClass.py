from random import randrange
from random import choice
from enum import Enum
from GameClass import alive,dead

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
        return member

    return None

LOCAIS = {
  "MONTANHA": {
    Raridade.EPICO: {lambda: "// achar caverna"}
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
    self.now = "Em preparação."
    self.armor = 30
    self.strength = randrange(40, 100)
    self.qi = randrange(40, 91)
    self.stamina = randrange(40, 91)
    self.local = "Início"
    self.friends = {}
    self.weapon = ""
    self.maestria = 1 + randrange(10,71)/100
    self.AD = 0,6*self.strength + 0,4*self.stamina 
    self.bag = set()
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

  def calc_AD(self):
    match self.weapon:
      case "":
        self.AD = 0,6*self.strength + 0,4*self.stamina
      case "Machado":
        self.AD = (0,6*self.strength + 0,3*self.stamina + 0.1*self.qi)*self.maestria
      case "Espada":
        self.AD = (0,4*self.strength + 0,4*self.stamina + 0.1*self.qi)*(self.maestria+0.2)
      case "Arco":
        self.AD = (0,3*self.strength + 0,1*self.stamina + 0.4*self.qi)*(self.maestria+0.3)
      case "Punhal":
        self.AD = (0,3*self.strength + 0,4*self.stamina + 0.3*self.qi)*(self.maestria+0.1)
      # Martelo Nunchuaku lança

  def calc_DMG(self,AD : int, weapon : str, buff : bool):
    if weapon == "":
      return AD
    if buff:
      return (AD * (1 - self.armor/(100+self.armor)) * 1.05)
    return (AD * (1 - self.armor/(100+self.armor)))
    
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
    alive.remove(self.name)
    dead.add(self.name)
    print(f"{self.name} morreu.")

  def comer(self, food = "food"):
    if "cogumelo" in self.bag:
      print(f"{self.name} comeu um cogumelo e ficou brisadão.")
      self.brisa()
    elif food in self.bag:
      print(f"{self.name} comeu, descansou e recuperou 4 pnts de vida.")
      self.bag.remove(food)
    self.hp += 4
    if self.hp > 100:
      self.hp = 100

  def saquear(self,bag):
    pass
    # codar saques (food, arma, veneno,etc)

  def lutar(player1, player2 : 'Player'):
    print(f"{player1.nome} e {player2.nome} entraram em batalha!")
    player1.calc_AD()
    player2.calc_AD()
    DMG_in_P1 = player1.calc_DMG(player2.AD, player2.weapon, "Veneno" in player2.bag)
    DMG_in_P2 = player2.calc_DMG(player1.AD, player1.weapon, "Veneno" in player1.bag)
    Time_to_defeat_P1 = player1.hp/DMG_in_P1
    Time_to_defeat_P2 = player2.hp/DMG_in_P2
    if Time_to_defeat_P1>Time_to_defeat_P2:
      winner = player1
      loser = player2
      DMG = DMG_in_P1
    else:
      winner = player2
      loser = player1
      DMG = DMG_in_P2
    print(f"{winner.nome} saiu vitorioso.")
    loser.morrer()
    Time = min(Time_to_defeat_P1,Time_to_defeat_P2)
    winner.hp = max(1,winner.hp - Time*DMG)
    winner.saquear(loser.bag)

  def morteBosta(self):
    # função nativa
    print(f"{self.name} pisou numa mina terrestre.")
    self.morrer()

  def armadilha(self):
    # função nativa
    print(f"{self.name} caiu numa armadilha.")
    self.morrer()

  def abrir_caixa(self):
    pass

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
      self.bag.add(item)
      if self.hp<100:
        self.comer(item)
    elif item == "baiacu":
      print(f"{self.name} extraiu o veneno do baiacu e o guardou na bolsa.")
      self.bag.add("veneno")

  def dormir(self):
    print(f"{self.name} dormiu tranquilamente como um neném.")
    self.hp+=3
    print(f"{self.name} descansou e recuperou 4 pnts de vida.")
    if self.hp > 100:
      self.hp = 100

  def olhar_ao_redor(self):
    for player in alive:
      if player!=self and player.local == self.local:
        self.interagir(player)

  def interagir(self, player2: 'Player'):
    pass

  def furtar(self, player2: 'Player'):
    item = choice(player2.bag)
    self.bag.add(item)
    player2.bag.remove(item)
    print(f"{self.name} furtou {item} de {player2.name}.")
    print(f"{self.name} riu de {player2.name}.")

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
