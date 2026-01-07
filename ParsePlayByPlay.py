


def InitiatePlayByPlay(SeasonID: int, GameID: int, actions: list, startPosition: int):
    print(f'     Formatting...')
    PlayByPlay = []
    print(f'     {len(actions[startPosition:])} actions to insert')
    finalAction = actions[-1]
    periods = finalAction['period'] if finalAction['period'] > 3 else 4
    gameTime = 48 if periods == 4 else (5 * (periods - 4))
    a= 1
    for index, action in enumerate(actions[startPosition:]):
        try:
            Clock = action['clock'].replace('PT', '').replace('M', ':').replace('S', '')
            Period = action['period']
            PointInGame = CalculatePointInGame(Clock, Period)

            ShotResult = action['shotResult'] if 'shotResult' in action.keys() else None
            ShotValue = int(action['actionType'][0]) if ShotResult != None and action['actionType'] != 'freethrow' else 1 if action['actionType'] == 'freethrow' else None

            if ShotResult == 'Made':
                ShotType = f"FG{ShotValue}M"
                PtsGenerated = ShotValue
            elif ShotResult == 'Missed':
                ShotType = f"FG{ShotValue}A"
                PtsGenerated = 0
            else:            
                ShotType = None
                PtsGenerated = None
            
            if action['actionType'] == 'freethrow':
                ShotType = f'FT{ShotType[3]}' #type: ignore

            if ShotType != None and len(ShotType) > 4:
                test = 1
            Area = action['area'] if 'area' in action.keys() else None
            AreaDetail = action['areaDetail'] if 'areaDetail' in action.keys() else None
            Qual1 = action['qualifiers'][0] if 'qualifiers' in action.keys() and len(action['qualifiers']) > 0 else None
            Qual2 = action['qualifiers'][1] if 'qualifiers' in action.keys() and len(action['qualifiers']) > 1 else None
            Qual3 = action['qualifiers'][2] if 'qualifiers' in action.keys() and len(action['qualifiers']) > 2 else None
            Description = action['description'].replace("'", "''") if 'description' in action.keys() else None
            Descriptor = action['descriptor'] if 'descriptor' in action.keys() else None

            X = action['x'] if 'x' in action.keys() else None
            XLegacy = action['xLegacy'] if 'xLegacy' in action.keys() else None
            
            Y = action['y'] if 'y' in action.keys() else None
            YLegacy = action['yLegacy'] if 'yLegacy' in action.keys() else None

            TeamID =  action['teamId'] if 'teamId' in action.keys() else None
            Tricode = action['teamTricode'] if 'teamTricode' in action.keys() else None
            ShotDistance = action['shotDistance'] if 'shotDistance' in action.keys() else None
            ShotActionNbr = action['shotActionNbr'] if 'shotActionNbr' in action.keys() else None
            PlayerIDAst = int(action['assistPersonId']) if 'assistPersonId' in action.keys() else None
            PlayerIDBlk = int(action['blockPersonId']) if 'blockPersonId' in action.keys() else None
            PlayerIDStl = int(action['stealPersonId']) if 'stealPersonId' in action.keys() else None
            PlayerIDFoulDrawn = int(action['foulDrawnPersonId']) if 'foulDrawnPersonId' in action.keys() else None
            PlayerIDJumpW = int(action['jumpBallWonPersonId']) if 'jumpBallWonPersonId' in action.keys() else None
            PlayerIDJumpL = int(action['jumpBallLostPersonId']) if 'jumpBallLostPersonId' in action.keys() else None
            OfficialID = int(action['officialId']) if 'officialId' in action.keys() else None
            Possession = action['possession'] if action['possession'] != 0 else None
            PlayerID = action['personId'] if 'personId' in action.keys() and action['personId'] != 0 else None
            IsFieldGoal = action['isFieldGoal'] if action['isFieldGoal'] == 1 else None

            test = 1
        except Exception as e:
            print(e)
            test = 1
        try:
            PlayByPlay.append({
                'SeasonID': SeasonID,
                'GameID': GameID,
                'ActionID': int(index + 1) if startPosition == 0 else int(index + 1 + startPosition),
                'ActionNumber': action['actionNumber'],
                'PointInGame': PointInGame,
                'Qtr': Period,
                'Clock': Clock,
                'TimeActual': action['timeActual'],
                'ScoreHome': action['scoreHome'],
                'ScoreAway': action['scoreAway'],
                'Possession': Possession,
                'TeamID': TeamID,
                'Tricode': Tricode,
                'PlayerID': PlayerID,
                'Description': action['description'],
                'SubType': action['subType'],
                'IsFieldGoal': IsFieldGoal,
                'ShotResult': ShotResult,
                'ShotValue': ShotValue,
                'ActionType': action['actionType'],
                'ShotDistance': ShotDistance,
                'Xlegacy': XLegacy,
                'Ylegacy': YLegacy,
                'X': X,
                'Y': Y,
                'Location': None,

                'Area': Area,
                'AreaDetail': AreaDetail,

                'Side': action['side'],
                'ShotType': ShotType,
                'PtsGenerated': PtsGenerated,
                'Descriptor': Descriptor,

                'Qual1': Qual1,
                'Qual2': Qual2,
                'Qual3': Qual3,
                'ShotActionNbr': ShotActionNbr,
                'PlayerIDAst': PlayerIDAst,
                'PlayerIDBlk': PlayerIDBlk,
                'PlayerIDStl': PlayerIDStl,
                'PlayerIDFoulDrawn': PlayerIDFoulDrawn,
                'PlayerIDJumpW': PlayerIDJumpW,
                'PlayerIDJumpL': PlayerIDJumpL,
                'OfficialID': OfficialID,
                'QtrType': action['periodType']
            })
        except Exception as e:
            print(e)
            test = 1

    return PlayByPlay



def CalculatePointInGame(Clock: str, Period: int):
    cMinutes = int(Clock[0:2])
    cSeconds = float(Clock[-5:])
    PointInGame = 12 - (cMinutes + (cSeconds / 60)) + ((Period - 1) * 12)
    return PointInGame