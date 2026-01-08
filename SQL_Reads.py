import pandas as pd
import pyodbc
from DBConfig import nbaConnection, nbaCursor, nbaEngine
def FirstIteration(gamesInProg: list) -> list[dict]:
    '''
Returns a list of Game dictionaries (dbGames/existingGames). Contains SeasonID, GameID and a count of the PlayByPlay actions

:param nbaCursor: pyodbc Cursor for SQL connection
:param gamesInProg: List of GameIDs of Games that are in progress
'''

    query = f'''
select g.SeasonID, g.GameID, (select count(p.GameID) from PlayByPlay p where g.SeasonID = p.SeasonID and g.GameID = p.GameID) Actions
from Game g
where g.SeasonID = 2025 and g.GameID in({', '.join(str(s) for s in gamesInProg)})
'''.replace("in()", "in('')")
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