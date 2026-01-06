from sqlalchemy import create_engine
import pyodbc
import urllib.parse
import os
import socket
from dotenv import load_dotenv

load_dotenv()
def GetEngineConnection():
    hostname = socket.gethostname()
    database = os.getenv('Database')
    if hostname != 'DESKTOP-F7FN836': #Laptop
        server = os.getenv('ServerIP')
        username = os.getenv('AdminUser')
        pw = os.getenv('AdminPass')
        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={pw}' 
    else:
        server = os.getenv('ServerLocal')
        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
    params = urllib.parse.quote_plus(connectionString)
    return create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


def GetPyodbcConnection():
    hostname = socket.gethostname()
    database = os.getenv('Database')
    if hostname != 'DESKTOP-F7FN836':
        server = os.getenv('ServerIP')
        username = os.getenv('AdminUser')
        pw = os.getenv('AdminPass')
        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={pw}' 
    else:
        server = os.getenv('ServerLocal')
        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
    return pyodbc.connect(connectionString)


nbaEngine = GetEngineConnection()
nbaConnection = GetPyodbcConnection()
nbaCursor = nbaConnection.cursor()