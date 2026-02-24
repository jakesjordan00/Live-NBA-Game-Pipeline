import pandas as pd
import polars as pl



class Transform:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        pass


    def scoreboard(self, data) -> list:
        data = data['scoreboard']['games']

        scoreboard = [
            {
                'SeasonID': f'20{g['gameId'][3:5]}',
                'GameID': int(g['gameId']),
                'GameIDStr': g['gameId'],             
                'GameCode': g['gameCode'],
                'GameStatus': g['gameStatus'],
                'GameStatusText': g['gameStatusText'],
                'Period': g['period'],
                'GameClock': g['gameClock'],
                'GameTimeUTC': g['gameTimeUTC'],
                'GameEt': g['gameEt'],
                'RegulationPeriods': g['regulationPeriods'],
                'IfNecessary': g['ifNecessary'],
                'SeriesGameNumber': g['seriesGameNumber'],
                'GameLabel': g['gameLabel'],
                'GameSubLabel': g['gameSubLabel'],
                'SeriesText': g['seriesText'],
                'SeriesConference': g['seriesConference'],
                'RoundDesc': g['poRoundDesc'],
                'GameSubtype': g['gameSubtype'],
                'IsNeutral': g['isNeutral'],
                'HomeTeam': g['homeTeam'],
                'AwayTeam': g['awayTeam'],
                }             
            for g in data if g['gameStatus'] != 1]
        return scoreboard

