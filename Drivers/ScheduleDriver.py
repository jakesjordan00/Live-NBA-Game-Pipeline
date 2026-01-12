import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from GetSchedule import GetSchedule
from Directions import GetGamesInProgress, Wait
from SQL_Reads import FirstIteration
from GetDataNBA import GetBox, GetPlayByPlay, InsertBox, InsertPbp, UpdateBox
from FirstRunCoDriver import NewGameData, ExistingGameData
from DBConfig import nbaCursor
import time
print('-')


def MainFunction():
    '''
    Function that runs pipeline. Will get Box and/or PlayByPlay data
    
    :param iterations: How many times MainFunction has executed
    :type iterations: int

    :param dbGames: List of Game dictionaries. Contains SeasonID, GameID and a count of the PlayByPlay actions
    :type dbGames: list[dict]
    '''
    #Get the Games in Today's Scoreboard
    print('Getting Scoreboard...')
    dfGames = GetSchedule()
    dbGames = []
    #Using Today's Scoreboard, get the Games that are in progress
    #^^^^ still need to implement as of 1:09am 1/9/26!
    #^ Should be implements....1/11/25. Just need to make sure its working as expected.

    print(f'{len(dfGames)} Games in progress')

    #Declare Box and PlayByPlay as none
    Box = None
    PlayByPlay = None
    gameIDs = dfGames['GameID'].to_list()
    #If we're on our first iteration or every fifth, see what games exist from the Scoreboard in the Db
    existingGames = FirstIteration(gameIDs)
    existingGameIDs = list(g['GameID']for g in existingGames )
    notInDbGames = [game for game in gameIDs if game not in existingGameIDs]
    if len(notInDbGames) > 0:
        dbGames.extend(NewGameData(notInDbGames))
    if len(existingGames) > 0:
        dbGames.extend(ExistingGameData(existingGames))
    test = 1



def InsertPlayByPlay():
    gameList = []
    games = input('Enter GameID (if multiple, separate with space): ')
    if ' ' in games or ' ' in games:
        games = games.replace(',', '').replace(' ', ' ').strip().split(' ')
    else:
        games = [int(games)]
    test = 1
    for game in games:
        GameID = game
        SeasonID = int(f'20{str(GameID)[1:3]}')
        gameList.append({
        'SeasonID': SeasonID,
        'GameID': GameID,
        'Actions': 0
        })

    deleteCmd = ', '.join(game['GameID'] for game in gameList)
    DeleteGames(deleteCmd)
    ExistingGameData(gameList)


def DeleteGames(deleteCmd: str):
    deleteCmd = f'''
delete from jjs.StintPlayer 
where SeasonID = 2025 and GameID in({deleteCmd})

delete from jjs.Stint 
where SeasonID = 2025 and GameID in({deleteCmd})

delete from PlayByPlay 
where SeasonID = 2025 and GameID in({deleteCmd})
'''
    nbaCursor.execute(deleteCmd)
    nbaCursor.commit()



# MainFunction()

InsertPlayByPlay()