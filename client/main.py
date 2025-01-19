import sys

import json
import math
import time
import pygame
import pygame.imageext
import requests

from territories import *
from pygame.locals import *
 
pygame.init()
pygame.font.init()

USER = "JANUS" if len(sys.argv) < 2 else sys.argv[1]
UUID = ""
SERVER = "127.0.0.1"
PORT = 8000
TURN = False
PLACE = 0
STATUS = "UNKNOWN"
NEUTRAL = False
PLAYERS = []
PLAYER_NUMBER = 0
ARMIES = 1

my_font = pygame.font.SysFont('Helvetica', 18)
 
fps = 10
fpsClock = pygame.time.Clock()
 
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

WORLD_MAP = pygame.image.load("map.png").convert()

def closest_territory(pos: tuple[int, int]) -> str:
    closest = ("",50)
    for tr in TERRITORIES.values():
        distance = math.dist(pos, tr.loc)
        if distance < closest[1]:
            closest = (tr.name, distance)

    return closest[0]

def select_territory():
    global SELECTED
    pos = pygame.mouse.get_pos()
    name = closest_territory(pos)
    if len(name):
        if len(SELECTED) and name in SELECTED:
            SELECTED.remove(name)
        else:
            SELECTED.append(name)
            if STATUS in ["Setup", "Place"]:
                if len(SELECTED) > 1:
                    SELECTED = SELECTED[-1:]
            elif len(SELECTED) > 2:
                SELECTED = SELECTED[-2:]

def place(armies: int) -> bool:
    if len(SELECTED) == 1:
        resp = requests.get(f"http://{SERVER}:{PORT}/place/{UUID}/{SELECTED[0]}/{armies}")
        if resp.status_code == 200:
            content = json.loads(resp.content)
            if content.get("valid") is not None:
                if content["valid"]:    
                    return True
                else:
                    print(f"Error placing {UUID} : {SELECTED[0]} : {armies} : {content['error']}")
                    return False
        else:
            print(f"Error placing army {UUID} : {SELECTED[0]} : {armies}")
            return False
    else:
        print("No Territory Selected!")
        return False

def attack(armies: int) -> tuple[bool, bool]:
    if len(SELECTED) == 2:
        resp = requests.get(f"http://{SERVER}:{PORT}/attack/{UUID}/{SELECTED[0]}/{SELECTED[1]}/{armies}")
        if resp.status_code == 200:
            content = json.loads(resp.content)
            if content.get("valid") is not None:
                if content["valid"]:    
                    return True, content["win"]
                else:
                    print(f"Error attacking {UUID} : {SELECTED[0]} : {SELECTED[1]} : {armies} : {content['error']}")
                    return False, None
        else:
            print(f"Error attacking {UUID} : {SELECTED[0]} : {SELECTED[1]} : {armies}")
            return False, None
    else:
        print("Need two Territories Selected!")
        return False, None

def transfer(armies: int) -> bool:
    origin = ""
    dest = ""
    if len(SELECTED) == 2:
        origin = SELECTED[0]
        dest = SELECTED[1]
    elif len(SELECTED) == 1:
        origin = SELECTED[0]
        dest = SELECTED[0]
    else:
        print("Need a Territory Selected!")
        return False

    resp = requests.get(f"http://{SERVER}:{PORT}/transfer/{UUID}/{origin}/{dest}/{armies}")
    if resp.status_code == 200:
        content = json.loads(resp.content)
        if content.get("valid") is not None:
            if content["valid"]:    
                return True
            else:
                print(f"Error transfering {UUID} : {origin} : {dest} : {armies} : {content['error']}")
                return False
    else:
        print(f"Error transfering {UUID} : {origin} : {dest} : {armies}")
        return False

def select_action():
    # Display available actions
    # Check if pos in near action
    # User needs to select Territories before Action
    pass

