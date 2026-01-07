from GetScoreboard import GetTodaysScoreboard
from Directions import GetGamesInProgress
from SQL_Reads import FirstIteration
from DBConfig import nbaEngine, nbaConnection, nbaCursor
from GetDataNBA import GetBox, GetPlayByPlay, InsertBox, InsertPbp






def MainFunction(iterations: int, dbGames: list):
    '''
    Function that runs pipeline. Will get Box and/or PlayByPlay data
    
    :param iterations: How many times MainFunction has executed
    :type iterations: int
    '''
    #Get the Games in Today's Scoreboard
    dfScoreboard = GetTodaysScoreboard()

    #Using Today's Scoreboard, get the Games that are in progress
    gamesInProg = GetGamesInProgress(dfScoreboard)
    
    #If we're on our first iteration or every fifth, see what games exist from the Scoreboard in the Db
    if iterations == 0 or iterations % 5 == 0:
        existingGames = FirstIteration(nbaCursor, gamesInProg)
        existingGameIDs = list(g['GameID']for g in existingGames )
        notInDbGames = [game for game in gamesInProg if game not in existingGameIDs]
        for GameID in notInDbGames:
            print(f'\n{GameID}                                        MainFunction')
            Box = GetBox(GameID)
            if Box != None:
                boxStatus = InsertBox(Box)
                SeasonID = Box['Game']['SeasonID']
                PlayByPlay = GetPlayByPlay(SeasonID, GameID, 0, 'MainFunction')
                pbpStatus = InsertPbp(PlayByPlay)
                dbGames.append({
                    'SeasonID': SeasonID,
                    'GameID': GameID,
                    'Actions': len(PlayByPlay)
                })

        inDbGames = [game for game in gamesInProg if game in existingGameIDs]
        for game in existingGames:
            dbGames.append({
                'SeasonID': game['SeasonID'],
                'GameID': game['GameID'],
                'Actions': game['Actions']
            })

        test = 1
    else:
    #If not, 
        existingGames = dbGames.copy()
        RecurringFunction(existingGames, iterations)
    iterations += 1
    return dbGames, iterations

def RecurringFunction(existingGames: list, iterations: int):
    for game in existingGames:
        print(f'\n{game['GameID']}                                        RecurringFunction v{iterations}')
        PlayByPlay = GetPlayByPlay(game['SeasonID'], game['GameID'], game['Actions'], 'RecurringFunction')
        test = 1
    return 1


iterations = 0
dbGames, iterations = MainFunction(iterations, [])

if iterations > 0:
    while True:
       dbGames, iterations = MainFunction(iterations, dbGames)
       test = 1