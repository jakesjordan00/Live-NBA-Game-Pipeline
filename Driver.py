from GetScoreboard import GetTodaysScoreboard
from Directions import GetGamesInProgress
from SQL_Reads import FirstIteration
from DBConfig import engine, nbaConnection, nbaCursor
from GetDataNBA import GetBox, GetPlayByPlay






def MainFunction(iterations):
    '''
    Function that runs pipeline
    
    :param iterations: How many times MainFunction has executed
    '''
    #Get the Games in Today's Scoreboard
    dfScoreboard = GetTodaysScoreboard()

    #Using Today's Scoreboard, get the Games that are in progress
    gamesInProg = GetGamesInProgress(dfScoreboard)
    
    #If we're on our first iteration, see what games exist from the Scoreboard
    if iterations == 0:
        existingGames = FirstIteration(nbaCursor, gamesInProg)
        notInDbGames = [game for game in gamesInProg if game not in existingGames]
        for GameID in notInDbGames:
            dfBox = GetBox(GameID)

        test = 1

    test= 1




iterations = 0
MainFunction(iterations)

if iterations > 0:
    while True:
        test = 1