import pandas as pd
import polars as pl

from pipelines.base import Pipeline
import config.api_map
from connectors.static_data import StaticDataConnector
from connectors.api_data import APIDataConnector
from transforms.transform_playbyplay import Transform

class PlayByPlayPipeline(Pipeline[dict]):
    def __init__(self, scoreboard_data, boxscore_data, start_action: int, home_stats: dict | None, away_stats: dict | None, environment: str, iterations: int):
        super().__init__('PlayByPlay')
        self.GameID = scoreboard_data['GameID']
        self.GameIDStr = scoreboard_data['GameIDStr']
        self.url = f'https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_{self.GameIDStr}.json'
        self.source = StaticDataConnector(self)
        self.environment = environment
        self.file_source = f'Refactor/tests/pbp/{self.GameID}'
        self.iterations = iterations

        
        self.transformer = Transform(self)
        self.start_action = start_action
        self.home_stats = home_stats
        self.away_stats = away_stats
        self.Data = {
            'scoreboard_data': scoreboard_data,
            'boxscore_data': boxscore_data
        }

    def extract(self):
        static_data_extract = self.source.fetch() if self.environment == 'Production' else self.source.fetch_file()
        if static_data_extract:
            self.logger.info(f'Extracted {self.GameID} Playbyplay data, {len(static_data_extract['game']['actions'])} actions')

        if static_data_extract == None:
            self.logger.warning(f'No Playbyplay data!')
        

        return static_data_extract


    def transform(self, data_extract):
        data_transformed = self.transformer.playbyplay(data_extract)
        self.logger.info(f'Transformed {len(data_transformed['PlayByPlay'])} actions')
        return data_transformed



    def load(self, data_transformed):
        data_loaded = self.destination.initiate_insert(data_transformed)
        return data_loaded