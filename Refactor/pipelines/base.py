from abc import ABC, abstractmethod
from datetime import datetime
import logging
from typing import TypeVar, Generic
import polars as pl
import pandas as pd
from connectors.sql import SQLConnector 


T = TypeVar('T', pl.DataFrame, dict)

class Pipeline(ABC, Generic[T]):

    def __init__(self, pipeline_name):
        self.pipeline_name = pipeline_name
        self.logger = logging.getLogger(pipeline_name)
        self.destination = SQLConnector('JJsNBA')
        self.run_timestamp = None

    @abstractmethod
    def extract(self) -> T:
        pass
    
    @abstractmethod
    def transform(self, data: T) -> T:
        pass

    @abstractmethod
    def load(self, data: T) -> T:
        pass


    def run(self) -> dict:
        self.run_timestamp = datetime.now()
        self.logger.info(f'Starting {self.pipeline_name}')

        #Extract
        self.logger.info(f'Extracting...')
        data_extract = self.extract()

        #Transform
        self.logger.info(f'Transforming...')
        data_transformed = self.transform(data_extract)

        #Load
        self.logger.info(f'Loading...')
        data = self.load(data_transformed)

        return {
            'pipeline': self.pipeline_name,
            'status': 'success',
            'extracted': len(data_extract),
            'loaded': data,
            'timestamp': self.run_timestamp.isoformat()
        }