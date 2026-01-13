import pandas as pd
from datetime import datetime, timedelta
import time


def GetGamesInProgress(dfScoreboard: pd.DataFrame, sender: str):
    '''
Receives dfScoreboard\n
Returns a list of GameIDs of only those games in progress
    
:param dfScoreboard: Scoreboard DataFrame
:type dfScoreboard: pd.DataFrame
'''
    gamesInProg = []
    gamesInProgDict = []
    completedGames = []
    halftimeGames = []
    allStartTimes = []
    for index, game in dfScoreboard.iterrows():
        GameID = game['GameID']
        gameStatusText = game['GameStatusText']
        if game['GameStatus'] == 1:
            allStartTimes.append(datetime.strptime(game['GameEt'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(minutes=10))
            continue
        # elif game['GameStatus'] != 1: #Testing
        elif game['GameStatus'] == 2: #Prod
            gamesInProg.append(GameID)
        else:
            completedGames.append(GameID)        
        if sender == 'Recurring' and gameStatusText == 'Half':
            halftimeGames.append(GameID)
    gamesInProg.sort()
    allStartTimes.sort()
    return gamesInProg, completedGames, halftimeGames, allStartTimes
            
        


def Wait(dbGamesLen: int, allStartTimes: list):
    if len(allStartTimes) > 0:
        nextGameTip =(allStartTimes[0] - datetime.now()).seconds
    else:
        nextGameTip = 60
    waitTime = nextGameTip if dbGamesLen == 0 else 3
    if waitTime > 3:
        checkpoints = [waitTime-1, waitTime-2, waitTime-3, waitTime-4, int(waitTime * .75), int(waitTime/2), int(waitTime/3), int(waitTime/4), int(waitTime/6), int(waitTime/10), 5, 4, 3, 2, 1]
    else:
        checkpoints = [3, 2, 1]
    
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
    print(f'{printStr}Done waiting!\n-') 
