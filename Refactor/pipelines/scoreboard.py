import polars as pl
import pandas as pd
from pipelines.base import Pipeline
from connectors.static_data import StaticDataConnector


class ScoreboardPipeline(Pipeline):

    def __init__(self):
        super().__init__('scoreboard')

        self.url = 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'
        self.source = StaticDataConnector(self)


    def extract(self):
        data = self.source.fetch()
        bp = 'here'
        return data


    def transform(self, data):

        return data



    def load(self, data):

        pass