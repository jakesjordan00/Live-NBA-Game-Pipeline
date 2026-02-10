import pandas as pd
import polars as pl

from pipelines.base import Pipeline
import config.api_map
from connectors.static_data import StaticDataConnector
from connectors.api_data import APIDataConnector
from transforms.transform_playbyplay import Transform

class PlayByPlayPipeline(Pipeline[dict]):
    def __init__(self, scoreboard_data, boxscore_data, start_action = 0):
        super().__init__('PlayByPlay')
        self.GameID = scoreboard_data['GameID']
        self.GameIDStr = scoreboard_data['GameIDStr']
        self.url = f'https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_{self.GameIDStr}.json'
        self.source = StaticDataConnector(self)
        self.api_source = APIDataConnector(self)
        self.api_map = config.api_map.nba_stats_endpoints['playbyplayv3']
        self.api_map['params']['GameID'] = self.GameIDStr
        
        self.transformer = Transform(self)
        self.start_action = start_action
        self.Data = {
            'scoreboard_data': scoreboard_data,
            'boxscore_data': boxscore_data
        }

    def extract(self):
        static_data_extract = self.source.fetch()
        # api_data_extract = self.api_source.fetch()  #Removing this on 2/10. Don't think we realistically need it.
        api_data_extract = None
        extract = {
            'static_data_extract': static_data_extract,
            'api_data_extract': api_data_extract
        }

        return extract


    def transform(self, data_extract):
        data_transformed = self.transformer.playbyplay(data_extract)
        return data_transformed



    def load(self, data_transformed):
        data_loaded = data_transformed
        return data_loaded