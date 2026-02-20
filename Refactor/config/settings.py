

import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).parent.parent.parent / 'Drivers' / '.env')


DATABASES = {
    'JJsNBA':{
        'server': os.getenv('ServerIP'),
        'database': os.getenv('Database'),
        'username': 'jjAdmin',
        'password': os.getenv('AdminPass'),
        'Tables':{
            'Team':{
                'keys': ['SeasonID', 'TeamID',],
                'columns': ['SeasonID',
                    'TeamID',
                    'City',
                    'Name',
                    'Tricode',
                    'Wins',
                    'Losses',
                    'FullName',
                    'Conference',
                    'Division'
                ],
                'update_columns': ['Wins', 'Losses']
            },
            'Arena':{
                'keys': ['SeasonID', 'ArenaID'],
                'columns': [
                    'SeasonID',
                    'ArenaID',
                    'TeamID',
                    'City',
                    'Country',
                    'Name',
                    'PostalCode',
                    'State',
                    'StreetAddress',
                    'Timezone'
                ],
                'update_columns': []
            },
            'Official':{
                'keys': ['SeasonID', 'OfficialID'],
                'columns': [
                    'SeasonID',
                    'OfficialID',
                    'Name',
                    'Number'
                ],
                'update_columns': []
            },
            'Player':{
                'keys': ['SeasonID', 'PlayerID'],
                'columns': [
                    'SeasonID',
                    'PlayerID',
                    'Name',
                    'Number',
                    'Position',
                    'NameInitial',
                    'NameLast',
                    'NameFirst'
                ],
                'update_columns': []
            },
            'Game':{
                'keys': ['SeasonID', 'GameID'],
                'columns':[
                    'SeasonID',
                    'GameID',
                    'Date',
                    'GameType',
                    'HomeID',
                    'HScore',
                    'AwayID',
                    'AScore',
                    'WinnerID',
                    'WScore',
                    'LoserID',
                    'LScore',
                    'SeriesID',
                    'Datetime',
                ],
                'update_columns':[
                    'HScore', 
                    'AScore', 
                    'WinnerID', 
                    'WScore', 
                    'LoserID', 
                    'LScore'
                ]
            },
            'GameExt':{
                'keys': ['SeasonID', 'GameID'],
                'columns':[
                    'SeasonID',
                    'GameID',
                    'ArenaID', 
                    'Attendance', 
                    'Sellout', 
                    'Label', 
                    'LabelDetail', 
                    'OfficialID', 
                    'Official2ID', 
                    'Official3ID', 
                    'OfficialAlternateID', 
                    'Status', 
                    'Periods'
                ],
                'update_columns':[
                    'Attendance', 
                    'Sellout', 
                    'Label', 
                    'LabelDetail', 
                    'Status', 
                    'Periods'
                ]
            },
            'TeamBox':{
                'keys':['SeasonID', 'GameID', 'TeamID', 'MatchupID'],
                'columns':[
                    'SeasonID',
                    'GameID',
                    'TeamID',
                    'MatchupID',
                    'Points',
                    'PointsAgainst',
                    'FG2M',
                    'FG2A',
                    '[FG2%]',
                    'FG3M',
                    'FG3A',
                    '[FG3%]',
                    'FGM',
                    'FGA',
                    '[FG%]',
                    'FieldGoalsEffectiveAdjusted',
                    'FTM',
                    'FTA',
                    '[FT%]',
                    'SecondChanceFGM',
                    'SecondChanceFGA',
                    '[SecondChanceFG%]',
                    'TrueShootingAttempts',
                    'TrueShootingPercentage',
                    'PtsFromTurnovers',
                    'PtsSecondChance',
                    'PtsInThePaint',
                    'PaintFGM',
                    'PaintFGA',
                    '[PaintFG%]',
                    'PtsFastBreak',
                    'FastBreakFGM',
                    'FastBreakFGA',
                    '[FastBreakFG%]',
                    'BenchPoints',
                    'ReboundsDefensive',
                    'ReboundsOffensive',
                    'ReboundsPersonal',
                    'ReboundsTeam',
                    'ReboundsTeamDefensive',
                    'ReboundsTeamOffensive',
                    'ReboundsTotal',
                    'Assists',
                    'AssistsTurnoverRatio',
                    'BiggestLead',
                    'BiggestLeadScore',
                    'BiggestScoringRun',
                    'BiggestScoringRunScore',
                    'TimeLeading',
                    'TimesTied',
                    'LeadChanges',
                    'Steals',
                    'Turnovers',
                    'TurnoversTeam',
                    'TurnoversTotal',
                    'Blocks',
                    'BlocksReceived',
                    'FoulsDrawn',
                    'FoulsOffensive',
                    'FoulsPersonal',
                    'FoulsTeam',
                    'FoulsTeamTechnical',
                    'FoulsTechnical',
                    'Wins',
                    'Losses',
                    'Win',
                    'Seed'
                ],
                'update_columns': [
                    'Points',
                    'PointsAgainst',
                    'FG2M',
                    'FG2A',
                    '[FG2%]',
                    'FG3M',
                    'FG3A',
                    '[FG3%]',
                    'FGM',
                    'FGA',
                    '[FG%]',
                    'FieldGoalsEffectiveAdjusted',
                    'FTM',
                    'FTA',
                    '[FT%]',
                    'SecondChanceFGM',
                    'SecondChanceFGA', 
                    '[SecondChanceFG%]',
                    'TrueShootingAttempts',
                    'TrueShootingPercentage',
                    'PtsFromTurnovers',
                    'PtsSecondChance',
                    'PtsInThePaint',
                    'PaintFGM',
                    'PaintFGA',
                    '[PaintFG%]',
                    'PtsFastBreak',
                    'FastBreakFGM',
                    'FastBreakFGA',
                    '[FastBreakFG%]',
                    'BenchPoints',
                    'ReboundsDefensive',
                    'ReboundsOffensive',
                    'ReboundsPersonal',
                    'ReboundsTeam',
                    'ReboundsTeamDefensive',
                    'ReboundsTeamOffensive',
                    'ReboundsTotal',
                    'Assists',
                    'AssistsTurnoverRatio',
                    'BiggestLead',
                    'BiggestLeadScore',
                    'BiggestScoringRun',
                    'BiggestScoringRunScore',
                    'TimeLeading',
                    'TimesTied',
                    'LeadChanges',
                    'Steals',
                    'Turnovers',
                    'TurnoversTeam',
                    'TurnoversTotal',
                    'Blocks',
                    'BlocksReceived',
                    'FoulsDrawn',
                    'FoulsOffensive',
                    'FoulsPersonal',
                    'FoulsTeam',
                    'FoulsTeamTechnical',
                    'FoulsTechnical',
                    'Wins', 
                    'Losses',
                    'Win',
                    'Seed'
                ]
            },
            'PlayerBox':{
                'keys': ['SeasonID', 'GameID', 'TeamID', 'MatchupID', 'PlayerID'],
                'columns': [
                    'SeasonID',
                    'GameID',
                    'TeamID',
                    'MatchupID',
                    'PlayerID',
                    'Status',
                    'Starter', 
                    'Position', 
                    'Minutes', 
                    'MinutesCalculated', 
                    'Points',
                    'Assists',
                    'ReboundsTotal',
                    'FG2M',
                    'FG2A',
                    '[FG2%]',
                    'FG3M', 
                    'FG3A',
                    '[FG3%]',
                    'FGM', 
                    'FGA', 
                    '[FG%]', 
                    'FTM', 
                    'FTA', 
                    '[FT%]', 
                    'ReboundsDefensive', 
                    'ReboundsOffensive', 
                    'Blocks', 
                    'BlocksReceived', 
                    'Steals', 
                    'Turnovers', 
                    'AssistsTurnoverRatio', 
                    'Plus', 
                    'Minus', 
                    'PlusMinusPoints',
                    'PtsFastBreak',
                    'PtsInThePaint',
                    'PtsSecondChance', 
                    'FoulsOffensive', 
                    'FoulsDrawn', 
                    'FoulsPersonal', 
                    'FoulsTechnical', 
                    'StatusReason', 
                    'StatusDescription'

                ],
                'update_columns': [
                    'Status',
                    'Starter',
                    'Position',
                    'Minutes',
                    'MinutesCalculated',
                    'Points',
                    'Assists',
                    'ReboundsTotal',
                    'FG2M',
                    'FG2A',
                    '[FG2%]',
                    'FG3M',
                    'FG3A',
                    '[FG3%]',
                    'FGM',
                    'FGA',
                    '[FG%]',
                    'FTM',
                    'FTA',
                    '[FT%]',
                    'ReboundsDefensive',
                    'ReboundsOffensive',
                    'Blocks',
                    'BlocksReceived',
                    'Steals',
                    'Turnovers',
                    'AssistsTurnoverRatio',
                    'Plus',
                    'Minus',
                    'PlusMinusPoints',
                    'PtsFastBreak',
                    'PtsInThePaint',
                    'PtsSecondChance',
                    'FoulsOffensive',
                    'FoulsDrawn',
                    'FoulsPersonal',
                    'FoulsTechnical',
                    'StatusReason',
                    'StatusDescription'
                ]
            },    
            'StartingLineups':{
                'keys': ['SeasonID', 'GameID', 'TeamID', 'MatchupID', 'PlayerID'],
                'columns': [
                    'SeasonID',
                    'GameID',
                    'TeamID',
                    'MatchupID',
                    'PlayerID',
                    'Unit',
                    'Position'
                ],
                'update_columns': []
            },
            'PlayByPlay':{
                # 'keys': ['SeasonID', 'GameID', 'ActionID', 'ActionNumber'],
                'keys': [],
                'columns': [
                    'SeasonID',
                    'GameID',
                    'ActionID',
                    'ActionNumber',
                    'Qtr',
                    'Clock',
                    'TimeActual',
                    'ScoreHome',
                    'ScoreAway',
                    'Possession',
                    'TeamID',
                    'Tricode',
                    'PlayerID',
                    'Description',
                    'SubType',
                    'IsFieldGoal',
                    'ShotResult',
                    'ShotValue',
                    'ActionType',
                    'ShotDistance',
                    'Xlegacy',
                    'Ylegacy',
                    'X',
                    'Y',
                    'Location',
                    'Area',
                    'AreaDetail',
                    'Side',
                    'ShotType',
                    'PtsGenerated',
                    'Descriptor',
                    'Qual1',
                    'Qual2',
                    'Qual3',
                    'ShotActionNbr',
                    'PlayerIDAst',
                    'PlayerIDBlk',
                    'PlayerIDStl',
                    'PlayerIDFoulDrawn',
                    'PlayerIDJumpW',
                    'PlayerIDJumpL',
                    'OfficialID',
                    'QtrType'
                ],
                'update_columns': [],
                'check_query': '''select count(p.ActionID) Actions
	 , max(ActionNumber) LastActionNumber
from PlayByPlay p
where p.SeasonID = season_id and p.GameID = game_id'''
            },
            'jjs.Stint':{
                'keys': ['SeasonID', 'GameID', 'TeamID', 'StintID'],
                'columns': [
                    'SeasonID',
                    'GameID',
                    'TeamID',
                    'StintID',
                    'QtrStart',
                    'QtrEnd',
                    'ClockStart',
                    'ClockEnd',
                    'MinElapsedStart',
                    'MinElapsedEnd',
                    'MinutesPlayed',
                    'Possessions',
                    'PtsScored',
                    'PtsAllowed',
                    'FG2M',
                    'FG2A',
                    'FG3M',
                    'FG3A',
                    'FGM',
                    'FGA',
                    'FTM',
                    'FTA',
                    'OREB',
                    'DREB',
                    'REB',
                    'AST',
                    'TOV',
                    'STL',
                    'BLK',
                    'BLKd',
                    'F',
                    'FDrwn'
                ],
                'update_columns': [
                    'QtrEnd',
                    'ClockEnd',
                    'MinElapsedEnd',
                    'MinutesPlayed',
                    'Possessions',
                    'PtsScored',
                    'PtsAllowed',
                    'FG2M',
                    'FG2A',
                    'FG3M',
                    'FG3A',
                    'FGM',
                    'FGA',
                    'FTM',
                    'FTA',
                    'OREB',
                    'DREB',
                    'REB',
                    'AST',
                    'TOV',
                    'STL',
                    'BLK',
                    'BLKd',
                    'F',
                    'FDrwn'
                ],
                'check_query':
                '''
with TeamsOnCourt as(
select s.*
	 , dense_rank() over(partition by TeamID order by StintID desc) OnCourt
from jjs.Stint s
where s.SeasonID = season_id and s.GameID = game_id
)
select *
from TeamsOnCourt
where OnCourt = 1
order by OnCourt asc,TeamID'''
            },
            'jjs.StintPlayer':{
                'keys': ['SeasonID', 'GameID', 'TeamID', 'StintID', 'PlayerID'],
                'columns': [
                    'SeasonID',
                    'GameID',
                    'TeamID',
                    'StintID',
                    'PlayerID',
                    'MinutesPlayed',
                    'PlusMinus',
                    'PTS',
                    'AST',
                    'REB',
                    'FG2M',
                    'FG2A',
                    'FG3M',
                    'FG3A',
                    'FGM',
                    'FGA',
                    'FTM',
                    'FTA',
                    'OREB',
                    'DREB',
                    'TOV',
                    'STL',
                    'BLK',
                    'BLKd',
                    'F',
                    'FDrwn'
                ],
                'update_columns': [
                    'MinutesPlayed',
                    'PlusMinus',
                    'PTS',
                    'AST',
                    'REB',
                    'FG2M',
                    'FG2A',
                    'FG3M',
                    'FG3A',
                    'FGM',
                    'FGA',
                    'FTM',
                    'FTA',
                    'OREB',
                    'DREB',
                    'TOV',
                    'STL',
                    'BLK',
                    'BLKd',
                    'F',
                    'FDrwn'
                ],
                'check_query': '''
with PlayersOnCourt as(
select sp.*
	 , dense_rank() over(partition by TeamID order by StintID desc) OnCourt
from jjs.StintPlayer sp
where sp.SeasonID = season_id and sp.GameID = game_id
)
select *
from PlayersOnCourt
where OnCourt = 1
order by OnCourt asc,TeamID, PlayerID
'''
            },
            'Schedule': {
                'check_query': '''
select s.SeasonID
     , s.GameID
     , s.Status
     , s.HomeID
     , h.Name HomeName
     , h.City HomeCity
     , h.Tricode HomeTri
     , s.HomeWins
     , s.HomeLosses
     , s.HomeScore
     , s.HomeSeed
     , s.AwayID
     , a.Name AwayName
     , a.City AwayCity
     , a.Tricode AwayTri
     , s.AwayWins
     , s.AwayLosses
     , s.AwayScore
     , s.AwaySeed
     , s.IfNecessary
     , s.SeriesText
from Schedule s
left join Team h on s.SeasonID = h.SeasonID and s.HomeID = h.TeamID
left join Team a on s.SeasonID = a.SeasonID and s.AwayID = a.TeamID
where s.SeasonID = season_id and s.GameID in(game_id)
'''
            }
        }
    }
}

TABLES = {
    
}