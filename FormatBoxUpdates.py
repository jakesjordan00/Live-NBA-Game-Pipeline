from SQL_Writes import UpdateBoxData
from SQLTableColumns import *

def FormatUpdates(Box: dict, programMap: str):    
    # programMap += MapProgram(programMap, 'FormatBoxUpdates.FormatUpdates')
    programMap += '╾FormatBoxUpdates.FormatUpdates╼╮'
    


    lastLine = programMap.split('\n')[-1]
    polePosition = lastLine.index('╞')
    programMap += f'\n{lastLine[:polePosition]}│                                ╞╾'




    updateGame, updateGameExt, programMap = FormatGame(Box['Game'], Box['GameExt'], programMap)
    
    programMap += f'\n{lastLine[:polePosition]}│                                ╞╾'
    updateTeamBox, programMap = FormatTeamBox(Box['TeamBox'], programMap)

    programMap += f'\n{lastLine[:polePosition]}│                                ╞╾'
    updatePlayerBox, programMap = FormatPlayerBox(Box['PlayerBox'], programMap)

    programMap += f'\n{lastLine[:polePosition]}│                                ╞╾'

    fullUpdate = f'{updateGame} \n {updateGameExt} \n {updateTeamBox} \n {updatePlayerBox}'
    updateStatus, programMap = UpdateBoxData(fullUpdate, programMap, 'SQL_Writes.UpdateBoxData')

    programMap += f'\n{lastLine[:polePosition]}╞╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾─╯'

    return updateStatus, programMap


def MapWriteUpdate(programMap:str, sender: str, hits: int, parent: str):
    programMap += f'{sender}╼╮x{hits}\n'
    lastLine = programMap.split('\n')[-2]
    spacer = (len(sender) + 2)
    startPos = lastLine.index(sender)
    programMap += f'{lastLine[:startPos -2]}╞╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾─╯\n'
    
    programMap = MapBackToFormatUpdates(programMap, parent)

    return programMap

def MapBackToFormatUpdates(programMap:str, sender: str):
    lastLine = programMap.split('\n')[-4]
    startPos = lastLine.index(sender)
    spacer = len(sender) + 2
    ants = '╼╾' * int(spacer/2)
    if spacer % 2 == 0:
        ants = f'{'╼╾' * (int(spacer/2) - 1)}─'
        test = 1

    programMap += f'{lastLine[:startPos -2]}╞╾{ants}╯'


    return programMap



def MapProgramL2(programMap:str, sender: str):
    programMap += f'{sender}╼╮\n'
    lastLine = programMap.split('\n')[-2]
    spacer = (len(sender) + 2) * ' ' 

    startPos = lastLine.index(sender)
    programMap += f'{lastLine[:startPos -2]}│{spacer}╞╾'
    return programMap



def FormatGame(Game: dict, GameExt: dict, programMap: str):
    programMap = MapProgramL2(programMap, 'FormatBoxUpdates.FormatGame')

    where = f'\nwhere SeasonID = {Game['SeasonID']} and GameID = {Game['GameID']};\n'

    updateGame = WriteUpdate('Game', Game, where, updateColumns_Game)
    updateGameExt = WriteUpdate('GameExt', GameExt, where, updateColumns_GameExt)
    
    programMap = MapWriteUpdate(programMap, 'FormatBoxUpdates.WriteUpdate', 2, 'FormatBoxUpdates.FormatGame')
    
    return updateGame, updateGameExt, programMap


def FormatTeamBox(TeamBox: dict, programMap: str):    
    programMap = MapProgramL2(programMap, 'FormatBoxUpdates.FormatTeamBox') #Good through here
    updateTeamBox = ''
    for team in TeamBox:
        where = f'\nwhere SeasonID = {team['SeasonID']} and GameID = {team['GameID']} and TeamId = {team['TeamID']} and MatchupID = {team['MatchupID']};\n'
        updateTbox = WriteUpdate('TeamBox', team, where, updateColumns_TeamBox)
        updateTeamBox += updateTbox
    
    programMap = MapWriteUpdate(programMap, 'FormatBoxUpdates.WriteUpdate', 2, 'FormatBoxUpdates.FormatTeamBox')
    return updateTeamBox, programMap



def FormatPlayerBox(PlayerBox: dict, programMap: str):
    programMap = MapProgramL2(programMap, 'FormatBoxUpdates.FormatPlayerBox') #Good through here
    updatePlayerBox = ''
    for player in PlayerBox:
        where = f'\nwhere SeasonID = {player['SeasonID']} and GameID = {player['GameID']} and TeamId = {player['TeamID']} and MatchupID = {player['MatchupID']} and PlayerID = {player['PlayerID']};\n'
        updatePbox = WriteUpdate('PlayerBox', player, where, updateColumns_PlayerBox)
        updatePlayerBox += updatePbox
    programMap = MapWriteUpdate(programMap, 'FormatBoxUpdates.WriteUpdate', len(PlayerBox), 'FormatBoxUpdates.FormatPlayerBox')
    return updatePlayerBox, programMap

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


def MapProgram(programMap:str, sender: str):
    programMap += f'{sender}╼╮'
    spacer = (len(sender) + 1) * ' ' 
    lastLine = programMap.split('\n')[-1]
    polePosition = lastLine.index('╞')
    programMap += f'\n{lastLine[:polePosition]}│{spacer}╞'
    a = 'FormatBoxUpdates.FormatUpdates'
    b = '                               '
    return programMap
