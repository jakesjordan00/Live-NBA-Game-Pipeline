


def InitiatePlayByPlay(SeasonID: int, GameID: int, actions: list, startPosition: int, sender: str, programMap: str):
    totalActions = len(actions[startPosition:])
    if totalActions > 0:
        programMap += '\n            ParsePlayByPlay.InitiatePlayByPlay ➡️'
        programMap += f'\n                ParsePlayByPlay.CalculatePointInGame x{totalActions}\n            ↩️'
        if 'MainFunction' in sender:
            print(f'     Formatting...') 
        singularPlural = 'action' if totalActions == 1 else 'actions'
        print(f'     {len(actions[startPosition:])} {singularPlural} to insert') if sender != 'MainFunctionAlt' else print(f'     {len(actions[startPosition:])} total {singularPlural}')
    else:
        programMap += '\n            ParsePlayByPlay.InitiatePlayByPlay\n            ↩️'
        print(f'     No new actions')
    PlayByPlay = []
    finalAction = actions[-1]
    periods = finalAction['period'] if finalAction['period'] > 3 else 4
    gameTime = 48 if periods == 4 else (5 * (periods - 4))
    a= 1
    for index, action in enumerate(actions[startPosition:]):
        try:
            Clock = action['clock'].replace('PT', '').replace('M', ':').replace('S', '')
            Period = action['period']
            PointInGame = CalculatePointInGame(Clock, Period)

            ShotResult = action.get('shotResult')
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
            Area = action.get('area')
            AreaDetail = action.get('areaDetail')
            Qual1 = action['qualifiers'][0] if 'qualifiers' in action.keys() and len(action['qualifiers']) > 0 else None
            Qual2 = action['qualifiers'][1] if 'qualifiers' in action.keys() and len(action['qualifiers']) > 1 else None
            Qual3 = action['qualifiers'][2] if 'qualifiers' in action.keys() and len(action['qualifiers']) > 2 else None
            Description = action.get('description').replace("'", "''")
            Descriptor = action.get('descriptor')

            X = action.get('x')
            XLegacy = action.get('xLegacy')
            
            Y = action.get('y')
            YLegacy = action.get('yLegacy')
            action.get('')
            TeamID = action.get('teamId')
            Tricode = action.get('teamTricode')
            ShotDistance = action.get('shotDistance')
            ShotActionNbr = action.get('shotActionNbr')
            PlayerIDAst = action.get('assistPersonId')
            PlayerIDBlk = action.get('blockPersonId')
            PlayerIDStl = action.get('stealPersonId')
            PlayerIDFoulDrawn = action.get('foulDrawnPersonId')
            PlayerIDJumpW = action.get('jumpBallWonPersonId')
            PlayerIDJumpL = action.get('jumpBallLostPersonId')
            OfficialID = action.get('officialId')
            Possession = action.get('possession')
            PlayerID = action.get('personId')
            IsFieldGoal = action.get('isFieldGoal')


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
    if len(PlayByPlay) == 0:
        test = 1
    return PlayByPlay, programMap



def CalculatePointInGame(Clock: str, Period: int):
    cMinutes = int(Clock[0:2])
    cSeconds = float(Clock[-5:])
    PointInGame = 12 - (cMinutes + (cSeconds / 60)) + ((Period - 1) * 12)
    return PointInGame