from urllib import response
import config.api_map
import requests
import json


class APIDataConnector:
    
    class Endpoint:
        def __init__(self, friendly_name: str, endpoint_name) -> None:
            self.name = friendly_name
            pass
        


    def __init__(self, pipeline):
        self.pipeline = pipeline
        pass
#test

    def fetch(self):
        response = requests.get(url=self.pipeline.api_map['url'], params=self.pipeline.api_map['params'], headers=self.pipeline.api_map['headers'])
        api_extract = response.json()
        return api_extract
    

    def _set_endpoints(self):
        self.player_stats = self.Endpoint('player_stats', 'leaguedashplayerstats')