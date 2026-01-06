from URLs import BoxScore, PlayByPlay
import requests
import pandas as pd
from ParseBox import InitiateBox


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
        status = InitiateBox(game)
    except Exception as e:
        status = False
        print(f"Error downloading BoxScore: {e}")

    return status




def GetPlayByPlay():

    return 1