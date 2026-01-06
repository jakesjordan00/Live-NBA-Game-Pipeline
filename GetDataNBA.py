from URLs import BoxScore, PlayByPlay
import requests
import pandas as pd
from ParseBox import InitiateBox
from SQL_Writes import InsertGame, InsertTeamBox, InsertPlayerBox

def GetBox(GameID: int):
    '''
    Docstring for GetBox
    
    :param GameID: GameID of game
    :type GameID: int
    '''
    try:
        response = requests.get(f'{BoxScore}00{GameID}.json')
        data = response.json()
        game = data['game']
        Box = InitiateBox(game)
    except Exception as e:
        Box = None
        print(f"Error downloading BoxScore: {e}")

    return Box


def InsertBox(Box: dict):
    gStatus = InsertGame(Box['Game'], Box['GameExt'])
    tBoxStatus = InsertTeamBox(Box['TeamBox'])
    pBoxStatus = InsertPlayerBox(Box['PlayerBox'])
    
    return f'{gStatus}, {tBoxStatus}, {pBoxStatus}'


def GetPlayByPlay():

    return 1