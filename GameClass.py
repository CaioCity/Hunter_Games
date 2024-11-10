alive = set()
dead = set()


class Game:
    def __init__(self):
        self.players: dict[str, Player] = {}
        self.day = 1

    def add_player(self, name: str):
        if name not in self.players:
            self.players[name] = Player(name)
            print(f"{name} foi adicionado(a) ao jogo.")
            self.players[name].print_data()
            alive.add(name)
        else:
            print(f"{name} já está no jogo!")

    def listar_players(self):
        for i in self.players:
            print(f"{i} está {self.players[i].status}")

    def listar_vivos(self):
        for i in alive:
            print(f"{i} está vivo(a).")

    def listar_mortos(self):
        for i in dead:
            print(f"{i} está morto(a).")

    #### In Game

    def run_turn(self):
        for name in alive:
            player = self.players[name]
            player.turn()
        print("Resumo da rodada:\n")


from PlayerClass import Player