def update():
    global ARMIES
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            select_territory()
            select_action()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                place(ARMIES)
            elif event.key == pygame.K_a:
                if attack(ARMIES):
                    SELECTED.clear()
            elif event.key == pygame.K_t:
                transfer(ARMIES)
            elif event.key == pygame.K_c:
                SELECTED.clear()
            elif event.key == pygame.K_UP:
                ARMIES += 1
            elif event.key == pygame.K_DOWN:
                ARMIES -= 1 if ARMIES > 1 else 0

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
  
def draw(screen: pygame.Surface):
    screen.fill((0, 0, 0))
    screen.blit(WORLD_MAP, (0, 0))

    color = (255,255,255)
    if PLAYER_NUMBER == 1:
        color = (255,128,0)
    elif PLAYER_NUMBER == 2:
        color = (128,255,0)

    screen.blit(my_font.render(USER, False, color), (400,20))
    
    color = (255,0,0)
    if not NEUTRAL:
        screen.blit(my_font.render(f"{PLAYERS[TURN]}'s Turn", False, color), (500, 440))
    else:
        screen.blit(my_font.render(f"{PLAYERS[TURN]}'s Neutral", False, color), (500, 440))

    screen.blit(my_font.render(f"{STATUS} Phase", False, color), (500, 460))

    color = (255,255,255)
    screen.blit(my_font.render(f"Commit #{ARMIES}", False, color), (180, 220))
    screen.blit(my_font.render(f"Avail #{PLACE}", False, color), (180, 240))

    for tr in TERRITORIES.values():
        if tr.loc != (0, 0):
            color = (255,255,255)
            if tr.player == 1:
                color = (255,128,0)
            elif tr.player == 2:
                color = (128,255,0)
            if len(SELECTED) and tr.name == SELECTED[0]:
                color = (255,0,0)
            elif len(SELECTED) > 1 and tr.name == SELECTED[1]:
                color = (0,0,255)
            screen.blit(my_font.render(f'{tr.armies}', False, color), tr.loc)

    pygame.display.flip()

resp = requests.get(f"http://{SERVER}:{PORT}/register/{USER}")

if resp.status_code != 200:
    print(f"Error Registering User {USER} : {resp.status_code}")
    pygame.quit()
    sys.exit()

registration = json.loads(resp.content)
if registration.get("id"):
    UUID = registration["id"]
    print(f"Registered as {USER} : {UUID}")
else:
    print(f"Error Registering User {USER} : Game is Full")
    pygame.quit()
    sys.exit()

started = False
while not started:
    resp = requests.get(f"http://{SERVER}:{PORT}/start/{UUID}")
    if resp.status_code != 200:
        print(f"Error Starting Game {UUID} : {resp.status_code}")
        pygame.quit()
        sys.exit()
    content = json.loads(resp.content)
    print(content)
    if content.get("start") is not None:
        started = content["start"]
        if not started:
            time.sleep(2.0)
    else:
        print(f"Error Starting Game {UUID} : {content.get('error')}")
        pygame.quit()
        sys.exit()

def load_board():
    resp = requests.get(f"http://{SERVER}:{PORT}/board/{UUID}")
    if resp.status_code == 200:
        content = json.loads(resp.content)
        if not content.get("error"):
            global TURN, STATUS, PLACE, NEUTRAL, PLAYERS, PLAYER_NUMBER
            old_turn = TURN
            TURN = content["play"]
            if old_turn != TURN:
                SELECTED.clear()
            STATUS = content["phase"]
            PLACE = content["place"]
            old_neutral = NEUTRAL
            NEUTRAL = content["neutral"]
            if old_neutral != NEUTRAL:
                SELECTED.clear()
            PLAYERS = content["players"]
            PLAYER_NUMBER = PLAYERS.index(USER)
            board = content["board"]
            for name, attr in board.items():
                if name in TERRITORIES:
                    TERRITORIES[name].player = attr["player"]
                    TERRITORIES[name].armies = attr["armies"]
        else:
            print(f"Error Loading Board {UUID} : {content.get('error')}")
            pygame.quit()
            sys.exit()

while True:
    load_board()
    update()
    draw(screen)
    fpsClock.tick(fps)
