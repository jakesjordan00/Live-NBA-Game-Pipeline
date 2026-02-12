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
        pipeline = self.pipeline
        dir_files = os.listdir(self.pipeline.file_source)
        with open(f'{self.pipeline.file_source}/{dir_files[0]}', 'r') as f:
            data = json.load(f)
        return data
        
