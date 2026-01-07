from GetScoreboard import GetTodaysScoreboard
from Directions import GetGamesInProgress
from SQL_Reads import FirstIteration
from DBConfig import nbaEngine, nbaConnection, nbaCursor
from GetDataNBA import GetBox, GetPlayByPlay, InsertBox, InsertPbp






def MainFunction(iterations: int, dbGames: list):
    '''
    Function that runs pipeline
    
    :param iterations: How many times MainFunction has executed
    :type iterations: int
    '''
    #Get the Games in Today's Scoreboard
    dfScoreboard = GetTodaysScoreboard()

    #Using Today's Scoreboard, get the Games that are in progress
    gamesInProg = GetGamesInProgress(dfScoreboard)
    
    test = iterations % 5
    #If we're on our first iteration or every fifth, see what games exist from the Scoreboard in the Db
    if iterations == 0 or iterations % 5 == 0:
        existingGames = FirstIteration(nbaCursor, gamesInProg)
        notInDbGames = [game for game in gamesInProg if game not in existingGames]
        for GameID in notInDbGames:
            print(f'\n{GameID}')
            Box = GetBox(GameID)
            if Box != None:
                boxStatus = InsertBox(Box)
                SeasonID = Box['Game']['SeasonID']
                PlayByPlay = GetPlayByPlay(SeasonID, GameID, 0, 'MainFunction')
                pbpStatus = InsertPbp(PlayByPlay)
                # print(f'          {pbpStatus}')
                dbGames.append({
                    'SeasonID': SeasonID,
                    'GameID': GameID,
                    'Actions': len(PlayByPlay)
                })

        test = 1
    else:
    #If not, 
        existingGames = dbGames.copy()
        RecurringFunction(existingGames)
        test = 1
    iterations += 1
    test= 1
    return dbGames, iterations

def RecurringFunction(existingGames: list):
    for game in existingGames:
        PlayByPlay = GetPlayByPlay(game['SeasonID'], game['GameID'], game['Actions'], 'RecurringFunction')

    return 1


iterations = 0
dbGames, iterations = MainFunction(iterations, [])

if iterations > 0:
    while True:
       dbGames, iterations = MainFunction(iterations, dbGames)
       test = 1