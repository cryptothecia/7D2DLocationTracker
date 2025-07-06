import requests
import os
from math import dist
from dotenv import load_dotenv

load_dotenv()
TOKEN_NAME = os.getenv('TOKEN_NAME')
TOKEN_VALUE = os.getenv('TOKEN_VALUE')
WEB_URL = os.getenv('WEB_URL')
headers = {
    "X-SDTD-API-TOKENNAME": TOKEN_NAME,
    "X-SDTD-API-SECRET": TOKEN_VALUE,
    "Content-Type": "application/json"
}

class Player:
    def __init__(self,player_data:dict):
        self.id = player_data['entityId']
        self.name = player_data['name']
        self.pos = player_data['position']
        self.posX = player_data['position']['x']
        self.posY = player_data['position']['y']
        self.posZ = player_data['position']['z']
        self.level = player_data['level']
        self.health = player_data['health']
        self.stamina = player_data['stamina']
        self.deaths = player_data['deaths']
        self.kills = player_data['kills']['zombies']

class Location:
    def __init__(self,minX:float,maxX:float,minY:float,maxY:float,minZ:float,maxZ:float,name:str=""):
        self.minX = minX
        self.maxX = maxX
        self.X = sum([self.minX, self.maxX])/2
        self.minY = minY
        self.maxY = maxY
        self.Y = sum([self.minY, self.maxY])/2
        self.minZ = minZ
        self.maxZ = maxZ
        self.Z = sum([self.minZ, self.maxZ])/2
        self.name = name
    def check(self,player:Player):
        distance = dist([player.posX, player.posZ], [self.X, self.Z])
        if player.posX < self.maxX and player.posX > self.minX and player.posY < self.maxY and player.posY > self.minY and player.posZ < self.maxZ and player.posZ > self.minZ:
            inside = True
            print(f"{player.name} is inside {self.name}")
        else:
            inside = False
            print(f"{player.name} is {distance:.2f} units from {self.name}")
        return { "inside" : inside, "distance" : distance }

def get_players():
    url = WEB_URL + '/player'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = (response.json())['data']['players']
        players = []
        for player in data:
            players.append(Player(player))
        return players
    else:
        print(response.status_code)
        return None
    
def send_command(command:str):
    url = WEB_URL + '/command'
    body = {
        "command": command
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        print(f'Sent to server: {command}')
        return True
    else:
        print(response.status_code)
        return False