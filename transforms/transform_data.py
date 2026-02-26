import pandas as pd
import polars as pl
from datetime import datetime
import logging



class Transform:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.logger = logging.getLogger(f'{pipeline.pipeline_name}.transform')
        pass


    def scoreboard(self, data: dict) -> list:
        '''
        Returns a list of formatted Scoreboard dictionaries

        :param data: Output of fetch(). Contains game information for today's games
        :type data: dict
        :return scoreboard: List of games taking place today that are **In progress** or **Completed**
        :rtype: list
        '''
        data = data['scoreboard']['games']
        scoreboard = [
            {
                'SeasonID': int(f'20{g['gameId'][3:5]}'),
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

