from GetScoreboard import GetTodaysScoreboard
from Directions import GetGamesInProgress
from SQL_Reads import FirstIteration
from DBConfig import engine, nbaConnection, nbaCursor







def MainFunction(iterations):
    #Get the Games in Today's Scoreboard
    dfScoreboard = GetTodaysScoreboard()

    #Using Today's Scoreboard, get the Games that are in progress
    gamesInProg = GetGamesInProgress(dfScoreboard)
    
    if iterations == 0:
        existingGames = FirstIteration(engine, gamesInProg)
        test = 1

    test= 1




iterations = 0
MainFunction(iterations)

if iterations > 0:
    while True:
        test = 1