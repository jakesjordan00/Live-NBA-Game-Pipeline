import pandas as pd



def GetGamesInProgress(dfScoreboard: pd.DataFrame):
    '''
Receives dfScoreboard\n
Returns only those games in progress
    
:param dfScoreboard: Scoreboard DataFrame
'''
    gamesInProg = []
    for index, game in dfScoreboard.iterrows():
        GameID = game['GameID']
        if game['GameStatus'] == 1:
            continue
        else:
            gamesInProg.append(GameID)
    gamesInProg.sort()
    return gamesInProg
            
        