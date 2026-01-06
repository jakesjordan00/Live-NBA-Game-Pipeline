import pyodbc
from DBConfig import nbaConnection, nbaCursor, nbaEngine
from SQLTableColumns import *


def InsertGame(Game: dict, GameExt: dict):
    
    gameCommand = f'''
        insert into Game ({', '.join(keys_Game)})
        values ({', '.join(['?'] * len(keys_Game))})
    '''
    gameExtCommand = f'''
        insert into GameExt ({', '.join(keys_GameExt)})
        values ({', '.join(['?'] * len(keys_GameExt))})
    '''

    try:
        # nbaCursor.execute(gameCommand, DictToParams(Game, gameKeys))
        # nbaCursor.execute(gameExtCommand, DictToParams(GameExt, gameExtKeys))
        # nbaCursor.commit()
        status = 'Game/GameExt success!'
    except Exception as e:
        print(e)
        status = f'Game/GameExt failure!\n\n{e}\n\nGame/GameExt Failure!'

    return status


def InsertTeamBox(TeamBox: list):

    teamBoxCommand = f'''
        insert into TeamBox ({', '.join(keys_TeamBox)})
        values ({', '.join(['?'] * len(keys_TeamBox))})
    '''
    teamBoxParams = [DictToParams(tb, keys_TeamBox) for tb in TeamBox]
    try:
        # nbaCursor.execute(teamBoxCommand, teamBoxParams)
        # nbaCursor.commit()
        status = 'TeamBox success!'
    except Exception as e:
        print(e)
        status = f'TeamBox failure!\n\n{e}\n\nTeamBox Failure!'



def InsertPlayerBox(PlayerBox: list):
    playerBoxCommand = f'''
        insert into TeamBox ({', '.join(keys_PlayerBox)})
        values ({', '.join(['?'] * len(keys_PlayerBox))})
    '''
    playerBoxParams = [DictToParams(tb, keys_PlayerBox) for tb in PlayerBox]

    try:
        # nbaCursor.execute(playerBoxCommand, playerBoxParams)
        # nbaCursor.commit()
        status = 'PlayerBox success!'
    except Exception as e:
        print(e)
        status = f'PlayerBox failure!\n\n{e}\n\nPlayerBox Failure!'
    return status











def DictToParams(d: dict, keys: list) -> tuple:
    return tuple(d[k] for k in keys)