import pandas as pd
import polars as pl

from pipelines.base import Pipeline
from connectors.static_data import StaticDataConnector
from transforms.transform_boxscore import Transform


class BoxscorePipeline(Pipeline[dict]):

    def __init__(self, scoreboard_data: pl.DataFrame, environment: str, iterations: int):
        super().__init__('Boxscore')
        self.GameID = scoreboard_data['GameID']
        self.GameIDStr = scoreboard_data['GameIDStr']
        self.Data = scoreboard_data
        self.url = f'https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{self.GameIDStr}.json'
        self.source = StaticDataConnector(self)
        self.transformer = Transform(self)
        self.environment = environment
        self.file_source = f'tests/box/{self.GameID}'
        self.iterations = iterations
        
    def extract(self):
        data_extract = self.source.fetch() if self.environment == 'Production' else self.source.fetch_file()
        self.logger.info(f'Extracted {self.GameID} Box data')
        return data_extract


    def transform(self, data_extract):
        data_transformed = self.transformer.box(data_extract)
        self.logger.info(f'Transformed Box data to {', '.join(name for name, data in data_transformed['sql_tables'].items())}')
        bp = 'here'
        return data_transformed



    def load(self, data_transformed):
        data_loaded = self.destination.initiate_insert(data_transformed['sql_tables'])

        return data_transformed