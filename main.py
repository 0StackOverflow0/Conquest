from fastapi import FastAPI
from continents import *
from player import *
from territories import *
from game import *

app = FastAPI()

@app.get("/register/{name}")
async def register(name):
    return {"id" : game.register(name)}

@app.get('/start/{id}')
async def start(id: str):
    if game.start(id):
        return {"start" : game.isReady()}
    return {"error" : "need to register"}

@app.get('/board/{id}')
async def board(id):
    if game.isPlayer(id):
        return game.board(id)
    else:
        return {"valid": False, "error": "Invalid Player ID"}

@app.get('/place/{id}/{territory}/{armies}')
async def place(id: str, territory: str, armies: int):
    if game.isPlayer(id) and validTerritory(territory):
        if game.isYourTurn(id) and (game.isSetup() or game.isPlacement()):
            if game.validPlacement(id, territory, armies):
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
    if game.isPlayer(id) and validTerritory(attacker) and validTerritory(defender):
        if game.isYourTurn(id) and game.isCombat():
            if game.validCombat(id, attacker, defender, armies):
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
    if game.isPlayer(id) and validTerritory(origin) and validTerritory(dest):
        if game.isYourTurn(id) and game.isCombat():
            if game.validTransfer(id, origin, dest, armies):
                game.transfer(origin, dest, armies)
                return {"valid" : True}
            else:
                return {"valid": False, "error": "Invalid Transfer"}
        else:
            return {"valid": False, "error": "Not your Turn or Combat Phase"}
    else:
        return {"valid": False, "error": "Invalid Player ID or Territory"}