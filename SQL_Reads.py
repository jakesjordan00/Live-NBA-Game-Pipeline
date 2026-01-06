import pandas as pd
import pyodbc
def FirstIteration(nbaCursor: pyodbc.Cursor, gamesInProg: list):
    '''
Returns GameIDs of Games from list that already exist in the database

:param nbaCursor: pyodbc Cursor for SQL connection
:param dfScoreboard: Scoreboard DataFrame
'''
    query = f'''
select GameID
from Game g
where g.SeasonID = 2025 and g.GameID in({', '.join(str(s) for s in gamesInProg)})
'''
    nbaCursor.execute(query)
    existingGames = list(row[0] for row in nbaCursor.fetchall())
    return existingGames