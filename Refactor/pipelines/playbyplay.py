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
        data_extract = self.source.fetch()
        api_data_extract = self.api_source.fetch()

        tde = data_extract['game']['actions']
        tad = api_data_extract['game']['actions']

        test_tde = pd.DataFrame(tde)
        test_tad = pd.DataFrame(tad)
        test_tad['actionType'] = test_tad['actionType'].str.lower()

        test_left = test_tde.merge(test_tad[['actionType', 'personId', 'clock', 'period', 'description']], on=['actionType', 'personId', 'clock', 'period'], how='left', suffixes=('', '_api'))
        print(test_left['description_api'].values)
        
        for i, row in test_left.iterrows():
            if row['actionType'] == 'substitution':
                test = len(row['description'])
                print(f'{row['description']}{(100 - test) * ' '}{row['description_api']}')
                bp = 'here'



        return data_extract


    def transform(self, data_extract, api_data_extract):
        data_transformed = self.transformer.playbyplay(data_extract, api_data_extract)
        return data_transformed



    def load(self, data):
        pass