alive = set()
dead = set()
Players: dict[str, 'Player'] = {}

from PlayerClass import Player

class Game:
    def __init__(self):
        self.day = 1

    def add_player(self, name: str):
        if name not in Players:
            Players[name] = Player(name)
            print(f"{name} foi adicionado(a) ao jogo.")
            Players[name].get_data()
            alive.add(name)
        else:
            print(f"{name} já está no jogo!")

    def listar_players(self):
        for i in Players:
            print(f"{i} está {Players[i].status}")

    def listar_vivos(self):
        for i in alive:
            print(f"{i} está vivo(a).")

    def listar_mortos(self):
        for i in dead:
            print(f"{i} está morto(a).")

    #### In Game

    def run_turn(self):
        for name in alive:
            player = Players[name]
            player.turn()
        print("Resumo da rodada:\n")
