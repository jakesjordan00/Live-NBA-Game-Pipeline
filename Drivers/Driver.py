import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from GetScoreboard import GetTodaysScoreboard
from Directions import GetGamesInProgress, Wait
from SQL_Reads import FirstIteration
from GetDataNBA import GetBox, GetPlayByPlay, InsertBox, InsertPbp, UpdateBox
from FirstRunCoDriver import NewGameData, ExistingGameData
import time
from datetime import datetime
from ProgramMapHelper import level, DisplayProgramMap, DisplayFullProgramMap
print('-')
programMap = ''
fullProgramMap = []
completedUpdatedGames = []


def MainFunction(iterations: int, dbGames: list, sender: str, programMap: str):
    '''
    Function that runs pipeline. Will get Box and/or PlayByPlay data
    
    :param iterations: How many times MainFunction has executed
    :type iterations: int

    :param dbGames: List of Game dictionaries. Contains SeasonID, GameID and a count of the PlayByPlay actions
    :type dbGames: list[dict]
    '''
    underscore = '_' * 70
    programMap = f'{underscore}\nDriver.MainFunction                                                                                                    v{iterations+1}'
    #Get the Games in Today's Scoreboard
    print('Getting Scoreboard...')
    dfScoreboard, programMap = GetTodaysScoreboard(programMap, iterations)

    #Using Today's Scoreboard, get the Games that are in progress
    halftimeGames, allStartTimes, gamesInProgDict, completedGamesDict, games, programMap = GetGamesInProgress(dfScoreboard, sender, programMap)
    yetToStart = [time for time in allStartTimes if time >= datetime.now()]
    yetToStartCount = len(yetToStart)
    yetToStart = 'No more games tonight.' if yetToStartCount == 0 else f'{yetToStartCount} games yet to start.'
    print(f'''-     -     -     -     -     -     -
   -    -    -    -    -    -    -
-     -     -     -     -     -     -
{games} Games this evening.
-
{len(gamesInProgDict)} Games are in progress.
-
{len(completedGamesDict)} Games are completed.
-
{yetToStart}
-     -     -     -     -     -     -
   -    -    -    -    -    -    -
-     -     -     -     -     -     -''')

    #Declare Box and PlayByPlay as none
    Box = None
    PlayByPlay = None

    #If we're on our first iteration or every fifth, see what games exist from the Scoreboard in the Db
    if iterations == 0:
        if len(gamesInProgDict) > 0:
            existingGames, programMap = FirstIteration(gamesInProgDict, programMap)    
            existingGameIDs = list(g['GameID']for g in existingGames )
            notInDbGames = [game for game in gamesInProgDict if game['GameID'] not in existingGameIDs]
            if len(notInDbGames) > 0:
                newDbGames, programMap = NewGameData(notInDbGames, programMap, 'MainFunction')
                dbGames.extend(newDbGames)
            if len(existingGames) > 0:
                existingDbGames, programMap = ExistingGameData(existingGames, programMap)
                dbGames.extend(existingDbGames)
    
        if len(completedGamesDict) > 0:
            existingCompletedGames, programMap = FirstIteration(completedGamesDict, programMap)
            
            existingCompletedGameIDs = list(g['GameID']for g in existingCompletedGames )
            notInDbCompletedGames = [game for game in completedGamesDict if game['GameID'] not in existingCompletedGameIDs]
            if len(notInDbCompletedGames) > 0:
                newDbCompletedGames, programMap = NewGameData(notInDbCompletedGames, programMap, 'MainFunction')
            if len(existingCompletedGames) > 0:
                existingCompletedDbGames, programMap = ExistingGameData(existingCompletedGames, programMap)
            

        test = 1
    elif iterations % 10 == 0:
        print('\n\n----------------------------Checking for any new Games...')
        existingGames = dbGames.copy()
        existingGames, programMap = RecurringFunction(iterations, existingGames, completedGamesDict, dbGames, halftimeGames, programMap)
        existingGameIDs = list(g['GameID']for g in existingGames )
        notInDbGames = [game for game in gamesInProgDict if game['GameID'] not in existingGameIDs]
        for game in notInDbGames:
            GameID = game['GameID']
            print(f'\n{GameID}                                        MainFunction, in notInDbGames')
            Box, programMap = GetBox(GameID, game, 'MainFunction', programMap, '')
            if Box != None:
                boxStatus, programMap = InsertBox(Box, programMap)
                SeasonID = Box['Game']['SeasonID']
                HomeID = Box['Game']['HomeID']
                AwayID = Box['Game']['AwayID']
                # PlayByPlay = GetPlayByPlay(SeasonID, GameID, HomeID, AwayID, 0, 'MainFunction')
                PlayByPlay, programMap = GetPlayByPlay(SeasonID, GameID, 0, 'MainFunction', programMap)
                pbpStatus, programMap = InsertPbp(PlayByPlay, programMap, 'MainFunction')
                dbGames.append({
                    'SeasonID': SeasonID,
                    'GameID': GameID,
                    'Box': Box,
                    'PlayByPlay': PlayByPlay,
                    'Actions': len(PlayByPlay),
                    'Data': game
                })
        lastLine = programMap.split('\n')[-1]
        programMap += f'╭╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╯' if lastLine == '' else f'\n╭╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╯'
        
        test = 1
    else:
        existingGames = dbGames.copy()
        existingGames, programMap = RecurringFunction(iterations, existingGames, completedGamesDict, dbGames, halftimeGames, programMap)
        lastLine = programMap.split('\n')[-1]
        programMap += f'╭╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╯' if lastLine == '' else f'\n╭╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╯'
        for game in existingGames:
            if game['GameID'] in completedUpdatedGames:
                dbGames.remove(game)
    iterations += 1
    return dbGames, iterations, allStartTimes, programMap

