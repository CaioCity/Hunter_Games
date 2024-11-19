from random import randrange
from random import choice
from GameClass import alive, dead, Players
from utils import Rarity, LOCAIS


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
        self.location = "Início"
        self.friends = set()
        self.weapon = choice(("","Machado","Espada","Arco","Punhal"))
        self.mastery = 1 + randrange(10, 71) / 100
        self.bag = set()
        self.leader = name
        self.group_size = 1
        self.actions: dict[Rarity, set] = {
            Rarity.LEGENDARY: {self.random_death},
            Rarity.EPIC: set(),
            Rarity.RARE: set(),
            Rarity.UNCOMMON: set(),
            Rarity.COMMON: set(),
        }

        # setar sistema de compatibilidades

    def get_data(self):
        print("\nFicha Técnica:")
        print(f"Nome: {self.name}")
        print(f"Status: {self.status}")
        print(f"Localização: {self.location}")
        print(f"Força: {self.strength}")
        print(f"Inteligência: {self.qi}")
        print(f"Fôlego: {self.stamina}\n")

    def calc_AD(self) -> float:
        match self.weapon:
            case "Machado":
                return (0.5 * self.strength + 0.3 * self.stamina + 0.1 * self.qi) * self.mastery
            case "Espada":
                return (0.4 * self.strength + 0.4 * self.stamina + 0.1 * self.qi) * (
                    self.mastery + 0.2
                )
            case "Arco":
                return (0.3 * self.strength + 0.1 * self.stamina + 0.4 * self.qi) * (
                    self.mastery + 0.3
                )
            case "Punhal":
                return (0.3 * self.strength + 0.4 * self.stamina + 0.3 * self.qi) * (
                    self.mastery + 0.1
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
        rarity = Rarity(randrange(1, 51))
        func = choice(list(self.actions[rarity]))
        # self.actions[Raridade.LEGENDARY] = [self.turn]
        # self.game.dead.append(sla porra)
        func()

    # def move(self):
      # destino = choice(adj[self.location])
      # print(f"{self.name} foi de {self.location} para {destino}.")
      # for rarity in """Enum?""" # @Claudemir
        # for func in functions[self.location][rarity]:
          # self.removeAction(func,rarity)
        # for func in functions[destino][rarity]:
          # self.addAction(func,rarity)
    
    def better_weapon(self, morto : str):
      if self.weapon == None:
        self.weapon = choice(self.weapon,morto.weapon)
      elif morto.weapon != None:
        W1 = self.weapon
        old_AD = self.calc_AD()
        self.weapon = morto.weapon
        if old_AD > self.calc_AD(): 
          self.weapon = W1
        else: morto.weapon = W1

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
    def die(self):
        self.hp = 0
        self.status = "Morto"
        alive.remove(self.name)
        dead.add(self.name)
        print(f"{self.name} morreu.")

    def eat(self, food="food"):
        if "cogumelo" in self.bag:
            print(f"{self.name} comeu um cogumelo e ficou brisadão.")
            self.brisa()
        elif food in self.bag:
            print(f"{self.name} comeu, descansou e recuperou 4 pnts de vida.")
            self.bag.remove(food)
        self.hp = min(100, self.hp + 4)

    def heal(self):
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

    def loot(self, morto : 'Player'):
      for item in morto.bag:
        if item not in self.bag:
          self.bag.add(item)
          morto.bag.remove(item)
      self.better_weapon(morto)
      print(f"{self.name} saqueou o corpo de {morto}.")

    def fight(self, player2: 'Player'):
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

    def random_death(self):
        # função nativa
        print(f"{self.name} pisou numa mina terrestre.")
        self.morrer()
          
    def kill(self, morto: 'Player'):
        print(f"{self.name} passou o ruim em {morto.name}.")
        morto.morrer()
        self.saquear(morto)

    def sleep(self):
        print(f"{self.name} dormiu tranquilamente como um neném.")
        print(f"{self.name} descansou e recuperou 4 pnts de vida.")
        self.hp = min(100, self.hp + 3)

    def look_around(self):
        for player in alive:
          if player != self and player.local == self.location:
            if player.now == "Em cima da árvore" and self.now != "Em cima da árvore":
              continue
            print(f"{self.name} encontrou {player.name}.")
            self.interagir(player)
        for player in dead:
          if player != self and player.local == self.location:
            print(f"{self.name} encontrou o corpo de {player.name}.")
            self.saquear(player)

    def interact(self, player2: 'Player'):
      interação = choice(("Luta","Amizade"))
      match interação:
        case "Luta":
          self.lutar(player2)
        case "Amizade":
          self.join(player2)

    def steal(self, player2: 'Player'):
        item = choice(list(player2.bag))
        self.bag.add(item)
        player2.bag.remove(item)
        print(f"{self.name} furtou {item} de {player2.name}.")
        print(f"{self.name} riu de {player2.name}.")

    def drug(self):
        bonus = choice([5, -10])
        self.hp += bonus
        print(f"{self.name} {"ganhou" if bonus > 0 else "perdeu"} {bonus} pnts de vida")
        if self.hp <= 0:
            self.morrer()
        elif self.hp > 100:
            self.hp = 100

    # ===================== Métodos de ações locais de turno ======================

    # Na Praia ou no Rio
    def drown(self):
        print(f"{self.name} se afogou.")
        self.location = "???"
        self.morrer()

    def fishing(self):
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

    # Na montanha e na floresta
    def find_cave(self): # Lendário na montanha e épico na floresta
      print(f"self.name encontrou uma caverna.")
      self.location = "Caverna"

    def hornet(self):
      print(f"{self.name} derrubou um vespeiro! CORREEEEE!!!")
      self.hp-=15
      if self.hp<0:
        self.morrer()
      self.curar()

    # Na caverna e na gruta
    def find_chest(self): # RARE
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
      
    def get_leader(self):
      A = self
      while(A.leader != A.name):
        A = Players[A.leader]
      while self != A :
        self.leader, self = A, self.leader
  
    def join(self, player2 : 'Player'):
      self = self.get_leader() 
      player2 = player2.get_leader()

      if self.name == player2.name:
        return None

      if self.group_size > player2.group_size:
        self, player2 = player2, self
      
      if self.group_size == 1:
        if player2.group_size > 1:
          print(f"{self.name} se juntou ao grupo de {player2.name}.")
        else:
          print(f"{self.name} e {player2.name} formaram uma aliança.")
      else: print(f"Os grupos de {self.name} e {player2.name} se fundiram.")

      player2.leader = self.leader
      self.group_size += player2.group_size

      for friend in self.friends:
        player2.friends.add(friend)
      for friend in player2.friends:
        self.friends.add(friend)


        

       



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
