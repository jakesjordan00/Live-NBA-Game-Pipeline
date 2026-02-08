import config.api_map


class APIDataConnector:
    
    def __init__(self, pipeline):
        self.pipeline = pipeline
        pass


    def fetch(self):
        data_extract = ''
        return 