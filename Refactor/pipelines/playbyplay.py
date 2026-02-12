import pandas as pd
import polars as pl

from pipelines.base import Pipeline
import config.api_map
from connectors.static_data import StaticDataConnector
from connectors.api_data import APIDataConnector
from transforms.transform_playbyplay import Transform

class PlayByPlayPipeline(Pipeline[dict]):
    def __init__(self, scoreboard_data, boxscore_data, environment: str, start_action = 0):
        super().__init__('PlayByPlay')
        self.GameID = scoreboard_data['GameID']
        self.GameIDStr = scoreboard_data['GameIDStr']
        self.url = f'https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_{self.GameIDStr}.json'
        self.source = StaticDataConnector(self)
        self.environment = environment
        self.file_source = 'Refactor/tests/playbyplay'

        
        self.transformer = Transform(self)
        self.start_action = start_action
        self.Data = {
            'scoreboard_data': scoreboard_data,
            'boxscore_data': boxscore_data
        }

    def extract(self):
        static_data_extract = self.source.fetch() if self.environment == 'Production' else self.source.fetch_file()
        if static_data_extract == None:
            bp= 'here'
            """Need to handle error here
       !                                                                                    !"""
        

        return static_data_extract


    def transform(self, data_extract):
        data_transformed = self.transformer.playbyplay(data_extract)
        return data_transformed



    def load(self, data_transformed):
        data_loaded = data_transformed
        return data_loaded