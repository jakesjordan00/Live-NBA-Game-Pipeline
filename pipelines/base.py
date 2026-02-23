from abc import ABC, abstractmethod
from datetime import datetime
import logging
import colorlog
from typing import TypeVar, Generic
import polars as pl
import pandas as pd
from connectors.sql import SQLConnector 


T = TypeVar('T', pl.DataFrame, dict)

class MillisecondFormatter(colorlog.ColoredFormatter):
    def formatTime(self, time_record, datefmt = None):
        time = datetime.fromtimestamp(time_record.created)
        if datefmt:
            new_time = time.strftime(datefmt)[:-3]
            return new_time
        return time.isoformat()

class Pipeline(ABC, Generic[T]):

    def __init__(self, pipeline_name):
        self.pipeline_name = pipeline_name
        self.logger = logging.getLogger(pipeline_name)
        if not logging.root.handlers:
            handler = colorlog.StreamHandler()
            handler.setFormatter(MillisecondFormatter(
                fmt='%(log_color)s%(asctime)s:  %(name)s ╍ %(levelname)s ╍ %(message)s',
                datefmt='%m/%d/%Y %H:%M:%S.%f',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'white',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red'
                }
            ))
            logging.root.setLevel(logging.INFO)
            logging.root.addHandler(handler)
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