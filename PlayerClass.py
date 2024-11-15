from random import randrange
from random import choice
from GameClass import alive, dead
from utils import Raridade, LOCAIS


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
        self.weapon = choice(("","Machado","Espada","Arco","Punhal"))
        self.maestria = 1 + randrange(10, 71) / 100
        self.bag = set()
        self.actions: dict[Raridade, set] = {
            Raridade.LENDARIO: {self.morteBosta},
            Raridade.EPICO: set(),
            Raridade.RARO: set(),
            Raridade.INCOMUM: set(),
            Raridade.COMUM: set(),
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

    def calc_AD(self) -> float:
        match self.weapon:
            case "Machado":
                return (0.6 * self.strength + 0.3 * self.stamina + 0.1 * self.qi) * self.maestria
            case "Espada":
                return (0.4 * self.strength + 0.4 * self.stamina + 0.1 * self.qi) * (
                    self.maestria + 0.2
                )
            case "Arco":
                return (0.3 * self.strength + 0.1 * self.stamina + 0.4 * self.qi) * (
                    self.maestria + 0.3
                )
            case "Punhal":
                return (0.3 * self.strength + 0.4 * self.stamina + 0.3 * self.qi) * (
                    self.maestria + 0.1
                )
            # Martelo Nunchuaku lança, outras armas
            case _:
                return 0.6 * self.strength + 0.4 * self.stamina

    def calc_DMG(self, AD: float, weapon: str, buff: bool) -> float:
        if not weapon:
            return AD
        if buff:
            return AD * (1 - self.armor / (100 + self.armor)) * 1.05
        return AD * (1 - self.armor / (100 + self.armor))

    def turn(self):
        self.hp = max(100, self.hp+4)
        # Escolher a raridade
        # Da raridade, escolher o conjunto de ações
        # Das ações, rodar alguma
        rarity = Raridade(randrange(1, 51))
        func = choice(list(self.actions[rarity]))
        # self.actions[Raridade.LENDARIO] = [self.turn]
        # self.game.dead.append(sla porra)
        func()

    # def move(self):
      # destino = choice(adj[self.local])
      # print(f"{self.name} foi de {self.local} para {destino}.")
      # for rarity in """Enum?"""
        # for func in functions[self.local][rarity]:
          # self.removeAction(func,rarity)
        # for func in functions[destino][rarity]:
          # self.addAction(func,rarity)
    
    def better_weapon(self, weapon : str):
      if self.weapon == None:
        self.weapon = choice(self.weapon,weapon)
      elif weapon != None:
        W1 = self.weapon
        old_AD = self.calc_AD()
        self.weapon = weapon
        if old_AD > self.calc_AD(): 
          self.weapon = W1

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

    # ===================== Métodos de ações padrão de turno ======================
    def morrer(self):
        self.hp = 0
        self.status = "Morto"
        alive.remove(self.name)
        dead.add(self.name)
        print(f"{self.name} morreu.")

    def comer(self, food="food"):
        if "cogumelo" in self.bag:
            print(f"{self.name} comeu um cogumelo e ficou brisadão.")
            self.brisa()
        elif food in self.bag:
            print(f"{self.name} comeu, descansou e recuperou 4 pnts de vida.")
            self.bag.remove(food)
        self.hp = min(100, self.hp + 4)

    def curar(self):
      if self.hp == 100:
        return None
      if "Atadura" in self.bag:
        self.hp = max(100,self.hp+15)
        print(f"{self.name} recuperou hp usando ataduras.")
        self.bag.remove("Atadura")
      if self.hp < 100 and "Bandagem" in self.bag:
        self.hp = max(100,self.hp + 25)
        print(f"{self.name} recuperou hp usando bandagens.")
        self.bag.remove("Bandagem")

    def saquear(self, morto : 'Player'):
      for item in morto.bag:
        if item not in self.bag:
          self.bag.add(item)
      self.better_weapon(morto.weapon)
      print(f"{self.name} saqueou o corpo de {morto}.")

    def lutar(self, player2: 'Player'):
        player1 = self
        print(f"{player1.name} e {player2.name} entraram em batalha!")
        player1_AD = player1.calc_AD()
        player2_AD = player2.calc_AD()
        DMG_in_P1 = player1.calc_DMG(player2_AD, player2.weapon, "Veneno" in player2.bag)
        DMG_in_P2 = player2.calc_DMG(player1_AD, player1.weapon, "Veneno" in player1.bag)
        Time_to_defeat_P1 = player1.hp / DMG_in_P1
        Time_to_defeat_P2 = player2.hp / DMG_in_P2
        if Time_to_defeat_P1 > Time_to_defeat_P2:
            winner = player1
            loser = player2
            DMG = DMG_in_P1
        else:
            winner = player2
            loser = player1
            DMG = DMG_in_P2
        print(f"{winner.name} saiu vitorioso.")
        loser.morrer()
        Time = min(Time_to_defeat_P1, Time_to_defeat_P2)
        winner.hp = max(1, winner.hp - Time * DMG)
        winner.saquear(loser)

    def morteBosta(self):
        # função nativa
        print(f"{self.name} pisou numa mina terrestre.")
        self.morrer()
          
    def assassinar(self, morto: 'Player'):
        print(f"{self.name} passou o ruim em {morto.name}.")
        morto.morrer()
        self.saquear(morto)

    def dormir(self):
        print(f"{self.name} dormiu tranquilamente como um neném.")
        print(f"{self.name} descansou e recuperou 4 pnts de vida.")
        self.hp = min(100, self.hp + 3)

    def olhar_ao_redor(self):
        for player in alive:
          if player != self and player.local == self.local:
            if player.now == "Em cima da árvore" and self.now != "Em cima da árvore":
              continue
            print(f"{self.name} encontrou {player.name}.")
            self.interagir(player)
        for player in dead:
          if player != self and player.local == self.local:
            print(f"{self.name} encontrou o corpo de {player.name}.")
            self.saquear(player)

    def interagir(self, player2: 'Player'):
      interação = choice(("Luta","Amizade"))
      match interação:
        case "Luta":
          self.lutar(player2)
        case "Amizade":
          print("Não implementado rsrs")

    def furtar(self, player2: 'Player'):
        item = choice(list(player2.bag))
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

    # ===================== Métodos de ações locais de turno ======================

    # Na Praia ou no Rio
    def afogamento(self):
        print(f"{self.name} se afogou.")
        self.local = "???"
        self.morrer()

    def pescar(self):
        peixes = ["pirarucu", "cará", "baiacu", "bota usada", "porra nenhuma"]
        item = choice(peixes)
        print(f"{self.name} pescou {item}")
        if item in ("pirarucu", "cará"):
            self.bag.add(item)
            if self.hp < 100:
                self.comer(item)
        elif item == "baiacu":
            print(f"{self.name} extraiu o veneno do baiacu e o guardou na bolsa.")
            self.bag.add("veneno")

    # Na montanha
    def find_cave(self): # Lendário
      print(f"self.name encontrou uma caverna.")
      self.local = "Caverna"

    # Na floresta
    def achar_gruta(self): # Épico
      print(f"self.name encontrou uma gruta.")
      self.local = "Gruta"
    def vespeiro(self):
      print(f"{self.name} derrubou um vespeiro! CORREEEEE!!!")
      self.hp-=15
      if self.hp<0:
        self.morrer()
      self.curar()

    # Na caverna e na gruta
    def find_chest(self): # Raro
      print(f"{self.name} encontrou um baú! O que será que há dentro dele?")
      lucky = randrange(1,11)
      match lucky:
        case 10:
          weapon = choice(("Machado","Espada","Arco","Punhal"))
          print(f"{self.name} encontrou um(a) {weapon}!")  
          self.bag.add("Veneno")
          self.better_weapon(weapon)
          return None
        case 9:
          print(f"{self.name} encontrou um kit de primeiros socorros!")       
          if self.hp<100:
            self.hp = 100
            print(f"{self.name} usou o kit recuperou seu hp por completo.")
          else:
            self.bag.add("Bandagem")
          return None
        case 8:
          print(f"{self.name} encontrou uma armadura resistente.")
          self.armor+=40
          return None
        case _:
          print("O baú estava vazio! :(")  
       



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
