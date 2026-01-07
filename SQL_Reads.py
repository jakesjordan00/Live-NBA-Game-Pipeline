import pandas as pd
import pyodbc
def FirstIteration(nbaCursor: pyodbc.Cursor, gamesInProg: list):
    '''
Returns GameIDs of Games from list that already exist in the database

:param nbaCursor: pyodbc Cursor for SQL connection
:param dfScoreboard: Scoreboard DataFrame
'''
    query = f'''
select g.SeasonID, g.GameID, (select count(p.GameID) from PlayByPlay p where g.SeasonID = p.SeasonID and g.GameID = p.GameID) Actions
from Game g
where g.SeasonID = 2025 and g.GameID in({', '.join(str(s) for s in gamesInProg)})
'''
    nbaCursor.execute(query)
    existingGames = []
    for row in nbaCursor.fetchall():
        SeasonID = row[0]
        GameID = row[1]
        Actions = row[2]
        existingGames.append({
            'SeasonID': SeasonID,
            'GameID': GameID,
            'Actions': Actions
        })
    return existingGames