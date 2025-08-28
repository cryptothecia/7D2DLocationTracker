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
        self.Zkills = player_data['kills']['zombies']

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

# To be used with the data from gameprefs or gamestats
class GameData:
    def __init__(self,data:list):
        self.data = data
    def get(self,search_str:str):
        if self.data is not None:
            query = next((item for item in self.data if item['name'] == search_str), None)
        else: 
            return None
        if query is not None:
            return query['value']

def send_request(url:str,headers:dict[str]=headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = (response.json())['data']
            return data
        else:
            print(response.status_code)
            return None
    except: 
        return None

def get_players():
    url = WEB_URL + '/player'
    data = send_request(url, headers=headers)
    if data is not None:
        data = data['players']
        players = []
        for player in data:
            players.append(Player(player))
        return players
    else:
        return None

def get_game_prefs():
    url = WEB_URL + "/gameprefs"
    data = send_request(url, headers=headers)
    return data
    
def get_game_stats():
    url = WEB_URL + "/gamestats"
    data = send_request(url, headers=headers)
    return data
    
def get_server_stats():
    url = WEB_URL + "/serverstats"
    data = send_request(url, headers=headers)
    return data 
    
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