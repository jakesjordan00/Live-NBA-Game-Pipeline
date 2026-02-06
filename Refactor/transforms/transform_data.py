import pandas as pd
import polars as pl



class Transform:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        pass


    def scoreboard(self, data):
        data = data['scoreboard']['games']
        dfScoreboard = pd.DataFrame(data)
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
        })
        dfScoreboard['GameIDStr'] = dfScoreboard['GameID'].astype(str)
        dfScoreboard['GameID'] = dfScoreboard['GameID'].astype(int)
        dfplScoreboard = pl.from_pandas(dfScoreboard)

        return dfScoreboard

