from datetime import datetime, timedelta
from pathlib import Path
import requests
import pandas as pd  
from Headers import scoreboard
import urllib3
import json


def GetTodaysScoreboard(programMap: str, iterations: int):
    spacer = '╰╼╾╼'
    programMap += f'\n╰╼╾╼╼GetScoreboard.GetTodaysScoreboard╼╮\n'
    #region testing
    # if iterations <= 3: #first four runs
    #     file = scoreboards[4] 
    # elif iterations <= 11:
    #     file =  scoreboards [3]
    # elif iterations <= 15:
    #     file = scoreboards[2]
    # elif iterations <= 20:
    #     file = scoreboards[1]
    # else:
    #     file = scoreboards[0]
    file = scoreboards[2]


    #endregion testing
    try:
        # with open(f'Scoreboards/{file}.json', 'r', encoding='utf-8-sig') as f: #Testing
        #     data = json.load(f) #testing
        response = requests.get("https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json")
        data = response.json()
        columns = data['scoreboard']['games']
        dfScoreboard = pd.DataFrame(data['scoreboard']['games'])
        dfScoreboard, programMap = ParseScoreboard(dfScoreboard, programMap)
    except Exception as e:
        dfScoreboard = pd.DataFrame()
        print(f"Error downloading PlayerGameLogs: {e}")

    return dfScoreboard, programMap



scoreboards = [
'todaysScoreboard_00_01-17-26_1a',
'todaysScoreboard_00_01-17-26_1145p',
'todaysScoreboard_00_01-17-26_9p',
'todaysScoreboard_00_01-17-26_7p',
'todaysScoreboard_00_01-17-26_5p',
'todaysScoreboard_00_01-15-26_8p',
'todaysScoreboard_00_01-15-26_645p',
'todaysScoreboard_00_01-14-26_9a',
'todaysScoreboard_00_01-14-26_11p',
'todaysScoreboard_00_01-13-26_6p',
'todaysScoreboard_00_01-12-26_10a',
'todaysScoreboard_00_01-10-26_4p',
'todaysScoreboard_00_01-09-26_11a',
'todaysScoreboard_00_01-08-26_8p',
'todaysScoreboard_00_01-07-26_9a',
'todaysScoreboard_00_01-06-26_8p',
]

def ParseScoreboard(dfScoreboard: pd.DataFrame, programMap: str):
    '''
ParseScoreboard takes the original dfScoreboard and renames its columns to friendlier names and drops anything we dont need

:param dfScoreboard: Scoreboard DataFrame
'''    
    programMap += f'                                       ╰╼GetScoreboard.ParseScoreboard╼╮\n'
    programMap += f'╭╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╯\n'
    # for c in dfScoreboard.columns:
    #     PascalCase = c[:1].upper() + c[1:]
    #     print(f"'{c}': '{PascalCase}',")
    dfScoreboard = dfScoreboard[[
        'gameId',
        'gameCode',
        'gameStatus',
        'gameStatusText',
        'period',
        'gameClock',
        'gameTimeUTC',
        'gameEt',
        'regulationPeriods',
        'ifNecessary',
        'seriesGameNumber',
        'gameLabel',
        'gameSubLabel',
        'seriesText',
        'seriesConference',
        'poRoundDesc',
        'gameSubtype',
        'isNeutral',
        'homeTeam',
        'awayTeam',        
    ]].rename(columns={
        'gameId': 'GameID',
        'gameCode': 'GameCode',
        'gameStatus': 'GameStatus',
        'gameStatusText': 'GameStatusText',
        'period': 'Period',
        'gameClock': 'GameClock',
        'gameTimeUTC': 'GameTimeUTC',
        'gameEt': 'GameEt',
        'regulationPeriods': 'RegulationPeriods',
        'ifNecessary': 'IfNecessary',
        'seriesGameNumber': 'SeriesGameNumber',
        'gameLabel': 'GameLabel',
        'gameSubLabel': 'GameSubLabel',
        'seriesText': 'SeriesText',
        'seriesConference': 'SeriesConference',
        'poRoundDesc': 'PoRoundDesc',
        'gameSubtype': 'GameSubtype',
        'isNeutral': 'IsNeutral',
        'homeTeam': 'HomeTeam',
        'awayTeam': 'AwayTeam',
    }).astype({
        'GameID': int
    })

    return dfScoreboard, programMap


