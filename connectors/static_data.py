import logging
import requests
import os
import json

class StaticDataConnector:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        pass
    
    def fetch(self) -> dict:
        '''
        Fetches data from NBA's static data feeds
        
        :return data (dict): Dict containing subdictionaries. Usually a 'meta' dict and then the dict that contains our data

           - 'scoreboard', 'game'
           
        '''
        try:
            response = requests.get(self.pipeline.url)
            data = response.json()
        except Exception as e:
            data = {}
            logging.error(f'No data available. Error msg: {e}')
        return data
    
    def fetch_file(self):
        dir_files = os.listdir(self.pipeline.file_source)
        test = f'{self.pipeline.file_source}/{dir_files[0]}'
        with open(f'{self.pipeline.file_source}/{dir_files[0]}', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
        
