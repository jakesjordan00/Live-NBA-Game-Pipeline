import pandas as pd
import polars as pl

from pipelines.base import Pipeline
from connectors.static_data import StaticDataConnector
from transforms.transform_playbyplay import Transform

class PlayByPlayPipeline(Pipeline[dict]):
    def __init__(self, scoreboard_data, boxscore_data, start_action = 0):
        super().__init__('PlayByPlay')
        self.GameID = scoreboard_data['GameID']
        self.GameIDStr = scoreboard_data['GameIDStr']
        self.url = f'https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_{self.GameIDStr}.json'
        self.source = StaticDataConnector(self)
        self.transformer = Transform(self)
        self.start_action = start_action
        self.Data = {
            'scoreboard_data': scoreboard_data,
            'boxscore_data': boxscore_data
        }

    def extract(self):
        data_extract = self.source.fetch()
        return data_extract


    def transform(self, data_extract):
        data_transformed = self.transformer.playbyplay(data_extract)
        return data_transformed



    def load(self, data):
        pass