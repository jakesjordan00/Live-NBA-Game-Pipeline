

#region Game and GameExt
keys_Game = ['SeasonID', 'GameID']
columns_Game = ['SeasonID', 'GameID', 'Date', 'GameType', 'HomeID', 'HScore', 'AwayID', 'AScore',
                'WinnerID', 'WScore', 'LoserID', 'LScore', 'SeriesID', 'Datetime']
updateColumns_Game = ['HScore', 'AScore', 'WinnerID', 'WScore', 'LoserID', 'LScore']


columns_GameExt = ['SeasonID', 'GameID', 'ArenaID', 'Attendance', 'Sellout', 'Label', 'LabelDetail', 
    'OfficialID', 'Official2ID', 'Official3ID', 'OfficialAlternateID', 'Status', 'Periods']
updateColumns_GameExt = ['Attendance', 'Sellout', 'Label', 'LabelDetail', 'Status', 'Periods']
#endregion GameExt

#region TeamBox
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

updateColumns_TeamBox = ['Points', 'PointsAgainst', 'FG2M', 'FG2A', '[FG2%]', 'FG3M', 'FG3A', '[FG3%]', 'FGM', 'FGA', '[FG%]', 'FieldGoalsEffectiveAdjusted', 'FTM', 'FTA', '[FT%]', 'SecondChancePointsMade', 'SecondChancePointsAttempted', 
'SecondChancePointsPercentage', 'TrueShootingAttempts', 'TrueShootingPercentage', 'PointsFromTurnovers', 'PointsSecondChance', 'PointsInThePaint', 'PointsInThePaintMade', 'PointsInThePaintAttempted', 'PointsInThePaintPercentage', 'PointsFastBreak', 'FastBreakPointsMade', 'FastBreakPointsAttempted', 'FastBreakPointsPercentage', 'BenchPoints', 'ReboundsDefensive', 'ReboundsOffensive', 'ReboundsPersonal', 'ReboundsTeam', 'ReboundsTeamDefensive', 'ReboundsTeamOffensive', 'ReboundsTotal', 'Assists', 'AssistsTurnoverRatio', 'BiggestLead', 'BiggestLeadScore', 'BiggestScoringRun', 'BiggestScoringRunScore', 'TimeLeading', 'TimesTied', 'LeadChanges', 'Steals', 'Turnovers', 'TurnoversTeam', 'TurnoversTotal', 'Blocks', 'BlocksReceived', 'FoulsDrawn', 'FoulsOffensive', 'FoulsPersonal', 'FoulsTeam', 'FoulsTeamTechnical', 'FoulsTechnical', 'Wins', 
'Losses', 'Win', 'Seed']
#endregion TeamBox


columns_PlayerBox = ['SeasonID', 'GameID', 'TeamID', 'MatchupID', 'PlayerID', 'Status', 'Starter', 'Position', 'Minutes', 'MinutesCalculated', 
            'Points', 'Assists', 'ReboundsTotal', 'FG2M', 'FG2A', 'FG2%', 'FG3M', 'FG3A', 'FG3%', 'FGM', 'FGA', 'FG%', 'FTM', 'FTA', 'FT%', 'ReboundsDefensive', 'ReboundsOffensive', 'Blocks', 'BlocksReceived', 'Steals', 'Turnovers', 'AssistsTurnoverRatio', 'Plus', 'Minus', 'PlusMinusPoints', 'PointsFastBreak', 'PointsInThePaint', 'PointsSecondChance', 'FoulsOffensive', 'FoulsDrawn', 'FoulsPersonal', 
            'FoulsTechnical', 'StatusReason', 'StatusDescription']
updateColumns_PlayerBox = ['Status', 'Starter', 'Position', 'Minutes', 'MinutesCalculated', 'Points', 'Assists', 'ReboundsTotal', 'FG2M', 'FG2A', 
'[FG2%]', 'FG3M', 'FG3A', '[FG3%]', 'FGM', 'FGA', '[FG%]', 'FTM', 'FTA', '[FT%]', 'ReboundsDefensive', 'ReboundsOffensive', 'Blocks', 'BlocksReceived', 'Steals', 'Turnovers', 'AssistsTurnoverRatio', 'Plus', 'Minus', 'PlusMinusPoints', 'PointsFastBreak', 'PointsInThePaint', 'PointsSecondChance', 'FoulsOffensive', 'FoulsDrawn', 'FoulsPersonal', 'FoulsTechnical', 'StatusReason', 'StatusDescription']





columns_PlayByPlay = ['SeasonID', 'GameID', 'ActionID', 'ActionNumber', 'Qtr', 'Clock', 'TimeActual', 'ScoreHome', 'ScoreAway', 'Possession', 'TeamID', 'Tricode', 'PlayerID', 'Description', 'SubType', 'IsFieldGoal', 'ShotResult', 'ShotValue', 'ActionType', 'ShotDistance', 'Xlegacy', 'Ylegacy', 'X', 'Y', 'Location', 'Area', 'AreaDetail', 'Side', 'ShotType', 'PtsGenerated', 'Descriptor', 'Qual1', 'Qual2', 'Qual3', 'ShotActionNbr', 'PlayerIDAst', 'PlayerIDBlk', 'PlayerIDStl', 
                   'PlayerIDFoulDrawn', 'PlayerIDJumpW', 'PlayerIDJumpL', 'OfficialID', 'QtrType']

columns_StartingLineups = ['SeasonID', 'GameID', 'TeamID', 'MatchupID', 'PlayerID', 'Unit', 'Position']





columns_Arena = ['SeasonID', 'ArenaID', 'TeamID', 'City', 'Country', 'Name', 'PostalCode', 'State', 'StreetAddress', 'Timezone']
