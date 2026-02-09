import config.data_map
import pandas as pd
import polars as pl


class Transform:

    def __init__(self, pipeline):
        self.pipeline = pipeline
        pass

    def playbyplay(self, data_extract_full):
        playbyplay_data = ConsolidateSources(data_extract_full)
        scoreboard_data = self.pipeline.Data['scoreboard_data']
        boxscore_data = self.pipeline.Data['boxscore_data']
        start_action = self.pipeline.start_action
        transformed_playbyplay = TransformPlayByPlay(playbyplay_data, scoreboard_data, boxscore_data, start_action)
        return transformed_playbyplay

def ConsolidateSources(data_extract_full: dict):
    static_data_extract = data_extract_full['static_data_extract']
    api_data_extract = data_extract_full['api_data_extract']
    static_playbyplay_data = static_data_extract['game']['actions']
    api_playbyplay_data = api_data_extract['game']['actions']

    tde = static_data_extract['game']['actions']
    tad = api_data_extract['game']['actions']

    test_tde = pd.DataFrame(tde)
    test_tad = pd.DataFrame(tad)
    test_tad['actionType'] = test_tad['actionType'].str.lower()


    test_left = test_tde.merge(test_tad[['actionType', 'personId', 'clock', 'period', 'description', 'actionNumber']], on=['actionType', 'personId', 'clock', 'period'], how='left', suffixes=('', '_api'))
            

    mask_out = (test_left['actionType'] == 'substitution')
    sub_out = test_left[[
        'actionNumber','period','clock', 
        'personId', 'playerName', 'playerNameI', 
        'description', 'description_api',
        'actionType', 'subType',
        'scoreHome', 'scoreAway',
    ]][mask_out]

    sub_out['description_api'] = sub_out['description_api'].fillna('')
    sub_out['description_sub_in'] = sub_out.apply(
        lambda row: (
            row['description_api']
            .replace(':', ' in:')
            .replace(' FOR ', '')
            .replace(row['playerName'], '')
        ), 
        axis=1
    )        
    
    mask_in = (test_left['actionType'] == 'substitution') & (test_left['subType'] == 'in')
    sub_in = test_left[[
        'actionNumber','period','clock', 
        'personId', 'playerName', 'playerNameI', 
        'description',
        'actionType', 'subType',
        'scoreHome', 'scoreAway',
    ]][mask_in]
    sub_in['description_sub_in'] = sub_in.apply(
        lambda row:(
        row['description'].replace(row['playerNameI'], row['playerName'])
        ),
        axis = 1
    )


    combined = sub_out.merge(sub_in, how='left', on = ['period','clock', 'scoreHome', 'scoreAway', 'actionType', 'description_sub_in']
                                , suffixes=('_dfOut', '_dfIn'))
    combined['description_dfIn'] = combined['description_dfIn'].fillna('')

    print(f'Sub out: {sub_out['description_sub_in'].iloc[0]}')
    print(f'Sub in:  {sub_in['description_sub_in'].iloc[0]}')


    matched_sub_in = combined[combined['actionNumber_dfIn'].notna()]['actionNumber_dfIn'].values
    combined = combined[~(
        (combined['subType_dfOut'] == 'in') & 
        (combined['actionNumber_dfIn'].isna()) & 
        (combined['actionNumber_dfOut'].isin(matched_sub_in))
    )]

    bp = 'here'
    for i, row in combined.iterrows():
        if row['actionType'] == 'substitution':
            print(f'{row['actionNumber_dfOut']} - {row['description_dfOut']}'
                    + f'{(35 - len(row['description_dfOut'])) * ' '}'
                    + f'{row['actionNumber_dfIn']} - {row['description_dfIn']}'
                    + f'{(35 - len(row['description_dfIn'])) * ' '}'
                    + f'API: {row['description_api']}')
            
    bp = 'here'
            



    playbyplay_data = []
    return playbyplay_data






