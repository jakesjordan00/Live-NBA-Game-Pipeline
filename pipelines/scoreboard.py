import polars as pl
import pandas as pd
from pipelines.base import Pipeline
from connectors.static_data import StaticDataConnector
from transforms.transform_data import Transform


class ScoreboardPipeline(Pipeline[list]):

    def __init__(self, environment: str):
        super().__init__('scoreboard')

        self.url = 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'
        self.source = StaticDataConnector(self)
        self.file_source = 'tests/scoreboard'
        self.transformer = Transform(self)
        self.environment = environment


    def extract(self):
        '''        
        Fetches Scoreboard data from NBA's static data feed

        :return data (dict): Dict containing 'meta' and **'scoreboard'** dicts
        '''
        data_extract = self.source.fetch() if self.environment == 'Production' else self.source.fetch_file()
        bp = 'here'
        return data_extract


    def transform(self, data_extract):
        '''
        Returns a list of formatted Scoreboard dictionaries


        :param data_extract: Output of fetch()/extract(). Contains game information for today's games
        :type data: dict
        :return scoreboard: List of games taking place today that are **In progress** or **Completed**
        :rtype: list
        '''
        data_transformed = self.transformer.scoreboard(data_extract)
        return data_transformed



    def load(self, data_transformed):
        
        return data_transformed