from uuid import uuid4
from fastapi import FastAPI
from continents import *
from player import *
from territories import *
from game import *

app = FastAPI()

@app.get("/register/{name}")
async def register(name):
    global PLAYERS
    global PLAYABLE
    uuid = str(uuid4())

    if len(PLAYERS) < 3 and len(name) and len(name) <= len("Player 1"):
        PLAYERS.append(Player(name, id=uuid))
        PLAYABLE[uuid] = PLAYERS[-1]
    else:
        uuid = ""

    return {"id" : uuid}

@app.get('/start/{id}')
async def start(id: str):
    if isPlayer(id):
        PLAYABLE[id].ready = True
        return {"start" : game.isReady()}
    return {"error" : "need to register"}

@app.get('/board/{id}')
async def board(id):
    if isPlayer(id):
        opponent = PLAYERS[2] if PLAYABLE[id] is PLAYERS[1] else PLAYERS[1]
        return {
            "play" : 1 if game.turn else 2,
            "phase" : game.status(),
            "place" : PLAYABLE[id].armies,
            "neutral" : game.neutral,
            "players" : [ player.name for player in PLAYERS ],
            "board" : { name : { "player" : territory.player, "armies" : territory.armies } for name, territory in TERRITORIES.items()}
        }
    else:
        return {"valid": False, "error": "Invalid Player ID"}

@app.get('/place/{id}/{territory}/{armies}')
async def place(id: str, territory: str, armies: int):
    if isPlayer(id) and validTerritory(territory):
        if isYourTurn(id) and (game.isSetup() or game.isPlacement()):
            if validPlacement(id, territory, armies):
                game.place(territory, armies)
                return {"valid" : True}
            else:
                return {"valid": False, "error": "Invalid Placement"}
        else:
            return {"valid": False, "error": "Not your Turn or Place Phase"}
    else:
        return {"valid": False, "error": "Invalid Player ID or Territory"}
            
@app.get('/attack/{id}/{attacker}/{defender}/{armies}')
async def attack(id: str, attacker: str, defender: str, armies: int):
    if isPlayer(id) and validTerritory(attacker) and validTerritory(defender):
        if isYourTurn(id) and game.isCombat():
            if validCombat(id, attacker, defender, armies):
                result = game.combat(attacker, defender, armies)
                return {
                    "valid" : True,
                    "win" : result
                    }
            else:
                return {"valid": False, "error": "Invalid Combat"}
        else:
            return {"valid": False, "error": "Not your Turn or Combat Phase"}
    else:
        return {"valid": False, "error": "Invalid Player ID or Territory"}

@app.get('/transfer/{id}/{origin}/{dest}/{armies}')
async def transfer(id: str, origin: str, dest: str, armies: int):
    if isPlayer(id) and validTerritory(origin) and validTerritory(dest):
        if isYourTurn(id) and game.isCombat():
            if validTransfer(id, origin, dest, armies):
                game.transfer(origin, dest, armies)
                return {"valid" : True}
            else:
                return {"valid": False, "error": "Invalid Transfer"}
        else:
            return {"valid": False, "error": "Not your Turn or Combat Phase"}
    else:
        return {"valid": False, "error": "Invalid Player ID or Territory"}