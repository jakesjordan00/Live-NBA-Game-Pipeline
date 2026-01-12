from GetScoreboard import GetTodaysScoreboard
from Directions import GetGamesInProgress, Wait
from SQL_Reads import FirstIteration
from GetDataNBA import GetBox, GetPlayByPlay, InsertBox, InsertPbp, UpdateBox
from FirstRunCoDriver import NewGameData, ExistingGameData

import time
print('-')

completedUpdatedGames = []


def MainFunction(iterations: int, dbGames: list, sender: str):
    '''
    Function that runs pipeline. Will get Box and/or PlayByPlay data
    
    :param iterations: How many times MainFunction has executed
    :type iterations: int

    :param dbGames: List of Game dictionaries. Contains SeasonID, GameID and a count of the PlayByPlay actions
    :type dbGames: list[dict]
    '''
    #Get the Games in Today's Scoreboard
    print('Getting Scoreboard...')
    dfScoreboard = GetTodaysScoreboard()

    #Using Today's Scoreboard, get the Games that are in progress
    gamesInProg, completedGames, halftimeGames = GetGamesInProgress(dfScoreboard, sender)
    #If game is completed, we should update it and check playbyplay one more time. After that, drop it.
    #^^^^ still need to implement as of 1:09am 1/9/26!
    #^ Should be implements....1/11/25. Just need to make sure its working as expected.

    print(f'{len(gamesInProg)} Games in progress')

    #Declare Box and PlayByPlay as none
    Box = None
    PlayByPlay = None

    #If we're on our first iteration or every fifth, see what games exist from the Scoreboard in the Db
    if iterations == 0:
        existingGames = FirstIteration(gamesInProg)
        existingGameIDs = list(g['GameID']for g in existingGames )
        notInDbGames = [game for game in gamesInProg if game not in existingGameIDs]
        if len(notInDbGames) > 0:
            dbGames.extend(NewGameData(notInDbGames))
        if len(existingGames) > 0:
            dbGames.extend(ExistingGameData(existingGames))
            

        test = 1
    elif iterations % 10 == 0:
        print('\n\n----------------------------Checking for any new Games...')
        existingGames = dbGames.copy()
        existingGames = RecurringFunction(iterations, existingGames, completedGames, dbGames, halftimeGames)
        existingGameIDs = list(g['GameID']for g in existingGames )
        notInDbGames = [game for game in gamesInProg if game not in existingGameIDs]
        for GameID in notInDbGames:
            print(f'\n{GameID}                                        MainFunction, in notInDbGames')
            Box = GetBox(GameID, 'MainFunction')
            if Box != None:
                boxStatus = InsertBox(Box)
                SeasonID = Box['Game']['SeasonID']
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
        existingGames = RecurringFunction(iterations, existingGames, completedGames, dbGames, halftimeGames)
        for game in existingGames:
            if game['GameID'] in completedUpdatedGames:
                dbGames.remove(game)
    iterations += 1
    return dbGames, iterations

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
    for game in existingGames:
        print(f'\n{game['GameID']}                                        RecurringFunction v{iterations}')
        if game['GameID'] in halftimeGames:
            print(f'     Halftime - skipping game for now.')
            continue
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
            Box = GetBox(game['GameID'], 'RecurringFunction')
            print('.', end='', flush=True)
            if Box != None:
                updateStatus = UpdateBox(Box)
            print(f'.{updateStatus}', end='', flush=True)
            test = 1
        
        if game['GameID'] in completedGames and game['GameID'] not in completedUpdatedGames:
            print(f'{game['GameID']} complete! Performing last upsert', end='', flush=True)
            Box = GetBox(game['GameID'], 'RecurringFunction')
            if Box != None:
                updateStatus = UpdateBox(Box)
            print(f'{updateStatus}')
            completedUpdatedGames.append(game['GameID'])
            existingGames.remove(game)
            #Update Box and Insert PlayByPlay, add game to completedUpdatedGames

    return existingGames



#When file is executed, it starts here
iterations = 0
dbGames, iterations = MainFunction(iterations, [], 'Default')
Wait(len(dbGames))

if iterations > 0:
    while True:
       dbGames, iterations = MainFunction(iterations, dbGames, 'Recurring')
       Wait(len(dbGames))

