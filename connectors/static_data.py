import logging
import requests
import os
import json

class StaticDataConnector:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        pass
    
    def fetch(self):
        try:
            response = requests.get(self.pipeline.url)
            data = response.json()
        except Exception as e:
            data = None
            logging.error(f'No data available. Error msg: {e}')
        return data
    
    def fetch_file(self):
        dir_files = os.listdir(self.pipeline.file_source)
        test = f'{self.pipeline.file_source}/{dir_files[self.pipeline.iterations]}'
        with open(f'{self.pipeline.file_source}/{dir_files[self.pipeline.iterations]}', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
        
