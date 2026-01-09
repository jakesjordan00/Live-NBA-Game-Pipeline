from datetime import datetime, timedelta
from pathlib import Path
import requests
import pandas as pd  
from Headers import scoreboard
import urllib3
import json



def GetTodaysScoreboard():
    try:
        # with open('todaysScoreboard_00_010826.json', 'r', encoding='utf-8-sig') as f: #Testing
        #     data = json.load(f) #testing
        response = requests.get("https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json")
        data = response.json()
        columns = data['scoreboard']['games']
        dfScoreboard = pd.DataFrame(data['scoreboard']['games'])
        dfScoreboard = ParseScoreboard(dfScoreboard)
    except Exception as e:
        dfScoreboard = pd.DataFrame()
        print(f"Error downloading PlayerGameLogs: {e}")

    return dfScoreboard




def ParseScoreboard(dfScoreboard: pd.DataFrame):
    '''
ParseScoreboard takes the original dfScoreboard and renames its columns to friendlier names and drops anything we dont need

:param dfScoreboard: Scoreboard DataFrame
'''
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

    return dfScoreboard




#If it's before 6am, use Yesterday's scoreboard instead. This will catch any games that are ongoing past midnight
date = (datetime.now() - timedelta(days=1) if datetime.now().hour < 6 else datetime.now()).strftime("%Y-%m-%d")

date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

def GetTodaysScoreboard1():
    '''
Hits the NBA api and retrieves the Scoreboard for today's (or yesterday's) games depending on the time.
 '''   
    url = 'https://stats.nba.com/stats/scoreboardv2'
    parameters = {
        'LeagueID':'00',
        'DayOffset': 0,
        'GameDate': date
        }
    
    try:
        response = requests.get(url, params=parameters, headers=scoreboard, timeout=30)
        data = response.json()
        columns = data['resultSets'][0]['headers']
        rows = data['resultSets'][0]['rowSet']
        dfScoreboard = pd.DataFrame(rows, columns=columns)
        dfScoreboard = ParseScoreboard(dfScoreboard)
    except Exception as e:
        df = pd.DataFrame()
        print(f"Error downloading PlayerGameLogs: {e}")
    return dfScoreboard
