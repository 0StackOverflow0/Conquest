from territories import *
from continents import *
from player import *
from copy import deepcopy
from uuid import uuid4

class GameState:
    turn: bool = True # True is Player 1, False is Player 2
    neutral: bool = False # True when setting up Neutral armies
    phase: int = -1 # [ -1, 0, 1, 2, 3, 4 ]
    territories: list[Territory] = []
    players: list[Player] = [
        Player(name="Neutral", armies=26)
    ]
    playable: dict[str, Player] = {}
    '''
        Phase -1 is 'Waiting to Start'
        Phase 0  is 'Board Setup'
        Phase 1  is 'Placement'
        Phase 2  is 'Combat/Transfer'
        Phase 3  is 'End of Turn'
    '''

    def __init__(self) -> None:
        self.territories = deepcopy(TERRITORIES)

    def register(self, name: str) -> str:
        uuid = str(uuid4())

        if len(self.players) < 3 and len(name) and len(name) <= len("Player 1"):
            self.players.append(Player(name, id=uuid))
            self.playable[uuid] = self.players[-1]
        else:
            uuid = ""

        return uuid
    
    def start(self, id: str) -> bool:
        if self.isPlayer(id):
            self.playable[id].ready = True
            return True
        return False

    def board(self, id: str) -> dict:
        return {
            "play" : 1 if self.turn else 2,
            "phase" : self.status(),
            "place" : self.playable[id].armies,
            "neutral" : self.neutral,
            "players" : [ player.name for player in self.players ],
            "board" : {
                name : { "player" : territory.player, "armies" : territory.armies }
                for name, territory in self.territories.items()
            }
        }

    def isSetup(self) -> bool:
        return self.phase == 0
    
    def isPlayer(self, id: str) -> bool:
        return id in self.playable.keys()
    
    def isYourTurn(self, id: str) -> bool:
        return (self.turn and self.playable[id] == self.players[1]) or (not self.turn and self.playable[id] == self.players[2])
    
    def getDefenders(self, id: str) -> list[Territory]:
        return self.players[0].territories + \
            (self.players[1].territories \
             if self.playable[id] == self.players[2] \
                else self.players[2].territories)

    def getAttackers(self, id: str) -> list[Territory]:
        return (self.players[1].territories \
                if self.playable[id] == self.players[1] \
                    else self.players[2].territories)

    
    def isPlacement(self) -> bool:
        return self.phase == 1
    
    def isCombat(self) -> bool:
        return self.phase == 2
    
    def isEndOfTurn(self) -> bool:
        return self.phase == 3

    def isEndofGame(self) -> bool:
        player = 1 if self.turn else 2
        return self.phase == 4 or \
            all(t.player == player for t in self.territories.values())

    def isStarted(self) -> bool:
        return self.phase >= 0
    
    def isPlaying(self) -> bool:
        return self.phase > 0 and self.phase < 4

    def isReady(self) -> bool:
        both_ready = len(self.players) == 3 and self.players[1].ready and self.players[2].ready
        if both_ready and not self.isStarted():
            self.shuffle()
            self.startSetup()
            self.player().armies = 2

        return both_ready

    def status(self) -> str:
        if self.isSetup():
            return "Setup"
        elif self.isPlacement():
            return "Place"
        elif self.isCombat():
            return "Combat"
        elif self.isEndofGame():
            return f"Winner is {self.player().name}"
        else:
            return "Wait to Start"

    def startSetup(self) -> None:
        self.phase = 0

    def startPlacement(self) -> None:
        self.income()
        self.phase = 1

    def startCombat(self) -> None:
        self.phase = 2

    def startEndOfTurn(self) -> None:
        self.phase = 3

    def startEndOfGame(self) -> None:
        self.phase = 4

    def shuffle(self) -> None:
        territories = list(self.territories.values())
        import random
        random.shuffle(territories)
        self.players[0].territories = territories[:14]
        self.players[1].territories = territories[14:28]
        self.players[2].territories = territories[28:]

        for territory in self.players[1].territories:
            territory.player = 1
        for territory in self.players[2].territories:
            territory.player = 2

        self.turn = (random.randint(1,10) % 2) == 0

    def player(self) -> Player:
        return self.players[1 if self.turn else 2]

    def income(self) -> None:
        '''
        Give player new armies based on income
        '''
        income = int(len(self.player().territories) / 3)
        income = 3 if income < 3 else income

        for continent in CONTINENTS.values():
            if all(territory in self.player().territories for territory in continent.territories):
                income += continent.score
        
        self.player().armies = income

    def place(self, territory: str, armies: str) -> None:
        if self.neutral:
            self.territories[territory].armies += 1
            self.players[0].armies -= 1
        else:
            self.territories[territory].armies += armies
            self.player().armies -= armies
        
        if self.player().armies == 0:
            if self.isSetup():
                self.determineState()
            else:
                self.startCombat()

    def combat(self, attacker: str, defender: str, armies: int) -> bool:
        '''
        Does not itself progress game state
        Will exhaust all committed armies to invade
        '''
        self.territories[attacker].armies -= armies
        offence = armies
        defence = self.territories[defender].armies

        lost = False
        conq = False if defence else True

        while not lost and not conq:
            off_dice = 3 if offence > 2 else 2 if offence > 1 else 1
            def_dice = 2 if defence > 1 else 1

            import random
            off_rolls = sorted( random.randint(1, 6) for _ in range(off_dice) )
            def_rolls = sorted( random.randint(1, 6) for _ in range(def_dice) )
            
            pair = def_dice if def_dice < off_dice else off_dice

            win = sum([1 if off_rolls[-1 - i] > def_rolls[-1 - i] else 0 for i in range(pair)])
            lose = pair - win

            offence -= lose
            defence -= win

            if offence == 0:
                lost = True
            elif defence == 0:
                conq = True

        if conq:
            self.players[self.territories[defender].player].territories.remove(self.territories[defender])
            self.territories[defender].player = 1 if self.turn else 2
            self.territories[defender].armies = offence
            self.player().territories += [ self.territories[defender] ]

            if self.isEndofGame():
                self.startEndOfGame()

            return True

    def transfer(self, origin: str, dest: str, armies: int) -> None:
        '''
        Will end Combat phase and start End of Turn
        To End Turn without Transfering Armies
        One must submit a transfer with null transfer
        origin and dest as the same territory
        '''
        self.territories[origin].armies -= armies
        self.territories[dest].armies += armies
        self.startEndOfTurn()
        self.determineState()
    
    def determineState(self) -> None:
        '''
        Valid action has taken place
        Adjust phase, turn, and neutral as needed
        '''
        if self.isSetup():
            if self.neutral:
                self.neutral = False
                self.turn = not self.turn
                self.player().armies = 2
                if self.players[0].armies == 0:
                    self.startPlacement()
            else:
                self.neutral = True

        if self.isPlaying():
            if self.isEndOfTurn():
                self.turn = not self.turn
                self.startPlacement()

    def validPlacement(self, id: str, territory: str, armies: int) -> bool:
        if (self.neutral or (self.playable[id].armies >= armies and armies > 0)):
            territories = self.players[0].territories if self.neutral else self.playable[id].territories
            return self.territories[territory] in territories
        return False
    
    def validCombat(self, id: str, attacker: str, defender: str, armies: int) -> bool:
        if self.territories[attacker] in self.getAttackers(id) and self.territories[defender] in self.getDefenders(id) and armies > 0:
            if self.territories[defender] in self.territories[attacker].neighbors:
                return self.territories[attacker].armies > armies
        return False

    def validTransfer(self, id: str, origin: str, dest: str, armies: int) -> bool:
        if self.territories[origin] in self.getAttackers(id) and self.territories[dest] in self.getAttackers(id) and armies >= 0:
            return self.territories[origin].armies > armies
        return False

game = GameState()
