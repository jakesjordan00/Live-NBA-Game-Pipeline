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
        nbaCursor.execute(gameCommand, DictToParams(Game, keys_Game))
        nbaCursor.execute(gameExtCommand, DictToParams(GameExt, keys_GameExt))
        nbaCursor.commit()
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
    teamBoxParams = DictToParams(TeamBox[0], keys_TeamBox) 
    try:
        nbaCursor.execute(teamBoxCommand, teamBoxParams)
        nbaCursor.commit()
        status = 'TeamBox success!'
    except Exception as e:
        print(e)
        status = f'TeamBox failure!\n\n{e}\n\nTeamBox Failure!'



def InsertPlayerBox(PlayerBox: list):
    playerBoxCommand = f'''
        insert into PlayerBox ({', '.join(keys_PlayerBox)})
        values ({', '.join(['?'] * len(keys_PlayerBox))})
    '''
    playerBoxParams = [DictToParams(tb, keys_PlayerBox) for tb in PlayerBox]

    try:
        nbaCursor.execute(playerBoxCommand, playerBoxParams)
        nbaCursor.commit()
        status = 'PlayerBox success!'
    except Exception as e:
        print(e)
        status = f'PlayerBox failure!\n\n{e}\n\nPlayerBox Failure!'
    return status


def InsertBoxscores(TeamBox: list, PlayerBox: list, StartingLineups: list):
    teamBoxCommand = f'''
        insert into TeamBox ({', '.join(keys_TeamBox)})
        values ({', '.join(['?'] * len(keys_TeamBox))})
    '''
    playerBoxCommand = f'''
        insert into PlayerBox ({', '.join(keys_PlayerBox)})
        values ({', '.join(['?'] * len(keys_PlayerBox))})
    '''
    startingLineupsCommand = f'''
        insert into StartingLineups ({', '.join(keys_StartingLineups)})
        values ({', '.join(['?'] * len(keys_StartingLineups))})
    '''

    teamBoxCommand = teamBoxCommand.replace('FG2%', '[FG2%]').replace('FG3%', '[FG3%]').replace('FG%', '[FG%]').replace('FT%', '[FT%]')
    playerBoxCommand = playerBoxCommand.replace('FG2%', '[FG2%]').replace('FG3%', '[FG3%]').replace('FG%', '[FG%]').replace('FT%', '[FT%]')
    
    teamBoxParams = [DictToParams(tb, keys_TeamBox) for tb in TeamBox]
    playerBoxParams = [DictToParams(pb, keys_PlayerBox) for pb in PlayerBox]
    startingLineupsParams = [DictToParams(sl, keys_StartingLineups) for sl in StartingLineups]

    try:
        nbaCursor.executemany(teamBoxCommand, teamBoxParams)
        nbaCursor.executemany(playerBoxCommand, playerBoxParams)
        nbaCursor.executemany(startingLineupsCommand, startingLineupsParams)
        nbaCursor.commit()
        status = 'TeamBox/PlayerBox/StartingLineups success!'
    except Exception as e:
        print(e)
        status = f'TeamBox/PlayerBox/StartingLineups failure!\n\n{e}\n\nTeamBox/PlayerBox/StartingLineups Failure!'
    return status



def InsertPlayByPlay(PlayByPlay: list):

    playByPlayCommand = f'''
        insert into PlayByPlay ({', '.join(keys_PlayByPlay)})
        values ({', '.join(['?'] * len(keys_PlayByPlay))})
    '''
    playByPlayParams = [DictToParams(action, keys_PlayByPlay) for action in PlayByPlay]

    try:
        nbaCursor.executemany(playByPlayCommand, playByPlayParams)
        nbaCursor.commit()
        status = 'PlayByPlay success!'
    except Exception as e:
        print(e)
        status = f'PlayByPlay failure!\n\n{e}\n\nPlayByPlay Failure!'
    return status


def FormatInsert():

    insertCmd = ''
    return insertCmd




def DictToParams(d: dict, keys: list) -> tuple:
    return tuple(d[k] for k in keys)

