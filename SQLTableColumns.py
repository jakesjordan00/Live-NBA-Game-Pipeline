columns_Game = ['SeasonID', 'GameID','Date', 'GameType', 'HomeID', 'HScore', 'AwayID', 'AScore',
                'WinnerID', 'WScore', 'LoserID', 'LScore', 'SeriesID', 'Datetime']
keys_Game = ['SeasonID', 'GameID']

columns_GameExt = ['SeasonID', 'GameID', 'ArenaID', 'Attendance', 'Sellout', 'Label', 'LabelDetail', 
    'OfficialID', 'Official2ID', 'Official3ID', 'OfficialAlternateID', 'Status', 'Periods']
keys_GameExt = ['SeasonID', 'GameID']

columns_TeamBox = ['SeasonID', 'GameID', 'TeamID', 'MatchupID', 'Points', 'PointsAgainst', 'FG2M', 'FG2A', 'FG2%', 'FG3M', 'FG3A', 'FG3%', 
            'FGM', 'FGA', 'FG%', 'FieldGoalsEffectiveAdjusted', 'FTM', 'FTA', 'FT%', 'SecondChancePointsMade', 'SecondChancePointsAttempted', 
            'SecondChancePointsPercentage', 'TrueShootingAttempts', 'TrueShootingPercentage', 'PointsFromTurnovers', 'PointsSecondChance', 
            'PointsInThePaint', 'PointsInThePaintMade', 'PointsInThePaintAttempted', 'PointsInThePaintPercentage', 'PointsFastBreak', 
            'FastBreakPointsMade', 'FastBreakPointsAttempted', 'FastBreakPointsPercentage', 'BenchPoints', 'ReboundsDefensive', 
            'ReboundsOffensive', 'ReboundsPersonal', 'ReboundsTeam', 'ReboundsTeamDefensive', 'ReboundsTeamOffensive', 'ReboundsTotal', 
            'Assists', 'AssistsTurnoverRatio', 'BiggestLead', 'BiggestLeadScore', 'BiggestScoringRun', 'BiggestScoringRunScore', 
            'TimeLeading', 'TimesTied', 'LeadChanges', 'Steals', 'Turnovers', 'TurnoversTeam', 'TurnoversTotal', 'Blocks', 'BlocksReceived', 
            'FoulsDrawn', 'FoulsOffensive', 'FoulsPersonal', 'FoulsTeam', 'FoulsTeamTechnical', 'FoulsTechnical', 'Wins', 
            'Losses', 'Win', 'Seed']
keys_TeamBox = ['SeasonID', 'GameID', 'TeamID', 'MatchupID']

columns_PlayerBox = ['SeasonID', 'GameID', 'TeamID', 'MatchupID', 'PlayerID', 'Status', 'Starter', 'Position', 'Minutes', 'MinutesCalculated', 
            'Points', 'Assists', 'ReboundsTotal', 'FG2M', 'FG2A', 'FG2%', 'FG3M', 'FG3A', 'FG3%', 'FGM', 'FGA', 'FG%', 'FTM', 'FTA', 'FT%', 'ReboundsDefensive', 'ReboundsOffensive', 'Blocks', 'BlocksReceived', 'Steals', 'Turnovers', 'AssistsTurnoverRatio', 'Plus', 'Minus', 'PlusMinusPoints', 'PointsFastBreak', 'PointsInThePaint', 'PointsSecondChance', 'FoulsOffensive', 'FoulsDrawn', 'FoulsPersonal', 
            'FoulsTechnical', 'StatusReason', 'StatusDescription']
keys_PlayerBox = ['SeasonID', 'GameID', 'TeamID', 'MatchupID', 'PlayerID']

columns_PlayByPlay = ['SeasonID', 'GameID', 'ActionID', 'ActionNumber', 'Qtr', 'Clock', 'TimeActual', 'ScoreHome', 'ScoreAway', 'Possession', 'TeamID', 'Tricode', 'PlayerID', 'Description', 'SubType', 'IsFieldGoal', 'ShotResult', 'ShotValue', 'ActionType', 'ShotDistance', 'Xlegacy', 'Ylegacy', 'X', 'Y', 'Location', 'Area', 'AreaDetail', 'Side', 'ShotType', 'PtsGenerated', 'Descriptor', 'Qual1', 'Qual2', 'Qual3', 'ShotActionNbr', 'PlayerIDAst', 'PlayerIDBlk', 'PlayerIDStl', 
                   'PlayerIDFoulDrawn', 'PlayerIDJumpW', 'PlayerIDJumpL', 'OfficialID', 'QtrType']
keys_PlayByPlay = ['SeasonID', 'GameID', 'ActionID', 'ActionNumber']

columns_StartingLineups = ['SeasonID', 'GameID', 'TeamID', 'MatchupID', 'PlayerID', 'Unit', 'Position']
keys_StartingLineups=['SeasonID', 'GameID', 'TeamID', 'MatchupID', 'PlayerID']
