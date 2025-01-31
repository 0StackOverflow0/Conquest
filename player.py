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
