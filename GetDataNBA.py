import requests
import pandas as pd
from ParseBox import InitiateBox
from ParsePlayByPlay import InitiatePlayByPlay
from SQL_Writes import InsertBoxscores, InsertGame, InsertPlayByPlay, InsertArena, InsertPlayer, InsertTeam, InsertOfficial
from FormatBoxUpdates import *
urlBoxScore = 'https://cdn.nba.com/static/json/liveData/boxscore/boxscore_'
urlPlayByPlay = 'https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_'


def GetBox(GameID: int, Data: dict, sender: str, programMap: str, mapPole: str):
    '''
    Hits Boxscore.json url of GameID passed
    
    :param GameID: GameID of game
    :type GameID: int
    '''
    
    test = programMap.split('\n')[-1]
    programMap += f'GetDataNBA.GetBox╼╮\n{mapPole}'
    if sender == 'MainFunction':
        print(f'     Retrieving Box data')
    urlBox = f'{urlBoxScore}00{GameID}.json'
    try:
        response = requests.get(urlBox)
        data = response.json()
        game = data['game']
        Box, programMap = InitiateBox(game, Data, sender, programMap, mapPole)
    except Exception as e:
        print(f"Error getting Boxscore data: {e}")

    return Box, programMap


def InsertBox(Box: dict, programMap: str):
    split = programMap.split('\n')
    lastLine = split[-2] if split[-1] == '' else split[-1]
    polePosition = lastLine.find('╞')
    programMap += f'\n{lastLine[:polePosition + 1]}╾GetDataNBA.InsertBox╼╮\n'
    programMap += f'{lastLine[:polePosition]}│                      ╞╾SQL_Writes.InsertGame╼╮\n'
    programMap += f'{lastLine[:polePosition]}│                      ╞╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╯\n'
    for team in Box['Team']:
        tStatus = InsertTeam(team)
    aStatus = InsertArena(Box['Arena'])
    for player in Box['Player']:
        pStatus = InsertPlayer(player)
    for official in Box['Official']:
        oStatus = InsertOfficial(official)
    gStatus = InsertGame(Box['Game'], Box['GameExt'])
    # if Box['Arena']['ArenaID'] == 315:
    #     aStatus = InsertArena(Box['Arena'])


    boxStatus = InsertBoxscores(Box['TeamBox'], Box['PlayerBox'], Box['StartingLineups'])
    programMap += f'{lastLine[:polePosition]}│                      ╞╾SQL_Writes.InsertBoxscores╼╮\n'
    programMap += f'{lastLine[:polePosition]}│                      ╞╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾─╯\n'
    programMap += f'{lastLine[:polePosition + 1]}╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╯\n'
    return f'{gStatus}\n{boxStatus}', programMap



def UpdateBox(Box: dict, programMap: str):
    lastLine = programMap.split('\n')[-1]
    polePosition = lastLine.index('╞')
    programMap += f'\n{lastLine[:polePosition]}│                      ╞'
    updateStatus, programMap = FormatUpdates(Box, programMap)
    
    programMap += f'\n{lastLine[:polePosition]}╞╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾─╯'
    return updateStatus, programMap



def GetPlayByPlay(SeasonID: int, GameID: int, ActionCount: int, sender: str, programMap: str):
    last2 = programMap.split('\n')[-1] if programMap.split('\n')[-1] != '' else programMap.split('\n')[-2]
    programMap += 'GetDataNBA.GetPlayByPlay╼╮\n'
    last1 = programMap.split('\n')[-2]
    polePosition = last1.find('╞') if last1.find('╞') != -1 else last2.find('╞')
    secondPole = last1.index('╼╮')
    programMap += f'{(polePosition * ' ')}│'
    programMap += f'{(secondPole - polePosition) * ' '}'
    if 'MainFunction' in sender:
        print(f'     Retrieving PlayByPlay data')
    urlPbp = f'{urlPlayByPlay}00{GameID}.json'
    try:
        response = requests.get(urlPbp)
        data = response.json()
        actions = data['game']['actions']
        PlayByPlay, programMap = InitiatePlayByPlay(SeasonID, GameID, actions, ActionCount, sender, programMap)
    except Exception as e:
        PlayByPlay = pd.DataFrame()
        print(f"Error getting PlayByPlay data: {e}")
    
    return PlayByPlay, programMap



def InsertPbp(PlayByPlay, programMap: str, sender: str):
    # lastLine = programMap.split('\n')[-2]
    # polePosition = lastLine.index('╞')
    # programMap += f'{lastLine[:polePosition]}│                      ╞'
    
    split = programMap.split('\n')
    lastLine = split[-2] if split[-1] == '' else split[-1]
    polePosition = lastLine.find('╞')
    nl = '\n' if lastLine == split[-1] else ''
    programMap += f'{nl}{lastLine[:polePosition]}╞╾GetDataNBA.InsertPbp╼╮'
    programMap += f'\n{lastLine[:polePosition]}│                      ╞'

    pbpStatus, programMap = InsertPlayByPlay(PlayByPlay, programMap)
    programMap += f'\n{lastLine[:polePosition]}╞╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾─╯'

    return f'{pbpStatus}', programMap 