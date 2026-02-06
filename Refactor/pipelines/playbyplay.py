import pandas as pd
import polars as pl

from pipelines.base import Pipeline
from connectors.static_data import StaticDataConnector
from transforms.transform_data import Transform

class PlayByPlayPipeline(Pipeline):
    def __init__(self, game_data):
        super().__init__('PlayByPlay')
        self.GameID = game_data['GameID']
        self.GameIDStr = game_data['GameIDStr']
        self.url = f'https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_{self.GameIDStr}.json'
        self.source = StaticDataConnector(self)
        self.transformer = Transform(self)

    def extract(self):
        pass


    def transform(self, data):
        pass



    def load(self, data):
        pass