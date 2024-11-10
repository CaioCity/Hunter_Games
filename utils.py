from enum import Enum


class Raridade(Enum):
    COMUM = range(1, 21)
    INCOMUM = range(21, 35)
    RARO = range(35, 45)
    EPICO = range(45, 50)
    LENDARIO = range(50, 51)

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if value in member.value:
                return member

        return None

    def __add__(self, level: int) -> 'Raridade':
        itens = list(Raridade)
        llen = len(Raridade)
        idx = min(llen - 1, itens.index(self) + level)
        return itens[idx]

    def __iadd__(self, level: int) -> 'Raridade':
        return self + level


LOCAIS = {
    "MONTANHA": {Raridade.EPICO: {lambda: "// achar caverna"}},
    "PRAIA": {
        Raridade.COMUM: {lambda: "se afogar", lambda: "comprar drogas"},
        Raridade.INCOMUM: {lambda: "pescar"},
    },
}
