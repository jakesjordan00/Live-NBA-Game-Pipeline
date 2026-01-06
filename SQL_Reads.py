import pandas as pd

def FirstIteration(engine, gamesInProg):
    query = f'''
select GameID
from Game g
where g.SeasonID = 2025 and g.GameID in({', '.join(str(s) for s in gamesInProg)})
'''
    existingGames = pd.read_sql(query, engine).to_numpy().tolist()
    return existingGames