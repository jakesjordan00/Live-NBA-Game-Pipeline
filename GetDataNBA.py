from URLs import urlBoxScore, urlPlayByPlay
import requests
import pandas as pd
from ParseBox import InitiateBox
from ParsePlayByPlay import InitiatePlayByPlay
from SQL_Writes import InsertBoxscores, InsertGame, InsertTeamBox, InsertPlayerBox, InsertPlayByPlay
from FormatBoxUpdates import *

def GetBox(GameID: int, sender: str):
    '''
    Hits Boxscore.json url of GameID passed
    
    :param GameID: GameID of game
    :type GameID: int
    '''
    if sender == 'MainFunction':
        print(f'     Retrieving Box data')
    urlBox = f'{urlBoxScore}00{GameID}.json'
    try:
        response = requests.get(urlBox)
        data = response.json()
        game = data['game']
        Box = InitiateBox(game, sender)
    except Exception as e:
        print(f"Error getting Boxscore data: {e}")

    return Box


def InsertBox(Box: dict):
    gStatus = InsertGame(Box['Game'], Box['GameExt'])
    boxStatus = InsertBoxscores(Box['TeamBox'], Box['PlayerBox'], Box['StartingLineups'])

    return f'{gStatus}\n{boxStatus}'

def UpdateBox(Box: dict):
    updateStatus = FormatUpdates(Box)
    return updateStatus


def GetPlayByPlay(SeasonID: int, GameID: int, ActionCount: int, sender: str):
    if 'MainFunction' in sender:
        print(f'     Retrieving PlayByPlay data')
    urlPbp = f'{urlPlayByPlay}00{GameID}.json'
    try:
        response = requests.get(urlPbp)
        data = response.json()
        actions = data['game']['actions']
        PlayByPlay = InitiatePlayByPlay(SeasonID, GameID, actions, ActionCount, sender)
    except Exception as e:
        Box = None
        print(f"Error getting PlayByPlay data: {e}")

    return PlayByPlay

def InsertPbp(PlayByPlay: list):
    pbpStatus = InsertPlayByPlay(PlayByPlay)
    return f'{pbpStatus}'