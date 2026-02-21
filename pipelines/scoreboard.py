import polars as pl
import pandas as pd
from pipelines.base import Pipeline
from connectors.static_data import StaticDataConnector
from transforms.transform_data import Transform


class ScoreboardPipeline(Pipeline[pl.DataFrame]):

    def __init__(self, environment: str, iterations: int):
        super().__init__('scoreboard')

        self.url = 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'
        self.source = StaticDataConnector(self)
        self.file_source = 'tests/scoreboard'
        self.transformer = Transform(self)
        self.environment = environment
        self.iterations = iterations


    def extract(self):
        data_extract = self.source.fetch() if self.environment == 'Production' else self.source.fetch_file()
        bp = 'here'
        return data_extract


    def transform(self, data_extract):
        data_transformed = self.transformer.scoreboard(data_extract)
        return data_transformed



    def load(self, data_transformed):
        
        return data_transformed