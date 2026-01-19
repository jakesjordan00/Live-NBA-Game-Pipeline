from numpy import where
from GetDataNBA import GetBox, GetPlayByPlay, InsertBox, InsertPbp, UpdateBox





def NewGameData(notInDbGames: list, programMap: str, sender: str):
    '''
    This function will only be hit on the first iteration of the program.\n
    Additionally, this function will only be hit if the length of notInDbGames > 0. (We need to insert games we dont have)
    
    :param notInDbGames: List of GameIDs of Games not found in the Database, thus requiring inserts to the tables filled through the Box dataset
    :type notInDbGames: list

    :return: dbGames
    :rtype: list[dict{SeasonID, GameID, Box, PlayByPlay, Actions}]
    '''
    programMap += '\n╰╼╾╼FirstRunCoDriver.NewGameData╼╮\n'
    last = programMap.split('\n')[-2]
    lastLen = len(last) - 1
    mapPole = f'{lastLen * ' '}│'
    programMap += f'{(lastLen - 8) * ' '}{notInDbGames[0]['GameID']}╞╾'
    dbGames = []
    for i, game in enumerate(notInDbGames):
        if i > 0:
            programMap += f'\n{(lastLen - 8) * ' '}{game['GameID']}╞╾'
        homeLineup = []
        awayLineup = []
        GameID = game['GameID']
        print(f'\n{GameID} not in Database...')
        Box, programMap = GetBox(GameID, game, sender, programMap,mapPole)
        if Box != None:
            SeasonID = Box['Game']['SeasonID']
            HomeID = Box['Game']['HomeID']
            AwayID = Box['Game']['AwayID']
            for player in Box['StartingLineups']:
                if player['Unit'] == 'Bench':
                    continue
                if HomeID == player['TeamID'] and player['Unit'] == 'Starters':
                    homeLineup.append(player['PlayerID'])
                elif AwayID == player['TeamID'] and player['Unit'] == 'Starters':
                    awayLineup.append(player['PlayerID'])
            programMap += f'\n{lastLen * ' '}╞╾'
            PlayByPlay, programMap = GetPlayByPlay(SeasonID, GameID, 0, 'MainFunction', programMap)
            dbGames.append({
                'SeasonID': SeasonID,
                'GameID': GameID,
                'Box': Box,
                'PlayByPlay': PlayByPlay,
                'Actions': len(PlayByPlay),
                'Data': game
            })
            boxStatus, programMap = InsertBox(Box, programMap)
            pbpStatus, programMap = InsertPbp(PlayByPlay, programMap, 'MainFunction')
    programMap += '\n╭╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╯'
    return dbGames, programMap


def ExistingGameData(existingGames: list, programMap: str) -> tuple[list[dict], str]:
    '''
    This function will only be hit on the first iteration of the program.\n
    Different from NewGameData, this function is only hit if the length of existingGames > 0. (We need to update games that we already have in the db)
    
    :param existingGames: List of GameIDs of 
    :type existingGames: list

    :return: dbGames
    :rtype: list[dict{SeasonID, GameID, Box, PlayByPlay, Actions}]
    '''

    programMap += '\n╰╼╾╼FirstRunCoDriver.ExistingGameData╼╮\n'
    last = programMap.split('\n')[-2]
    lastLen = len(last) - 1
    mapPole = f'{lastLen * ' '}│'
    programMap += f'{(lastLen - 8) * ' '}{existingGames[0]['GameID']}╞╾'
    dbGames = []
    
    for i, game in enumerate(existingGames):
        if i > 0:
            programMap += f'\n{(lastLen - 8) * ' '}{game['GameID']}╞╾'
        print(f'\n{game['GameID']}                                        MainFunction, in existingGames')
        Box, programMap = GetBox(game['GameID'], game['Data'], 'MainFunction', programMap, mapPole)


        programMap += f'\n{lastLen * ' '}╞╾'
        HomeID = Box['Game']['HomeID']
        AwayID = Box['Game']['AwayID']
        PlayByPlay, programMap = GetPlayByPlay(game['SeasonID'], game['GameID'], 0, 'MainFunctionAlt', programMap)

        dbGames.append({
            'SeasonID': game['SeasonID'],
            'GameID': game['GameID'],
            'Box': Box,
            'PlayByPlay': PlayByPlay,
            'Actions': len(PlayByPlay),
            'Data': game['Data']
        })
        pbp = PlayByPlay[game['Actions']:]
        if len(pbp) > 0:
            lastLine = programMap.split('\n')[-1]
            polePosition = lastLine.index('╞')
            programMap += f'\n{lastLine[:polePosition]}╞╾GetDataNBA.InsertPbp╼╮\n'
            pbpStatus, programMap = InsertPbp(pbp, programMap, 'MainFunction')
            print(f'     {len(pbp)} new actions inserted')
        else:            
            print(f'     No new actions')
        
        lastLine = programMap.split('\n')[-1]
        polePosition = lastLine.index('╞')
        programMap += f'\n{lastLine[:polePosition]}╞╾GetDataNBA.UpdateBox╼╮'
        updateStatus, programMap = UpdateBox(Box, programMap) #type: ignore
        
        print(f'     {updateStatus}')

    programMap += f'\n╭╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾╼╾─╯'
    


    return dbGames, programMap







