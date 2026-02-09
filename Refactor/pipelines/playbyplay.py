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
        extract = {
            'data_extract': data_extract,
            'api_data_extract': api_data_extract
        }

        tde = data_extract['game']['actions']
        tad = api_data_extract['game']['actions']

        test_tde = pd.DataFrame(tde)
        test_tad = pd.DataFrame(tad)
        test_tad['actionType'] = test_tad['actionType'].str.lower()


        test_left = test_tde.merge(test_tad[['actionType', 'personId', 'clock', 'period', 'description', 'actionNumber']], on=['actionType', 'personId', 'clock', 'period'], how='left', suffixes=('', '_api'))
                

        mask_out = (test_left['actionType'] == 'substitution')
        sub_out = test_left[[
            'actionNumber','period','clock', 
            'personId', 'playerName', 'playerNameI', 
            'description', 'description_api',
            'actionType', 'subType',
            'scoreHome', 'scoreAway',
        ]][mask_out]

        sub_out['description_api'] = sub_out['description_api'].fillna('')
        sub_out['description_sub_in'] = sub_out.apply(
            lambda row: (
                row['description_api']
                .replace(':', ' in:')
                .replace(' FOR ', '')
                .replace(row['playerName'], '')
            ), 
            axis=1
        )        
        
        mask_in = (test_left['actionType'] == 'substitution') & (test_left['subType'] == 'in')
        sub_in = test_left[[
            'actionNumber','period','clock', 
            'personId', 'playerName', 'playerNameI', 
            'description',
            'actionType', 'subType',
            'scoreHome', 'scoreAway',
        ]][mask_in]
        sub_in['description_sub_in'] = sub_in.apply(
            lambda row:(
            row['description'].replace(row['playerNameI'], row['playerName'])
            ),
            axis = 1
        )


        combined = sub_out.merge(sub_in, how='left', on = ['period','clock', 'scoreHome', 'scoreAway', 'actionType', 'description_sub_in']
                                 , suffixes=('_dfOut', '_dfIn'))
        combined['description_dfIn'] = combined['description_dfIn'].fillna('')

        print(f'Sub out: {sub_out['description_sub_in'].iloc[0]}')
        print(f'Sub in:  {sub_in['description_sub_in'].iloc[0]}')


        matched_sub_in = combined[combined['actionNumber_dfIn'].notna()]['actionNumber_dfIn'].values
        combined = combined[~(
            (combined['subType_dfOut'] == 'in') & 
            (combined['actionNumber_dfIn'].isna()) & 
            (combined['actionNumber_dfOut'].isin(matched_sub_in))
        )]

        bp = 'here'
        for i, row in combined.iterrows():
            if row['actionType'] == 'substitution':
                print(f'{row['actionNumber_dfOut']} - {row['description_dfOut']}'
                      + f'{(35 - len(row['description_dfOut'])) * ' '}'
                      + f'{row['actionNumber_dfIn']} - {row['description_dfIn']}'
                      + f'{(35 - len(row['description_dfIn'])) * ' '}'
                      + f'API: {row['description_api']}')
                


        bp = 'here'

        return extract


    def transform(self, data_extract):
        data_transformed = self.transformer.playbyplay(data_extract)
        return data_transformed



    def load(self, data_transformed):
        data_loaded = data_transformed
        return data_loaded