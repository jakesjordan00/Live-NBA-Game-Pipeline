import requests
import os
import json

class StaticDataConnector:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        pass
    
    def fetch(self):
        response = requests.get(self.pipeline.url)
        data = response.json()
        return data
    
    def fetch_file(self):
        dir_files = os.listdir('Refactor/connectors/fixtures')
        dir_files.sort(reverse=True)
        with open(f'Refactor/connectors/fixtures/{dir_files[1]}', 'r') as f:
            data = json.load(f)
        return data
        