def TransformPlayByPlay(playbyplay_data: list, scoreboard_data: dict, boxscore_data: dict, start_action: int):
    transformed_playbyplay = []
    final_action = playbyplay_data[-1]
    gameTime = 48 if boxscore_data['GameExt']['Periods'] <= 4 else (5 * (boxscore_data['GameExt']['Periods'] - 4))

    if start_action == 0:
        HomeID = boxscore_data['Game']['HomeID']
        AwayID = boxscore_data['Game']['AwayID']
        lineups = boxscore_data['StartingLineups']
        home = set(player['PlayerID'] for player in lineups if player['TeamID'] == HomeID and player['Unit'] == 'Starters')
        away = set(player['PlayerID'] for player in lineups if player['TeamID'] == AwayID and player['Unit'] == 'Starters')
        bp = 'here'

    for i, action in enumerate(playbyplay_data[start_action:]):
        SeasonID = boxscore_data['SeasonID']
        GameID = boxscore_data['GameID']
        ActionID = int(i + 1) if start_action == 0 else int(i + 1 + start_action)
        ActionNumber = action['actionNumber']
        Qtr = action['period']
        Clock = action['clock'].replace('PT', '').replace('M', ':').replace('S', '')
        PointInGame = CalculatePointInGame(Clock, Qtr)
        TimeActual = action['timeActual']
        ScoreHome = action['scoreHome']
        ScoreAway = action['scoreAway']
        Possession = action.get('possession') if action.get('possession') != 0 else None
        TeamID = action.get('teamId')
        Tricode = action.get('teamTricode')
        PlayerID = action.get('personId') if action.get('personId') != 0 else None 
        Description = action.get('description').replace("'", "''")
        SubType = action['subType'] if action['subType'] != '' else None
        IsFieldGoal = action.get('isFieldGoal') if action.get('isFieldGoal') == 1 else None
        ShotResult = action.get('shotResult')
        ShotValue = int(action['actionType'][0]) if ShotResult != None and action['actionType'] != 'freethrow' else 1 if action['actionType'] == 'freethrow' else None
        ActionType = action['actionType']
        ShotDistance = action.get('shotDistance')
        XLegacy = action.get('xLegacy')
        YLegacy = action.get('yLegacy')
        X = action.get('x')        
        Y = action.get('y')
        Area = action.get('area')
        AreaDetail = action.get('areaDetail')
        Side = action['side']
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
        Descriptor = action.get('descriptor')
        ShotActionNbr = action.get('shotActionNbr')
        Qual1 = action['qualifiers'][0] if 'qualifiers' in action.keys() and len(action['qualifiers']) > 0 else None
        Qual2 = action['qualifiers'][1] if 'qualifiers' in action.keys() and len(action['qualifiers']) > 1 else None
        Qual3 = action['qualifiers'][2] if 'qualifiers' in action.keys() and len(action['qualifiers']) > 2 else None
        PlayerIDAst = action.get('assistPersonId')
        PlayerIDBlk = action.get('blockPersonId')
        PlayerIDStl = action.get('stealPersonId')
        PlayerIDFoulDrawn = action.get('foulDrawnPersonId')
        PlayerIDJumpW = action.get('jumpBallWonPersonId')
        PlayerIDJumpL = action.get('jumpBallLostPersonId')
        OfficialID = action.get('officialId')
        QtrType = action['periodType']


        if ActionType == 'substitution':
            bp = 'here'
        if TeamID == HomeID and PlayerID in home and ActionType == 'substitution' and SubType == 'out':
            bp = 'here'
        if TeamID == HomeID and PlayerID not in home and PlayerID != None:
            bp = 'here'

        transformed_action = {
                'SeasonID': SeasonID,
                'GameID': GameID,
                'ActionID': ActionID,
                'ActionNumber': ActionNumber,
                'PointInGame': PointInGame,
                'Qtr': Qtr,
                'Clock': Clock,
                'TimeActual': TimeActual,
                'ScoreHome': ScoreHome,
                'ScoreAway': ScoreAway,
                'Possession': Possession,
                'TeamID': TeamID,
                'Tricode': Tricode,
                'PlayerID': PlayerID,
                'Description': Description,
                'SubType': SubType,
                'IsFieldGoal': IsFieldGoal,
                'ShotResult': ShotResult,
                'ShotValue': ShotValue,
                'ActionType': ActionType,
                'ShotDistance': ShotDistance,
                'Xlegacy': XLegacy,
                'Ylegacy': YLegacy,
                'X': X,
                'Y': Y,
                'Location': None,
                'Area': Area,
                'AreaDetail': AreaDetail,
                'Side': Side,
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
                'QtrType': QtrType
        }

        transformed_playbyplay.append(transformed_action)
        bp = 'here'
    return transformed_playbyplay




def CalculatePointInGame(Clock: str, Period: int):
    cMinutes = int(Clock[0:2])
    cSeconds = float(Clock[-5:])
    PointInGame = 12 - (cMinutes + (cSeconds / 60)) + ((Period - 1) * 12)
    return PointInGame