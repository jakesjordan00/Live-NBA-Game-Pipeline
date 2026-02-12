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
        dir_files = os.listdir('Refactor/connectors/fixtures')
        dir_files.sort(reverse=True)
        with open(f'Refactor/connectors/fixtures/{dir_files[0]}', 'r') as f:
            data = json.load(f)
        return data
        
