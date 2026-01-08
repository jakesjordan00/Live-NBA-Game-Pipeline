from GetScoreboard import GetTodaysScoreboard
from Directions import GetGamesInProgress, Wait
from SQL_Reads import FirstIteration
from GetDataNBA import GetBox, GetPlayByPlay, InsertBox, InsertPbp, UpdateBox

import time
print('-')




def MainFunction(iterations: int, dbGames: list):
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
    gamesInProg, completedGames = GetGamesInProgress(dfScoreboard)
    print(f'{len(gamesInProg)} Games in progress')

    #Declare Box and PlayByPlay as none
    Box = None
    PlayByPlay = None

    #If we're on our first iteration or every fifth, see what games exist from the Scoreboard in the Db
    if iterations == 0:
        existingGames = FirstIteration(gamesInProg)
        existingGameIDs = list(g['GameID']for g in existingGames )
        notInDbGames = [game for game in gamesInProg if game not in existingGameIDs]
        for GameID in notInDbGames:
            print(f'\n{GameID}                                        MainFunction, in notInDbGames')
            Box = GetBox(GameID)
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

        inDbGames = [game for game in gamesInProg if game in existingGameIDs]
        for game in existingGames:
            print(f'\n{game['GameID']}                                        MainFunction, in existingGames')
            Box = Box if Box != None else GetBox(game['GameID'])
            PlayByPlay = PlayByPlay if PlayByPlay != None else GetPlayByPlay(game['SeasonID'], game['GameID'], 0, 'MainFunctionAlt')
            dbGames.append({
                'SeasonID': game['SeasonID'],
                'GameID': game['GameID'],
                'Box': Box,
                'PlayByPlay': PlayByPlay,
                'Actions': game['Actions']
            })
            

        test = 1
    elif iterations % 10 == 0:
        print('\n\n----------------------------Checking for any new Games...')
        existingGames = dbGames.copy()
        existingGames = RecurringFunction(iterations, existingGames)
        existingGameIDs = list(g['GameID']for g in existingGames )
        notInDbGames = [game for game in gamesInProg if game not in existingGameIDs]
        for GameID in notInDbGames:
            print(f'\n{GameID}                                        MainFunction, in notInDbGames')
            Box = GetBox(GameID)
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
    #If not, 
        existingGames = dbGames.copy()
        existingGames = RecurringFunction(iterations, existingGames)
    iterations += 1
    return dbGames, iterations

def RecurringFunction(iterations: int, existingGames: list):
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
    '''
    for game in existingGames:
        print(f'\n{game['GameID']}                                        RecurringFunction v{iterations}')
        PlayByPlay = GetPlayByPlay(game['SeasonID'], game['GameID'], game['Actions'], 'RecurringFunction')
        PlayByPlayFull = game['PlayByPlay']
        PlayByPlayFull.extend(PlayByPlay)
        game['PlayByPlay'] = PlayByPlayFull
        game['Actions'] = len(PlayByPlayFull)
        if len(PlayByPlay) > 0:
            # pbpStatus = InsertPbp(PlayByPlay)
            test = 1
        if iterations % 25 == 1: #change that back to == 0
            print(f'  Updating Game, GameExt, TeamBox and PlayerBox.', end='', flush=True)
            Box = GetBox(game['GameID'])
            print('.', end='', flush=True)
            updateStatus = UpdateBox(Box)
            print(f'.{updateStatus}', end='', flush=True)
            test = 1
    return existingGames



#When file is executed, it starts here
iterations = 0
dbGames, iterations = MainFunction(iterations, [])
Wait(len(dbGames))

if iterations > 0:
    while True:
       dbGames, iterations = MainFunction(iterations, dbGames)
       Wait(len(dbGames))