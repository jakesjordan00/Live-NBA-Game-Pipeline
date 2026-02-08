import pandas as pd
import polars as pl

from pipelines.base import Pipeline
from connectors.static_data import StaticDataConnector
from transforms.transform_data import Transform

class PlayByPlayPipeline(Pipeline[dict]):
    def __init__(self, scoreboard_data, boxscore_data):
        super().__init__('PlayByPlay')
        self.GameID = scoreboard_data['GameID']
        self.GameIDStr = scoreboard_data['GameIDStr']
        self.url = f'https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_{self.GameIDStr}.json'
        self.source = StaticDataConnector(self)
        self.transformer = Transform(self)

    def extract(self):
        data_extract = self.source.fetch()
        return data_extract


    def transform(self, data_extract):
        data_transformed = pl.DataFrame(data_extract['game']['actions'])
        return data_transformed



    def load(self, data):
        pass