from urllib import response
import config.api_map
import requests
import json


class APIDataConnector:
    
    def __init__(self, pipeline):
        self.pipeline = pipeline
        pass
#test

    def fetch(self):
        response = requests.get(url=self.pipeline.api_map['url'], params=self.pipeline.api_map['params'], headers=self.pipeline.api_map['headers'])
        api_extract = response.json()
        return api_extract