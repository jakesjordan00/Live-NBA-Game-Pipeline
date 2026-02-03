import pyodbc
from DBConfig import nbaConnection, nbaCursor, nbaEngine
from SQLTableColumns import *
import pyperclip


def InsertGame(Game: dict, GameExt: dict):
    gKeys = ['SeasonID', 'GameID']
    gameCommand = f'''
    if not exists
    (select 1 from Game where SeasonID = ? and GameID = ?)
    begin
        insert into Game ({', '.join(columns_Game)})
        values ({', '.join(['?'] * len(columns_Game))})
    end
    '''
    gameExtCommand = f'''
    if not exists
    (select 1 from GameExt where SeasonID = ? and GameID = ?)
    begin
        insert into GameExt ({', '.join(columns_GameExt)})
        values ({', '.join(['?'] * len(columns_GameExt))})
    end
    '''

    try:
        nbaCursor.execute(gameCommand, DictToParams(Game, gKeys + columns_Game))
        nbaCursor.execute(gameExtCommand, DictToParams(GameExt, gKeys + columns_GameExt))
        nbaCursor.commit()
        status = 'Game/GameExt success!'
    except Exception as e:
        print(e)
        status = f'Game/GameExt failure!\n\n{e}\n\nGame/GameExt Failure!'

    return status

def InsertTeam(Team: dict):
    gameCommand = f'''
    if not exists
    (select 1 from Team where SeasonID = ? and TeamID = ?)
    begin
        insert into Team ({', '.join(columns_Team)})
        values ({', '.join(['?'] * len(columns_Team))})
    end
    '''

    try:
        nbaCursor.execute(gameCommand, DictToParams(Team, ['SeasonID', 'TeamID'] + columns_Team))
        nbaCursor.commit()
        status = 'Team success!'
    except Exception as e:
        print(e)
        status = f'Team failure!\n\n{e}\n\nGame/GameExt Failure!'

    return status


def InsertArena(Arena: dict):
    gameCommand = f'''
    if not exists
    (select 1 from Arena where SeasonID = ? and ArenaID = ?)
    begin
        insert into Arena ({', '.join(columns_Arena)})
        values ({', '.join(['?'] * len(columns_Arena))})
    end
    '''

    try:
        nbaCursor.execute(gameCommand, DictToParams(Arena, ['SeasonID', 'ArenaID'] + columns_Arena))
        nbaCursor.commit()
        status = 'Arena success!'
    except Exception as e:
        print(e)
        status = f'Arena failure!\n\n{e}\n\nGame/GameExt Failure!'

    return status

def InsertPlayer(Player: dict):
    gameCommand = f'''
    if not exists
    (select 1 from Player where SeasonID = ? and PlayerID = ?)
    begin
        insert into Player ({', '.join(columns_Player)})
        values ({', '.join(['?'] * len(columns_Player))})
    end
    '''

    try:
        nbaCursor.execute(gameCommand, DictToParams(Player, ['SeasonID', 'PlayerID'] + columns_Player))
        nbaCursor.commit()
        status = 'Player success!'
    except Exception as e:
        print(e)
        status = f'Player failure!\n\n{e}\n\nGame/GameExt Failure!'

    return status

def InsertOfficial(Official: dict):
    gameCommand = f'''
    if not exists
    (select 1 from Official where SeasonID = ? and OfficialID = ?)
    begin
        insert into Official ({', '.join(columns_Official)})
        values ({', '.join(['?'] * len(columns_Official))})
    end
    '''

    try:
        nbaCursor.execute(gameCommand, DictToParams(Official, ['SeasonID', 'OfficialID'] + columns_Official))
        nbaCursor.commit()
        status = 'Official success!'
    except Exception as e:
        print(e)
        status = f'Official failure!\n\n{e}\n\nGame/GameExt Failure!'

    return status




