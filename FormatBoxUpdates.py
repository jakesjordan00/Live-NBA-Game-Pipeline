from SQL_Writes import UpdateBoxData
from SQLTableColumns import *

def FormatUpdates(Box: dict):

    updateGame, updateGameExt = FormatGame(Box['Game'], Box['GameExt'])
    updateTeamBox = FormatTeamBox(Box['TeamBox'])
    updatePlayerBox = FormatPlayerBox(Box['PlayerBox'])

    fullUpdate = f'{updateGame} \n {updateGameExt} \n {updateTeamBox} \n {updatePlayerBox}'
    updateStatus = UpdateBoxData(fullUpdate)

    return updateStatus




def FormatGame(Game: dict, GameExt: dict):
    where = f'\nwhere SeasonID = {Game['SeasonID']} and GameID = {Game['GameID']};\n'
    updateGame = WriteUpdate('Game', Game, where, updateColumns_Game)
    updateGameExt = WriteUpdate('GameExt', GameExt, where, updateColumns_GameExt)
    test = 1
    return updateGame, updateGameExt


def FormatTeamBox(TeamBox: dict):    
    updateTeamBox = ''
    for team in TeamBox:
        where = f'\nwhere SeasonID = {team['SeasonID']} and GameID = {team['GameID']} and TeamId = {team['TeamID']} and MatchupID = {team['MatchupID']};\n'
        updateTbox = WriteUpdate('TeamBox', team, where, updateColumns_TeamBox)
        updateTeamBox += updateTbox

    return updateTeamBox

def FormatPlayerBox(PlayerBox: dict):
    updatePlayerBox = ''
    for player in PlayerBox:
        where = f'\nwhere SeasonID = {player['SeasonID']} and GameID = {player['GameID']} and TeamId = {player['TeamID']} and MatchupID = {player['MatchupID']} and PlayerID = {player['PlayerID']};\n'
        updatePbox = WriteUpdate('PlayerBox', player, where, updateColumns_PlayerBox)
        updatePlayerBox += updatePbox
    return updatePlayerBox

def WriteUpdate(table: str, dataDict: dict, where: str, columnsToUpdate: list):
    updateStr = f'update {table} set '
    for column in columnsToUpdate:
            columnLookup = column.replace('[', '').replace(']', '')
            if dataDict[columnLookup] != None:
                value = f"{dataDict[columnLookup]}" if type(dataDict[columnLookup]) != str else f"'{dataDict[columnLookup]}'"
                updateStr += f"{column} = {value}, " 

    updateStr = updateStr[:-2] + where
    test = 1
    return updateStr