def RecurringFunction(iterations: int, existingGames: list, completedGames: list, dbGames, halftimeGames: list, programMap: str):
    '''
    Docstring for RecurringFunction
    
    :param iterations: How many times MainFunction has executed
    :type iterations: int

    :param existingGames:
        List of Game dictionaries:

        - Should be the same as dbGames
        - Contains SeasonID, GameID
        - Includes a count of the PlayByPlay actions
    :type existingGames: list[dict]
    
    :param completedGames: Games that are have a GameStatus value of 3 from scoreboard
    :type iterations: list
    '''
    # programMap += f'\n╰╼╾╼Driver.RecurringFunction╼╮\n                             ╞╾'
    
    programMap += f'\n╰╼╾╼Driver.RecurringFunction╼╮\n'
    lastLine = programMap.split('\n')[-2]
    lastLen = len(lastLine) - 1
    mapPole = f'{lastLen * ' '}│'
    if len(existingGames) > 0:
        programMap += f'{(lastLen - 8) * ' '}{existingGames[0]['GameID']}╞╾'
    for i, game in enumerate(existingGames):
        if i > 0:
            programMap += f'\n{(lastLen - 8) * ' '}{game['GameID']}╞╾'
       
        print(f'\n{game['GameID']}                                        RecurringFunction v{iterations}')



        if game['GameID'] in halftimeGames:
            programMap += f'╮ Halftime - skipped for the time being'
            programMap += f'\n{(lastLen) * ' '}╞╾╯'            
            print(f'     Halftime - skipping game for now.')
            continue
        HomeID = game['Box']['Game']['HomeID']
        AwayID = game['Box']['Game']['AwayID']
        PlayByPlay, programMap = GetPlayByPlay(game['SeasonID'], game['GameID'], game['Actions'], 'RecurringFunction', programMap)

        PlayByPlayFull = game['PlayByPlay']
        PlayByPlayFull.extend(PlayByPlay)
        game['PlayByPlay'] = PlayByPlayFull
        game['Actions'] = len(PlayByPlayFull)
        if len(PlayByPlay) > 0:
            pbpStatus, programMap = InsertPbp(PlayByPlay, programMap, 'RecurringFunction')
            test = 1
        else:            
            bp = 'here'

        if iterations % 12 == 0:
            print(f'  Updating Game, GameExt, TeamBox and PlayerBox.', end='', flush=True)
            
            lastLine = programMap.split('\n')[-1]
            polePosition = lastLine.index('╞')
            programMap += f'\n{lastLine[:polePosition]}╞╾'
            Box, programMap = GetBox(game['GameID'], game['Data'], 'RecurringFunction', programMap, mapPole)
            print('.', end='', flush=True)
            if Box != None:
                updateStatus, programMap = UpdateBox(Box, programMap)
            print(f'.{updateStatus}', end='', flush=True)
        if game['GameID'] in completedGames and game['GameID'] not in completedUpdatedGames:
            print(f'{game['GameID']} complete! Performing last upsert', end='', flush=True)
            Box, programMap = GetBox(game['GameID'], game['Data'], 'RecurringFunction', programMap, mapPole)
            if Box != None:
                updateStatus, programMap = UpdateBox(Box, programMap)
            print(f'{updateStatus}')
            completedUpdatedGames.append(game['GameID'])
            existingGames.remove(game)
            #Update Box and Insert PlayByPlay, add game to completedUpdatedGames

    return existingGames, programMap



#When file is executed, it starts here
iterations = 0
dbGames, iterations, allStartTimes, programMap = MainFunction(iterations, [], 'Default', programMap)

programMap = Wait(len(dbGames), allStartTimes, programMap, 'MainFunction', fullProgramMap)


    # DisplayProgramMap(programMap, 'Wait')
    # bp = 'here'
if iterations > 0:
    while True:
       dbGames, iterations, allStartTimes, programMap = MainFunction(iterations, dbGames, 'Recurring', programMap)
       programMap = Wait(len(dbGames), allStartTimes, programMap, 'RecurringFunction', fullProgramMap)

