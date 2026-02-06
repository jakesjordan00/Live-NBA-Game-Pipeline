import pandas as pd
import polars as pl

from pipelines.base import Pipeline
from connectors.static_data import StaticDataConnector
from transforms.transform_boxscore import Transform


class BoxscorePipeline(Pipeline):

    def __init__(self, game_data: pl.DataFrame):
        super().__init__('Boxscore')
        self.GameID = game_data['GameID'][0]
        self.GameIDStr = game_data['GameIDStr'][0]
        self.Data = game_data[0].row(0, named=True)
        self.url = f'https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{self.GameIDStr}.json'
        self.source = StaticDataConnector(self)
        self.transformer = Transform(self)
        #Need self.loader here
        
    def extract(self):
        data_extract = self.source.fetch()
        bp = 'here'
        return data_extract


    def transform(self, data_extract):
        data_transformed = self.transformer.box(data_extract)
        bp = 'here'
        return data_transformed



    def load(self, data):
        pass