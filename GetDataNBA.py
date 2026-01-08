from URLs import urlBoxScore, urlPlayByPlay
import requests
import pandas as pd
from ParseBox import InitiateBox
from ParsePlayByPlay import InitiatePlayByPlay
from SQL_Writes import InsertBoxscores, InsertGame, InsertTeamBox, InsertPlayerBox, InsertPlayByPlay

def GetBox(GameID: int):
    '''
    Hits Boxscore.json url of GameID passed
    
    :param GameID: GameID of game
    :type GameID: int
    '''
    print(f'     Retrieving Box data')
    urlBox = f'{urlBoxScore}00{GameID}.json'
    try:
        response = requests.get(urlBox)
        data = response.json()
        game = data['game']
        Box = InitiateBox(game)
    except Exception as e:
        Box = None
        print(f"Error getting Boxscore data: {e}")

    return Box


def InsertBox(Box: dict):
    gStatus = InsertGame(Box['Game'], Box['GameExt'])
    boxStatus = InsertBoxscores(Box['TeamBox'], Box['PlayerBox'], Box['StartingLineups'])

    return f'{gStatus}\n{boxStatus}'



def GetPlayByPlay(SeasonID: int, GameID: int, ActionCount: int, sender: str):
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