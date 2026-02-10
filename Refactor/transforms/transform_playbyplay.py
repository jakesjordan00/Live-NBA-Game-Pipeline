import config.data_map
from transforms import transform_stints
import pandas as pd
import polars as pl
import unicodedata

class Transform:

    def __init__(self, pipeline):
        self.pipeline = pipeline
        pass

    def playbyplay(self, data_extract_full):
        scoreboard_data = self.pipeline.Data['scoreboard_data']
        boxscore_data = self.pipeline.Data['boxscore_data']
        playbyplay_data, sub_groups = transform_stints.DetermineSubstitutions(data_extract_full, boxscore_data)
        start_action = self.pipeline.start_action
        transformed_playbyplay = TransformPlayByPlay(playbyplay_data, boxscore_data, start_action)
        stints = transform_stints.Stints(playbyplay_data, transformed_playbyplay, sub_groups, start_action,  boxscore_data)
        return transformed_playbyplay




    

def TransformPlayByPlay(playbyplay_data: list, boxscore_data: dict, start_action: int):
    transformed_playbyplay = []
    gameTime = 48 if boxscore_data['GameExt']['Periods'] <= 4 else (5 * (boxscore_data['GameExt']['Periods'] - 4))


    for i, action in enumerate(playbyplay_data[start_action:]):
        SeasonID = boxscore_data['SeasonID']
        GameID = boxscore_data['GameID']
        ActionID = int(i + 1) if start_action == 0 else int(i + 1 + start_action)
        ActionNumber = action['actionNumber']
        Qtr = action['period']
        Clock = action['clock'].replace('PT', '').replace('M', ':').replace('S', '')
        # PointInGame = CalculatePointInGame(Clock, Qtr)
        PointInGame = action['PointInGame']
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
        # test = transform_stints.Stint(action, transformed_action, transformed_playbyplay, HomeID, AwayID, home, away)

        transformed_playbyplay.append(transformed_action)
        bp = 'here'
    return transformed_playbyplay




def CalculatePointInGame(Clock: str, Period: int):
    cMinutes = int(Clock[0:2])
    cSeconds = float(Clock[-5:])
    PointInGame = 12 - (cMinutes + (cSeconds / 60)) + ((Period - 1) * 12)
    return PointInGame

