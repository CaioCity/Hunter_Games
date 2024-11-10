from enum import Enum


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
    "MONTANHA": {Raridade.EPICO: {lambda: "// achar caverna"}},
    "PRAIA": {
        Raridade.COMUM: {lambda: "se afogar", lambda: "comprar drogas"},
        Raridade.INCOMUM: {lambda: "pescar"},
    },
}
