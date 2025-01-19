from territories import *

class Player:
    name: str
    id: str
    ready: bool = False
    armies: int
    cards: list # FUTURE
    conquered: int
    territories: list[Territory]

    def __init__(self, name, armies=0, id=""):
        self.name = name
        self.armies = armies
        self.territories = []

PLAYERS: list[Player] = [
    Player(name="Neutral", armies=4)
]

PLAYABLE: dict[str, Player] = {
}

def isPlayer(id: str) -> bool:
    return id in PLAYABLE.keys()

def getDefenders(id: str) -> list[Territory]:
    return PLAYERS[0].territories + (PLAYERS[1].territories if PLAYABLE[id] == PLAYERS[2] else PLAYERS[2].territories)

def getAttackers(id: str) -> list[Territory]:
    return (PLAYERS[1].territories if PLAYABLE[id] == PLAYERS[1] else PLAYERS[2].territories)
