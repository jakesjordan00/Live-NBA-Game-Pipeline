import pandas as pd
import time


def GetGamesInProgress(dfScoreboard: pd.DataFrame):
    '''
Receives dfScoreboard\n
Returns a list of GameIDs of only those games in progress
    
:param dfScoreboard: Scoreboard DataFrame
'''
    gamesInProg = []
    completedGames = []
    for index, game in dfScoreboard.iterrows():
        GameID = game['GameID']
        if game['GameStatus'] == 1:
            continue
        # elif game['GameStatus'] != 1: #Testing
        elif game['GameStatus'] == 2: #Prod
            gamesInProg.append(GameID)
        else:
            completedGames.append(GameID)
    gamesInProg.sort()
    return gamesInProg, completedGames
            
        


def Wait(dbGamesLen: int):
    waitTime = 60 if dbGamesLen == 0 else 3
    checkpoints = [59, 58, 57, 56, 45, 30, 20, 15, 10, 5, 4, 3, 2, 1]
    
    printStr = f'Waiting {waitTime} seconds...'
    print('-')
    print(printStr, end='\r')
    
    remaining = waitTime
    for checkpoint in checkpoints:
        if remaining > checkpoint:
            time.sleep(remaining - checkpoint)
            remaining = checkpoint
            printStr = f'{printStr}{checkpoint}...' if checkpoint != 56 else f'{printStr}{checkpoint}......'
            print(printStr, end='\r')
    
    time.sleep(remaining)
    print(f'{printStr}\nDone waiting!\n-') 
