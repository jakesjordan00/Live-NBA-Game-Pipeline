from datetime import datetime, timedelta
from pathlib import Path
import requests
import pandas as pd  
from Headers import scoreboard
import urllib3
import json



def GetSchedule():
    try:
        response = requests.get('https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_1.json')
        data = response.json()
        schedule = data['leagueSchedule']['gameDates']

        dfGames = ParseDates(schedule)
    except Exception as e:
        dfScoreboard = pd.DataFrame()
        print(f"Error: {e}")

    return dfGames


def ParseDates(schedule):
    games = []
    now = datetime.now()
    today = datetime.now().date()
    for date in schedule:
        gDate = datetime.strptime(date['gameDate'], '%m/%d/%Y %H:%M:%S').date()
        for game in date['games']:
            gameDateTime = datetime.strptime(game['gameDateTimeEst'], '%Y-%m-%dT%H:%M:%SZ')
            if gameDateTime > now:
                continue
            games.append(game)
        if gDate > today:
            break

    dfGames = pd.DataFrame(games)
    dfGames = ParseSchedule(dfGames)
    return dfGames


def ParseSchedule(dfGames: pd.DataFrame):
    try:
        dfGames = dfGames[[
        'gameId',
        'gameCode',
        'gameStatus',
        'gameStatusText',
        'gameDateTimeUTC',
        'gameDateTimeEst',
        'ifNecessary',
        'seriesGameNumber',
        'gameLabel',
        'gameSubLabel',
        'seriesText',
        'gameSubtype',
        'isNeutral',
        'homeTeam',
        'awayTeam',        
    ]].rename(columns={
        'gameId': 'GameID',
        'gameCode': 'GameCode',
        'gameStatus': 'GameStatus',
        'gameStatusText': 'GameStatusText',
        'gameDateTimeUTC': 'GameDateTimeUTC',
        'gameDateTimeEst': 'GameDateTimeEST',
        'regulationPeriods': 'RegulationPeriods',
        'ifNecessary': 'IfNecessary',
        'seriesGameNumber': 'SeriesGameNumber',
        'gameLabel': 'GameLabel',
        'gameSubLabel': 'GameSubLabel',
        'seriesText': 'SeriesText',
        'gameSubtype': 'GameSubtype',
        'isNeutral': 'IsNeutral',
        'homeTeam': 'HomeTeam',
        'awayTeam': 'AwayTeam',
    }).astype({
        'GameID': int
    })
    except Exception as e:
        print(e)
        test = e
        a = 1

    return dfGames




