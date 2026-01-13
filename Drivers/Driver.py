import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from GetScoreboard import GetTodaysScoreboard
from Directions import GetGamesInProgress, Wait
from SQL_Reads import FirstIteration
from GetDataNBA import GetBox, GetPlayByPlay, InsertBox, InsertPbp, UpdateBox
from FirstRunCoDriver import NewGameData, ExistingGameData

import time
print('-')

programMap = ''
completedUpdatedGames = []


def MainFunction(iterations: int, dbGames: list, sender: str, programMap: str):
    '''
    Function that runs pipeline. Will get Box and/or PlayByPlay data
    
    :param iterations: How many times MainFunction has executed
    :type iterations: int

    :param dbGames: List of Game dictionaries. Contains SeasonID, GameID and a count of the PlayByPlay actions
    :type dbGames: list[dict]
    '''
    '''
    -|
      ->
    '''
    programMap += 'Driver.MainFunction ➡️ \n'
    #Get the Games in Today's Scoreboard
    print('Getting Scoreboard...')
    dfScoreboard, programMap = GetTodaysScoreboard(programMap)

    #Using Today's Scoreboard, get the Games that are in progress
    halftimeGames, allStartTimes, gamesInProgDict, completedGamesDict, programMap = GetGamesInProgress(dfScoreboard, sender, programMap)

    print(f'{len(gamesInProgDict)} Games in progress')

    #Declare Box and PlayByPlay as none
    Box = None
    PlayByPlay = None

    #If we're on our first iteration or every fifth, see what games exist from the Scoreboard in the Db
    if iterations == 0:
        existingGames, programMap = FirstIteration(gamesInProgDict, programMap)
        existingGameIDs = list(g['GameID']for g in existingGames )
        notInDbGames = [game for game in gamesInProgDict if game['GameID'] not in existingGameIDs]
        if len(notInDbGames) > 0:
            newDbGames, programMap = NewGameData(notInDbGames, programMap)
            dbGames.extend(newDbGames)
        if len(existingGames) > 0:
            existingDbGames, programMap = ExistingGameData(existingGames, programMap)
            dbGames.extend(existingDbGames)
            

        test = 1
    elif iterations % 10 == 0:
        print('\n\n----------------------------Checking for any new Games...')
        existingGames = dbGames.copy()
        existingGames = RecurringFunction(iterations, existingGames, completedGamesDict, dbGames, halftimeGames)
        existingGameIDs = list(g['GameID']for g in existingGames )
        notInDbGames = [game for game in gamesInProgDict if game['GameID'] not in existingGameIDs]
        for GameID in notInDbGames:
            print(f'\n{GameID}                                        MainFunction, in notInDbGames')
            Box = GetBox(GameID, 'MainFunction')
            if Box != None:
                boxStatus = InsertBox(Box)
                SeasonID = Box['Game']['SeasonID']
                HomeID = Box['Game']['HomeID']
                AwayID = Box['Game']['AwayID']
                # PlayByPlay = GetPlayByPlay(SeasonID, GameID, HomeID, AwayID, 0, 'MainFunction')
                PlayByPlay = GetPlayByPlay(SeasonID, GameID, 0, 'MainFunction')
                pbpStatus = InsertPbp(PlayByPlay)
                dbGames.append({
                    'SeasonID': SeasonID,
                    'GameID': GameID,
                    'Box': Box,
                    'PlayByPlay': PlayByPlay,
                    'Actions': len(PlayByPlay)
                })
        
        test = 1
    else:
        existingGames = dbGames.copy()
        existingGames = RecurringFunction(iterations, existingGames, completedGamesDict, dbGames, halftimeGames)
        for game in existingGames:
            if game['GameID'] in completedUpdatedGames:
                dbGames.remove(game)
    iterations += 1
    return dbGames, iterations, allStartTimes, programMap

def RecurringFunction(iterations: int, existingGames: list, completedGames: list, dbGames, halftimeGames: list):
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
    programMap += 'Driver.RecurringFunction ➡️ '
    for game in existingGames:
        print(f'\n{game['GameID']}                                        RecurringFunction v{iterations}')
        if game['GameID'] in halftimeGames:
            print(f'     Halftime - skipping game for now.')
            continue
        HomeID = game['Box']['Game']['HomeID']
        AwayID = game['Box']['Game']['AwayID']
        # PlayByPlay = GetPlayByPlay(game['SeasonID'], game['GameID'], HomeID, AwayID, game['Actions'], 'RecurringFunction')
        PlayByPlay = GetPlayByPlay(game['SeasonID'], game['GameID'], game['Actions'], 'RecurringFunction')
        PlayByPlayFull = game['PlayByPlay']
        PlayByPlayFull.extend(PlayByPlay)
        game['PlayByPlay'] = PlayByPlayFull
        game['Actions'] = len(PlayByPlayFull)
        if len(PlayByPlay) > 0:
            pbpStatus = InsertPbp(PlayByPlay)
            test = 1
        if iterations % 12 == 0:
            print(f'  Updating Game, GameExt, TeamBox and PlayerBox.', end='', flush=True)
            Box, programMap = GetBox(game['GameID'], 'RecurringFunction', programMap)
            print('.', end='', flush=True)
            if Box != None:
                updateStatus, programMap = UpdateBox(Box, programMap)
            print(f'.{updateStatus}', end='', flush=True)
            test = 1
        
        if game['GameID'] in completedGames and game['GameID'] not in completedUpdatedGames:
            print(f'{game['GameID']} complete! Performing last upsert', end='', flush=True)
            Box, programMap = GetBox(game['GameID'], 'RecurringFunction', programMap)
            if Box != None:
                updateStatus = UpdateBox(Box, programMap)
            print(f'{updateStatus}')
            completedUpdatedGames.append(game['GameID'])
            existingGames.remove(game)
            #Update Box and Insert PlayByPlay, add game to completedUpdatedGames

    return existingGames



#When file is executed, it starts here
iterations = 0
dbGames, iterations, allStartTimes, programMap = MainFunction(iterations, [], 'Default', programMap)
programMap = Wait(len(dbGames), allStartTimes)

if iterations > 0:
    while True:
       dbGames, iterations, allStartTimes, programMap = MainFunction(iterations, dbGames, 'Recurring', programMap)
       programMap = Wait(len(dbGames), allStartTimes)

