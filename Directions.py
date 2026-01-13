import pandas as pd
from datetime import datetime, timedelta
import time


def GetGamesInProgress(dfScoreboard: pd.DataFrame, sender: str, programMap: str):
    '''
Receives dfScoreboard\n
Returns a list of GameIDs of only those games in progress
    
:param dfScoreboard: Scoreboard DataFrame
:type dfScoreboard: pd.DataFrame
'''
    programMap += 'GetGamesInProgress ➡️ '
    gamesInProgDict = []
    completedGamesDict = []
    gamesInProg = []
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
            programMap += 'GameDictionary ➡️ '
            gamesInProgDict.append(GameDictionary(game))
        else:
            completedGames.append(GameID)  
            programMap += 'GameDictionary ➡️ '
            completedGamesDict.append(GameDictionary(game))      
        if sender == 'Recurring' and gameStatusText == 'Half':
            halftimeGames.append(GameID)
    gamesInProg.sort()
    allStartTimes.sort()

    return halftimeGames, allStartTimes, gamesInProgDict, completedGamesDict, programMap
    return gamesInProg, completedGames, halftimeGames, allStartTimes, gamesInProgDict, completedGamesDict, programMap

        


def GameDictionary(game: dict):
    GameID = game['GameID']
    gameStatusText = game['GameStatusText']

    Label= game['GameLabel'] if game['GameLabel'] != '' else None
    LabelDetail =  game['GameSubLabel'] if game['GameSubLabel'] != '' else None
    SubType =  game['GameSubtype'] if game['GameSubtype'] != '' else None
    SeriesGameNumber =  int(game['SeriesGameNumber']) if game['SeriesGameNumber'] != '' else None
    SeriesText =  game['SeriesText'] if game['SeriesText'] != '' else None
    a = 1
    return{
    'GameID': GameID,
    'HomeTeam': {
        'teamId': game['HomeTeam']['teamId'],
        'wins': game['HomeTeam']['wins'],
        'losses': game['HomeTeam']['losses'],
        'seed': game['HomeTeam']['seed']
    },
    'AwayTeam': {
        'teamId': game['AwayTeam']['teamId'],
        'wins': game['AwayTeam']['wins'],
        'losses': game['AwayTeam']['losses'],
        'seed': game['AwayTeam']['seed']
    },    
    'Status': game['GameStatus'],
    'StatusText': gameStatusText,
    'Label': Label,
    'LabelDetail': LabelDetail,
    'SubType': SubType,
    'SeriesGameNumber': SeriesGameNumber,
    'SeriesText': SeriesText,

    }


def Wait(dbGamesLen: int, allStartTimes: list, programMap: str):
    programMap += 'Wait ➡️ '
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
    return programMap