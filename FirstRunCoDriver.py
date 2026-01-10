from GetDataNBA import GetBox, GetPlayByPlay, InsertBox, InsertPbp, UpdateBox





def NewGameData(notInDbGames: list):
    dbGames = []
    for GameID in notInDbGames:
        print(f'\n{GameID} not in Database')
        Box = GetBox(GameID)
        if Box != None:
            SeasonID = Box['Game']['SeasonID']
            PlayByPlay = GetPlayByPlay(SeasonID, GameID, 0, 'MainFunction')
            dbGames.append({
                'SeasonID': SeasonID,
                'GameID': GameID,
                'Box': Box,
                'PlayByPlay': PlayByPlay,
                'Actions': len(PlayByPlay)
            })
            boxStatus = InsertBox(Box)
            pbpStatus = InsertPbp(PlayByPlay)
    return dbGames


def ExistingGameData(existingGames: list):
    dbGames = []
    for game in existingGames:
        print(f'\n{game['GameID']}                                        MainFunction, in existingGames')
        Box = GetBox(game['GameID'])
        PlayByPlay = GetPlayByPlay(game['SeasonID'], game['GameID'], 0, 'MainFunctionAlt')
        dbGames.append({
            'SeasonID': game['SeasonID'],
            'GameID': game['GameID'],
            'Box': Box,
            'PlayByPlay': PlayByPlay,
            'Actions': len(PlayByPlay)
        })
        pbp = PlayByPlay[game['Actions']:]
        pbpStatus = InsertPbp(pbp)
        print(f'     {len(pbp)} new actions inserted')
        updateStatus = UpdateBox(Box) #type: ignore
        print(f'     {updateStatus}')


    return dbGames




