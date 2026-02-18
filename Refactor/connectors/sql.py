from config.settings import DATABASES 
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text, Numeric
from transforms.stint_processor import StintResult
import pyodbc
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class SQLConnector:

    def __init__(self, database_name: str):
        if database_name not in DATABASES:
            raise ValueError(f'Unknown db!')
        
        self.database_name = database_name
        self.config = DATABASES[database_name]
        self.tables = self.config['Tables']
        self.engine = self._create_engine()
        self.pyodbc_connection = pyodbc.connect(self._get_pyodbc_connection())
        self.logger = logging.getLogger('SQLConnector')
        


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
    
    def initiate_insert(self, data_transformed: dict):
        transformed_dicts = []
        
        for table_name, data in data_transformed.items():
            if type(data) == dict:
                self.checked_insert(table_name, [data])

            elif type(data) == list and table_name != 'PlayByPlay':
                self.checked_insert(table_name, data)

            elif type(data) == list and table_name == 'PlayByPlay':
                self.unchecked_insert(table_name, data)
                
            elif type(data) == StintResult:
                self.checked_insert('jjs.Stint', data.Stint)
                self.checked_insert('jjs.StintPlayer', data.StintPlayer)

        return data_transformed #change this to some sort of logging mechanism
    


    def checked_insert(self, table_name: str, data: list):
        sql_table = self.tables[table_name]
        insert_string = f'''
if not exists(
select 1 
from {table_name}
where {' = ? and '.join(sql_table['keys'])} = ?
)
begin
insert into {table_name}({', '.join(sql_table['columns'])})
values({', '.join(['?'] * len(sql_table['columns']))})
end

'''
        try:
            params = [self.dict_to_params(data_dict, sql_table['keys'] + sql_table['columns']) for data_dict in data]
            cursor = self.pyodbc_connection.cursor()
            cursor.fast_executemany = True
            cursor.executemany(insert_string, params)
            self.logger.info({
                'Table': table_name,
                'rows': len(data)
            })
            cursor.commit()
        except Exception as e:
            self.logger.error({
                'Table': table_name,
                'err_msg': e
            })
    

    def unchecked_insert(self, table_name: str, data: list):
        sql_table = self.tables[table_name]
        insert_string = f'''
insert into {table_name}({', '.join(sql_table['columns'])})
values({', '.join(['?'] * len(sql_table['columns']))})
        '''
        try:
            params = [self.dict_to_params(data_dict, sql_table['keys'] + sql_table['columns']) for data_dict in data]
            cursor = self.pyodbc_connection.cursor()
            cursor.executemany(insert_string, params)
            cursor.commit()
            self.logger.info({
                'Table': table_name,
                'rows': len(data)
            })
        except Exception as e:
            self.logger.error({
                'Table': table_name,
                'err_msg': e
            })

    def cursor_query(self, table_name: str, keys: dict):
        sql_table = self.tables[table_name]
        query = sql_table['check_query'].replace('season_id', keys['season_id']).replace('game_id', keys['game_id'])
        try:
            cursor = self.pyodbc_connection.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            actions = row[0] if row else 0
        except Exception as e:
            test = 1
        
        return actions

        







    def dict_to_params(self, d: dict, keys: list) -> tuple:
        return tuple(d[k.replace('[', '').replace(']', '')] for k in keys)