def InsertBoxscores(TeamBox: list, PlayerBox: list, StartingLineups: list):
    tKeys = ['SeasonID', 'GameID', 'TeamID', 'MatchupID']
    teamBoxCommand = f'''
    if not exists
    (select 1 from TeamBox where SeasonID = ? and GameID = ? and TeamID = ? and MatchupID = ?)
    begin
        insert into TeamBox ({', '.join(columns_TeamBox)})
        values ({', '.join(['?'] * len(columns_TeamBox))})
    end
    '''

    pKeys = ['SeasonID', 'GameID', 'TeamID', 'MatchupID', 'PlayerID']
    playerBoxCommand = f'''
    if not exists
    (select 1 from PlayerBox where SeasonID = ? and GameID = ? and TeamID = ? and MatchupID = ? and PlayerID = ?)
    begin
        insert into PlayerBox ({', '.join(columns_PlayerBox)})
        values ({', '.join(['?'] * len(columns_PlayerBox))})
    end
    '''
    startingLineupsCommand = f'''
        if not exists
    (select 1 from StartingLineups where SeasonID = ? and GameID = ? and TeamID = ? and MatchupID = ? and PlayerID = ?)
    begin
        insert into StartingLineups ({', '.join(columns_StartingLineups)})
        values ({', '.join(['?'] * len(columns_StartingLineups))})
    end
    '''

    teamBoxCommand = teamBoxCommand.replace('FG2%', '[FG2%]').replace('FG3%', '[FG3%]').replace('FG%', '[FG%]').replace('FT%', '[FT%]')
    playerBoxCommand = playerBoxCommand.replace('FG2%', '[FG2%]').replace('FG3%', '[FG3%]').replace('FG%', '[FG%]').replace('FT%', '[FT%]')
    

    teamBoxParams = [DictToParams(tb, tKeys + columns_TeamBox) for tb in TeamBox]
    playerBoxParams = [DictToParams(pb,  pKeys + columns_PlayerBox) for pb in PlayerBox]
    startingLineupsParams = [DictToParams(sl, pKeys + columns_StartingLineups) for sl in StartingLineups]

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



def InsertPlayByPlay(PlayByPlay: list, programMap: str):
    programMap += '╾SQL_Writes.InsertPlayByPlay╼╮'
    playByPlayCommand = f'''
        insert into PlayByPlay ({', '.join(columns_PlayByPlay)})
        values ({', '.join(['?'] * len(columns_PlayByPlay))})
    '''
    playByPlayParams = [DictToParams(action, columns_PlayByPlay) for action in PlayByPlay]

    try:
        # nbaCursor.fast_executemany = True
        if len(PlayByPlay) > 0:
            nbaCursor.executemany(playByPlayCommand, playByPlayParams)
            nbaCursor.commit()
            status = 'PlayByPlay success!'
        programMap += f' {len(PlayByPlay)} actions inserted\n'
    except Exception as e:
        programMap += f' Insert failed!\n'
        print(e)
        status = f'PlayByPlay failure!\n\n{e}\n\nPlayByPlay Failure!'

    lastLine = programMap.split('\n')[-2]
    polePosition = lastLine.index('╞')
    programMap += f'{lastLine[:polePosition]}╞╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╯'
    return status, programMap


def UpdateBoxData(updateStr: str, programMap: str, sender: str):
    programMap += f'{sender}╼╮\n'
    lastLine = programMap.split('\n')[-2]
    spacer = (len(sender) + 2) * ' ' 
    startPos = lastLine.index(sender)
    programMap += f'{lastLine[:startPos -2]}╞╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾─╯'
    # pyperclip.copy(updateStr)
    try:
        # nbaCursor.fast_executemany = True
        nbaCursor.execute(updateStr)
        nbaCursor.commit()
        status = 'Game, GameExt, TeamBox and Playerbox updated successfully!'
    except Exception as e:
        print(e)
        status = f'Game, GameExt, TeamBox and Playerbox update failed!\n\n{e}\n\nGame, GameExt, TeamBox and Playerbox update failed!'

    return status, programMap



def DictToParams(d: dict, keys: list) -> tuple:
    return tuple(d[k] for k in keys)





