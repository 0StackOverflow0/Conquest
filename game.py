from territories import *
from continents import *
from player import *

class GameState:
    turn: bool = True # True is Player 1, False is Player 2
    neutral: bool = False # True when setting up Neutral armies
    phase: int = -1 # [ -1, 0, 1, 2, 3, 4 ]
    '''
        Phase -1 is 'Waiting to Start'
        Phase 0  is 'Board Setup'
        Phase 1  is 'Placement'
        Phase 2  is 'Combat/Transfer'
        Phase 3  is 'End of Turn'
    '''

    def isSetup(self) -> bool:
        return self.phase == 0
    
    def isPlacement(self) -> bool:
        return self.phase == 1
    
    def isCombat(self) -> bool:
        return self.phase == 2
    
    def isEndOfTurn(self) -> bool:
        return self.phase == 3

    def isEndofGame(self) -> bool:
        player = 1 if self.turn else 2
        return self.phase == 4 or all(t.player == player for t in TERRITORIES.values())

    def isStarted(self) -> bool:
        return self.phase >= 0
    
    def isPlaying(self) -> bool:
        return self.phase > 0 and self.phase < 4

    def isReady(self) -> bool:
        global PLAYERS
        both_ready = len(PLAYERS) == 3 and PLAYERS[1].ready and PLAYERS[2].ready
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
        global PLAYERS
        territories = list(TERRITORIES.values())
        import random
        random.shuffle(territories)
        PLAYERS[0].territories = territories[:14]
        PLAYERS[1].territories = territories[14:28]
        PLAYERS[2].territories = territories[28:]

        for territory in PLAYERS[1].territories:
            territory.player = 1
        for territory in PLAYERS[2].territories:
            territory.player = 2

        self.turn = (random.randint(1,10) % 2) == 0

    def player(self) -> Player:
        return PLAYERS[1 if self.turn else 2]

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
        if game.neutral:
            TERRITORIES[territory].armies += 1
            PLAYERS[0].armies -= 1
        else:
            TERRITORIES[territory].armies += armies
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
        TERRITORIES[attacker].armies -= armies
        offence = armies
        defence = TERRITORIES[defender].armies

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
            PLAYERS[TERRITORIES[defender].player].territories.remove(TERRITORIES[defender])
            TERRITORIES[defender].player = 1 if self.turn else 2
            TERRITORIES[defender].armies = offence
            self.player().territories += [ TERRITORIES[defender] ]

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
        TERRITORIES[origin].armies -= armies
        TERRITORIES[dest].armies += armies
        self.startEndOfTurn()
        game.determineState()
    
    def determineState(self) -> None:
        '''
        Valid action has taken place
        Adjust phase, turn, and neutral as needed
        '''
        if self.isSetup():
            if game.neutral:
                self.neutral = False
                self.turn = not self.turn
                self.player().armies = 2
                if PLAYERS[0].armies == 0:
                    self.startPlacement()
            else:
                game.neutral = True

        if self.isPlaying():
            if self.isEndOfTurn():
                self.turn = not self.turn
                self.startPlacement()

game = GameState()

def isYourTurn(id: str) -> bool:
    return (game.turn and PLAYABLE[id] == PLAYERS[1]) or (not game.turn and PLAYABLE[id] == PLAYERS[2])

def validPlacement(id: str, territory: str, armies: int) -> bool:
    global PLAYABLE
    if (game.neutral or (PLAYABLE[id].armies >= armies and armies > 0)):
        territories = PLAYERS[0].territories if game.neutral else PLAYABLE[id].territories
        return TERRITORIES[territory] in territories
    return False

def validCombat(id: str, attacker: str, defender: str, armies: int) -> bool:
    if TERRITORIES[attacker] in getAttackers(id) and TERRITORIES[defender] in getDefenders(id) and armies > 0:
        if TERRITORIES[defender] in TERRITORIES[attacker].neighbors:
            return TERRITORIES[attacker].armies > armies
    return False

def validTransfer(id: str, origin: str, dest: str, armies: int) -> bool:
    if TERRITORIES[origin] in getAttackers(id) and TERRITORIES[dest] in getAttackers(id) and armies >= 0:
        return TERRITORIES[origin].armies > armies
    return False
