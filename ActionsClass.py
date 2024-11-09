class Actions:
    def __init__(self):
        self.actions_map = {}

    def take_action(self):
        print(f"{'Ações':^=70}")
        indexes = list(self.actions_map)
        for idx, name in enumerate(indexes, start = 1):
            print(f"{idx}) {name}")

        while True:
            try:
                # tentar pegar o input do corno, int
                # e acessar no indexes[i - 1]
                pass
            except:
                pass