import pandas as pd
import polars as pl



class Transform:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        pass


    def scoreboard(self, data):
        data = data['scoreboard']['games']        
        dfplScoreboard = pl.DataFrame(data)
        dfplScoreboard = dfplScoreboard.select([
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
        ]).rename({            
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
        })
        dfplScoreboard = dfplScoreboard.with_columns(
            pl.col('GameID').alias('GameIDStr')
        ).cast({'GameID': pl.Int64})
        return dfplScoreboard

