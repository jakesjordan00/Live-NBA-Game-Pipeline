import pyodbc
from DBConfig import nbaConnection, nbaCursor, nbaEngine
from SQLTableColumns import *


def InsertGame(Game: dict, GameExt: dict):
    
    gameCommand = f'''
        insert into Game ({', '.join(columns_Game)})
        values ({', '.join(['?'] * len(columns_Game))})
    '''
    gameExtCommand = f'''
        insert into GameExt ({', '.join(columns_GameExt)})
        values ({', '.join(['?'] * len(columns_GameExt))})
    '''

    try:
        nbaCursor.execute(gameCommand, DictToParams(Game, columns_Game))
        nbaCursor.execute(gameExtCommand, DictToParams(GameExt, columns_GameExt))
        nbaCursor.commit()
        status = 'Game/GameExt success!'
    except Exception as e:
        print(e)
        status = f'Game/GameExt failure!\n\n{e}\n\nGame/GameExt Failure!'

    return status


def InsertTeamBox(TeamBox: list):

    teamBoxCommand = f'''
        insert into TeamBox ({', '.join(columns_TeamBox)})
        values ({', '.join(['?'] * len(columns_TeamBox))})
    '''
    teamBoxParams = DictToParams(TeamBox[0], columns_TeamBox) 
    try:
        nbaCursor.execute(teamBoxCommand, teamBoxParams)
        nbaCursor.commit()
        status = 'TeamBox success!'
    except Exception as e:
        print(e)
        status = f'TeamBox failure!\n\n{e}\n\nTeamBox Failure!'



def InsertPlayerBox(PlayerBox: list):
    playerBoxCommand = f'''
        insert into PlayerBox ({', '.join(columns_PlayerBox)})
        values ({', '.join(['?'] * len(columns_PlayerBox))})
    '''
    playerBoxParams = [DictToParams(tb, columns_PlayerBox) for tb in PlayerBox]

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
        insert into TeamBox ({', '.join(columns_TeamBox)})
        values ({', '.join(['?'] * len(columns_TeamBox))})
    '''
    playerBoxCommand = f'''
        insert into PlayerBox ({', '.join(columns_PlayerBox)})
        values ({', '.join(['?'] * len(columns_PlayerBox))})
    '''
    startingLineupsCommand = f'''
        insert into StartingLineups ({', '.join(columns_StartingLineups)})
        values ({', '.join(['?'] * len(columns_StartingLineups))})
    '''

    teamBoxCommand = teamBoxCommand.replace('FG2%', '[FG2%]').replace('FG3%', '[FG3%]').replace('FG%', '[FG%]').replace('FT%', '[FT%]')
    playerBoxCommand = playerBoxCommand.replace('FG2%', '[FG2%]').replace('FG3%', '[FG3%]').replace('FG%', '[FG%]').replace('FT%', '[FT%]')
    
    teamBoxParams = [DictToParams(tb, columns_TeamBox) for tb in TeamBox]
    playerBoxParams = [DictToParams(pb, columns_PlayerBox) for pb in PlayerBox]
    startingLineupsParams = [DictToParams(sl, columns_StartingLineups) for sl in StartingLineups]

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
        insert into PlayByPlay ({', '.join(columns_PlayByPlay)})
        values ({', '.join(['?'] * len(columns_PlayByPlay))})
    '''
    playByPlayParams = [DictToParams(action, columns_PlayByPlay) for action in PlayByPlay]

    try:
        # nbaCursor.fast_executemany = True
        nbaCursor.executemany(playByPlayCommand, playByPlayParams)
        nbaCursor.commit()
        status = 'PlayByPlay success!'
    except Exception as e:
        print(e)
        status = f'PlayByPlay failure!\n\n{e}\n\nPlayByPlay Failure!'
    return status


def FormatBox(Box: dict):
    updateBoxCmd = 'update PlayerBox set '
    boxUpdateColumns = columns_PlayerBox[5:]
    for column in boxUpdateColumns:
        # value = Box[]
        test = f"{column} = " 
    test = str(col for col in boxUpdateColumns).join(" = ")
    boxParams = ''
    try:
        nbaCursor.fast_executemany = True
        nbaCursor.executemany(updateBoxCmd, boxParams)
        nbaCursor.commit()
        status = 'Box success!'
    except Exception as e:
        print(e)
        status = f'PlayByPlay failure!\n\n{e}\n\nPlayByPlay Failure!'
    return status




def DictToParams(d: dict, keys: list) -> tuple:
    return tuple(d[k] for k in keys)

