from datetime import datetime, timedelta
import pandas as pd



def Transform(scoreboardList: list):
    dfScoreboard = pd.DataFrame(data=scoreboardList)
    scoreboard = ParseScoreboard(dfScoreboard)
    
    return scoreboard


def ParseScoreboard(dfScoreboard: pd.DataFrame):
    scoreboard = dfScoreboard[[
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
    return scoreboard