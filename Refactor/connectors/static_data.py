import requests




class StaticDataConnector:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        pass
    
    def fetch(self):
        response = requests.get(self.pipeline.url)
        data = response.json()
        return data
        
