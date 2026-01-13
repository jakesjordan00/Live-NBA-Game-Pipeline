from URLs import urlBoxScore, urlPlayByPlay
import requests
import pandas as pd
from ParseBox import InitiateBox
from ParsePlayByPlay import InitiatePlayByPlay
from SQL_Writes import InsertBoxscores, InsertGame, InsertTeamBox, InsertPlayerBox, InsertPlayByPlay
from FormatBoxUpdates import *

def GetBox(GameID: int, Data: dict, sender: str, programMap: str):
    '''
    Hits Boxscore.json url of GameID passed
    
    :param GameID: GameID of game
    :type GameID: int
    '''
    programMap += 'GetBox ➡️ '
    if sender == 'MainFunction':
        print(f'     Retrieving Box data')
    urlBox = f'{urlBoxScore}00{GameID}.json'
    try:
        response = requests.get(urlBox)
        data = response.json()
        game = data['game']
        Box, programMap = InitiateBox(game, Data, sender, programMap)
    except Exception as e:
        print(f"Error getting Boxscore data: {e}")

    return Box, programMap


def InsertBox(Box: dict, programMap: str):
    programMap += 'InsertBox ➡️ '
    gStatus = InsertGame(Box['Game'], Box['GameExt'])
    boxStatus = InsertBoxscores(Box['TeamBox'], Box['PlayerBox'], Box['StartingLineups'])

    return f'{gStatus}\n{boxStatus}', programMap



def UpdateBox(Box: dict, programMap: str):
    programMap += 'UpdateBox ➡️ '
    updateStatus = FormatUpdates(Box)
    return updateStatus, programMap



def GetPlayByPlay(SeasonID: int, GameID: int, ActionCount: int, sender: str, programMap: str):
    programMap += 'GetPlayByPlay ➡️ '
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
    return PlayByPlay, programMap



def InsertPbp(PlayByPlay: list, programMap: str):
    programMap += 'InsertPbp ➡️ '
    pbpStatus = InsertPlayByPlay(PlayByPlay)
    return f'{pbpStatus}', programMap