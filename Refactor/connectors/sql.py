from config.settings import DATABASES 
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text, Numeric

class SQLConnector:

    def __init__(self, database_name: str):
        if database_name not in DATABASES:
            raise ValueError(f'Unknown db!')
        
        self.database_name = database_name
        self.config = DATABASES[database_name]
        self.engine = self._create_engine()
        self.pyodbc = self._get_pyodbc_connection()


    def _create_engine(self):
        password = quote_plus(self.config['password'])
        connection_string = (
            f"mssql+pyodbc://{self.config['username']}:{password}"
            f"@{self.config['server']}/{self.config['database']}"
            f"?driver=ODBC+Driver+17+for+SQL+Server"
        )
        return create_engine(connection_string)
    
    def _get_pyodbc_connection(self) -> str:
        return (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.config['server']};"
            f"DATABASE={self.config['database']};"
            f"UID={self.config['username']};"
            f"PWD={self.config['password']}"
        )
    