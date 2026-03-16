from pipelines import Pipeline
from connectors import StaticDataConnector, APIDataConnector
from transforms.transform_api_data import Transform
from datetime import datetime
import polars as pl

SCHEMA_CONFIG = {
    'adv': 'Advanced',
    'misc': 'Misc',
    'scoring': 'Scoring',
    'usage': 'Usage',
    'def': 'Defense',
    'violations': 'Violations'
}


class AdvancedStatsPipeline(Pipeline):
    def __init__(self, date_data: dict, schema: str):
        self.pipeline_name = 'advanced_stats'
        self.tag = 'advancedStats'
        self.schema = schema
        super().__init__(self.pipeline_name, self.tag, 'NBA API')
        self.schedule_source = StaticDataConnector(self)
        self.url = self.schedule_source.schedule        
        self.source = APIDataConnector(self)
        self.date = date_data['date']
        self.data = date_data['games']
        self.source.player_stats.params = {
            **self.source.player_stats.params,
            'MeasureType': SCHEMA_CONFIG[self.schema],
            'DateFrom': self.date,
            'DateTo': self.date
        }


        self.transformer = Transform(self)
        # self.destination.check_tables()

    def extract(self):
        self.logger.info(f'Extracting data from {self.date}')
        data_extract = self.source.fetch(self.source.player_stats)
        return data_extract
    

    def transform(self, data_extract):
        data_transformed = self.transformer.start_transform(data_extract)
        return data_transformed

    def load(self, data_transformed):
        data_loaded = self.destination.checked_upsert(table_name=f'{self.schema}.PlayerBox', data=data_transformed)
        return data_loaded



