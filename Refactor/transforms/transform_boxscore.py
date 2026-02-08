import config.mappings
from typing import Any
from datetime import datetime

class Transform:


    def __init__(self, pipeline):
        self.pipeline = pipeline
        pass
    
    def box(self, data_extract):
        box_data = data_extract['game']
        scoreboard_data = self.pipeline.Data

        transformed_data = TransformBox(box_data, scoreboard_data)


        return transformed_data

    

def TransformBox(box_data: dict, scoreboard_data: dict) -> dict:
    SeasonID = 2000 + int(box_data['gameId'][3:5])
    box_data['SeasonID'] = SeasonID
    box_data['GameID'] = scoreboard_data['GameID']

    #Teams
    HomeID = box_data['homeTeam']['teamId']
    AwayID = box_data['awayTeam']['teamId']
    teams = [
        (box_data['homeTeam'], scoreboard_data['HomeTeam'], HomeID, AwayID, 'homeTeam', box_data), 
        (box_data['awayTeam'], scoreboard_data['AwayTeam'], AwayID, HomeID, 'awayTeam', box_data)
    ]
    formatted_team_list = []
    formatted_teambox_list = []
    formatted_player_list = []
    formatted_playerbox_list = []
    formatted_startinglineups_list = []
    for teamBox, teamScoreboard, TeamID, MatchupID, selector, box_data in teams:
        prepared_team = PrepareTeam(teamBox, teamScoreboard, TeamID, MatchupID, selector, box_data)

        formatted_team_list.append(prepared_team['Team'])
        formatted_teambox_list.append(prepared_team['TeamBox'])
        for player in prepared_team['Players']:
            formatted_player_list.append(player['Player'])
            formatted_playerbox_list.append(player['PlayerBox'])
            formatted_startinglineups_list.append(player['StartingLineups'])

    formatted_officials = FormatOfficial(box_data['officials'])
    formatted_arena = FormatArena(box_data['arena'], SeasonID, HomeID if not scoreboard_data['IsNeutral'] else None)
    formatted_game, formatted_gameExt = FormatGame(box_data, scoreboard_data, formatted_officials, formatted_arena['ArenaID'])

    prepared_box_data = {
        'SeasonID': 2000 + int(box_data['gameId'][3:5]),
        'GameID': scoreboard_data['GameID'],
        'Game': formatted_game,
        'GameExt': formatted_gameExt,
        'Team': formatted_team_list,
        'TeamBox': formatted_teambox_list,
        'Player': formatted_player_list,
        'PlayerBox': formatted_playerbox_list,
        'StartingLineups': formatted_startinglineups_list,
        'Officials': formatted_officials,
        'Arena': formatted_arena,
    }

    return prepared_box_data


#region Game
def FormatGame(box_data: dict, scoreboard_data: dict, officials: list, ArenaID: int) -> tuple[dict[str, Any], dict[str, Any]]:
    DateStr = box_data['gameEt'][:10]
    DatetimeStr = box_data['gameEt'][:-6]
    Date = datetime.strptime(DateStr, '%Y-%m-%d')
    Datetime = datetime.strptime(DatetimeStr, '%Y-%m-%dT%H:%M:%S')



    if box_data['gameId'][2] == '2': #Regular Season
        GameType = 'RS'
        SeriesID = None
    elif box_data['gameId'][2] == '1': #Preseason
        GameType = 'PRE'
        SeriesID = None
    elif box_data['gameId'][2] == '4':
        GameType = 'PS'
        SeriesID = int(box_data['gameId'][2:-1])
    elif box_data['gameId'][2] == '5':
        GameType = 'PI'
        SeriesID = None
    elif box_data['gameId'][2] == '6':
        GameType = 'CUP'
        SeriesID = None

    if box_data['homeTeam']['score'] > box_data['awayTeam']['score'] and box_data['gameStatus'] == 3:
        WinnerID = box_data['homeTeam']['teamId']
        WScore = box_data['homeTeam']['score']
        LoserID = box_data['awayTeam']['teamId']
        LScore = box_data['awayTeam']['score']
    elif box_data['homeTeam']['score'] < box_data['awayTeam']['score'] and box_data['gameStatus'] == 3:
        WinnerID = box_data['awayTeam']['teamId']
        WScore = box_data['awayTeam']['score']
        LoserID = box_data['homeTeam']['teamId']
        LScore = box_data['homeTeam']['score']

    bp = 'here'
    formatted_Game = {
        'SeasonID': box_data['SeasonID'],
        'GameID': box_data['GameID'],
        'Date': Date,
        'GameType': GameType,
        'HomeID': box_data['homeTeam']['teamId'],
        'HScore': box_data['homeTeam']['score'],
        'AwayID': box_data['awayTeam']['teamId'],
        'AScore': box_data['awayTeam']['score'],
        'WinnerID': WinnerID,
        'WScore':  WScore,
        'LoserID': LoserID,
        'LScore':  LScore,
        'SeriesID': SeriesID,
        'Datetime': Datetime,

    }

    bp = 'here'
    formatted_GameExt = {
        'SeasonID': box_data['SeasonID'],
        'GameID': box_data['GameID'],
        'ArenaID': ArenaID,
        'Attendance': box_data['attendance'],
        'Sellout': int(box_data['sellout']),
        'Label': scoreboard_data['GameLabel'] if scoreboard_data['GameLabel'] not in ['', None] else None,
        'LabelDetail': scoreboard_data['GameSubLabel'] if scoreboard_data['GameSubLabel'] not in ['', None] else None,
        'OfficialID': next((o['OfficialID'] for o in officials if o['Assignment'] == 'OFFICIAL1'), None),
        'Official2ID': next((o['OfficialID'] for o in officials if o['Assignment'] == 'OFFICIAL2'), None),
        'Official3ID': next((o['OfficialID'] for o in officials if o['Assignment'] == 'OFFICIAL3'), None),
        'OfficialAlternateID': next((o['OfficialID'] for o in officials if o['Assignment'] == 'ALTERNATE'), None),
        'Status': box_data['gameStatusText'],
        'Periods': 4 if box_data['period'] <= 4 else box_data['period'],
    }
    bp = 'here'

    return formatted_Game, formatted_GameExt
#endregion Game


#region Team data
def PrepareTeam(teamBox: dict, teamScoreboard: dict, TeamID: int, MatchupID: int, selector: str, box_data: dict) -> dict:
    SeasonID = box_data['SeasonID']
    GameID = box_data['GameID']
    name = teamBox['teamName']
    city = teamBox['teamCity']
    tri = teamBox['teamTricode']

    if teamBox['statistics']['points'] > teamBox['statistics']['pointsAgainst'] and box_data['gameStatus'] == 3:
        WinnerID = TeamID
        LoserID = MatchupID
        Win = 1
    elif teamBox['statistics']['points'] < teamBox['statistics']['pointsAgainst'] and box_data['gameStatus'] == 3:
        WinnerID = MatchupID
        LoserID = TeamID
        Win = 0

    Home = 1 if selector == 'homeTeam' else 0
    game_data_payload = {
        'SeasonID': SeasonID,
        'GameID': GameID,
        'TeamID': TeamID,
        'MatchupID': MatchupID,
        'Home': Home,
        'Win': Win
    }

    conf_div = config.mappings.team_map[teamBox['teamId']]
    prepared_team = {
        'TeamID': teamBox['teamId'],
        'Team': {
            'SeasonID': SeasonID,
            'TeamID': teamBox['teamId'],
            'City': city,
            'Name': name,
            'Tricode': tri,
            'Wins': teamScoreboard['wins'],
            'Losses': teamScoreboard['losses'],
            'FullName': f'({tri}) {city} {name}',
            'Conference': conf_div['Conference'],
            'Division': conf_div['Division'],
        },
        'TeamBox': FormatTeamBox(teamBox, teamScoreboard, game_data_payload),
        'Players': PreparePlayer(teamBox['players'], game_data_payload, team_data=teamBox)
    }


    return prepared_team



def FormatTeamBox(team_data: dict, team_scoreboard_data: dict, game_data_payload: dict) -> dict:
    formatted_teambox = {
        'SeasonID': game_data_payload['SeasonID'],
        'GameID': game_data_payload['GameID'],
        'TeamID': team_data['teamId'],
        'MatchupID': game_data_payload['MatchupID'],
        'Points': team_data['statistics']['points'],
        'PointsAgainst': team_data['statistics']['pointsAgainst'],
        'FG2M': team_data['statistics']['twoPointersMade'],
        'FG2A': team_data['statistics']['twoPointersAttempted'],
        'FG2%': team_data['statistics']['twoPointersPercentage'],
        'FG3M': team_data['statistics']['threePointersMade'],
        'FG3A': team_data['statistics']['threePointersAttempted'],
        'FG3%': team_data['statistics']['threePointersPercentage'],
        'FGM':  team_data['statistics']['fieldGoalsMade'],
        'FGA':  team_data['statistics']['fieldGoalsAttempted'],
        'FG%':  team_data['statistics']['fieldGoalsPercentage'],
        'FieldGoalsEffectiveAdjusted': team_data['statistics']['fieldGoalsEffectiveAdjusted'],
        'FTM': team_data['statistics']['freeThrowsMade'],
        'FTA': team_data['statistics']['freeThrowsAttempted'],
        'FT%': team_data['statistics']['freeThrowsPercentage'],
        'PtsFastBreak': team_data['statistics']['pointsFastBreak'],
        'PtsInThePaint': team_data['statistics']['pointsInThePaint'],
        'PtsSecondChance': team_data['statistics']['pointsSecondChance'],
        'PtsFromTurnovers': team_data['statistics']['pointsFromTurnovers'],
        'FastBreakFGM': team_data['statistics']['fastBreakPointsMade'],
        'FastBreakFGA': team_data['statistics']['fastBreakPointsAttempted'],
        'FastBreakFG%': team_data['statistics']['fastBreakPointsPercentage'],
        'PaintFGM': team_data['statistics']['pointsInThePaintMade'],
        'PaintFGA': team_data['statistics']['pointsInThePaintAttempted'],
        'PaintFG%': team_data['statistics']['pointsInThePaintPercentage'],
        'SecondChanceFGM': team_data['statistics']['secondChancePointsMade'],
        'SecondChanceFGA': team_data['statistics']['secondChancePointsAttempted'],
        'SecondChanceFG%': team_data['statistics']['secondChancePointsPercentage'],
        'TrueShootingAttempts': team_data['statistics']['trueShootingAttempts'],
        'TrueShootingPercentage': team_data['statistics']['trueShootingPercentage'],
        'BenchPoints':              team_data['statistics']['benchPoints'],
        'ReboundsDefensive':        team_data['statistics']['reboundsDefensive'],
        'ReboundsOffensive':        team_data['statistics']['reboundsOffensive'],
        'ReboundsPersonal':         team_data['statistics']['reboundsPersonal'],
        'ReboundsTeam':             team_data['statistics']['reboundsTeam'],
        'ReboundsTeamDefensive':    team_data['statistics']['reboundsTeamDefensive'],
        'ReboundsTeamOffensive':    team_data['statistics']['reboundsTeamOffensive'],
        'ReboundsTotal':            team_data['statistics']['reboundsTotal'],
        'Assists':                  team_data['statistics']['assists'],
        'AssistsTurnoverRatio':     team_data['statistics']['assistsTurnoverRatio'],
        'BiggestLead':              team_data['statistics'].get('biggestLead'),
        'BiggestLeadScore':         team_data['statistics'].get('biggestLeadScore'),
        'BiggestScoringRun':        team_data['statistics'].get('biggestScoringRun'),
        'BiggestScoringRunScore':   team_data['statistics'].get('biggestScoringRunScore'),
        'TimeLeading':              team_data['statistics'].get('timeLeading'),
        'TimesTied':                team_data['statistics'].get('timesTied'),
        'LeadChanges':              team_data['statistics'].get('leadChanges'),
        'Steals':                   team_data['statistics']['steals'],
        'Turnovers':                team_data['statistics']['turnovers'],
        'TurnoversTeam':            team_data['statistics']['turnoversTeam'],
        'TurnoversTotal':           team_data['statistics']['turnoversTotal'],
        'Blocks':                   team_data['statistics']['blocks'],
        'BlocksReceived':           team_data['statistics']['blocksReceived'],
        'FoulsDrawn':               team_data['statistics']['foulsDrawn'],
        'FoulsOffensive':           team_data['statistics']['foulsOffensive'],
        'FoulsPersonal':            team_data['statistics']['foulsPersonal'],
        'FoulsTeam':                team_data['statistics']['foulsTeam'],
        'FoulsTeamTechnical':       team_data['statistics']['foulsTeamTechnical'],
        'FoulsTechnical':           team_data['statistics']['foulsTechnical'],
        'Wins': team_scoreboard_data['wins'],
        'Losses': team_scoreboard_data['losses'],
        'Win': game_data_payload['Win'],
        'Seed': team_scoreboard_data['seed']
    }

    return formatted_teambox
#endregion Team data


#region Player data
def PreparePlayer(players: list, game_data_payload: dict, team_data: dict) -> list:
    prepared_players = []
    for player in players:
        Player = FormatPlayer(player, game_data_payload['SeasonID'])
        PlayerBox = FormatPlayerBox(player, game_data_payload, team_data)
        StartingLineup = FormatStartingLineups(player, game_data_payload, team_data)
        prepared_players.append({
            'Player': Player,
            'PlayerBox': PlayerBox,
            'StartingLineups': StartingLineup
        })

    return prepared_players


def FormatPlayer(player: dict, SeasonID: int) -> dict:
    prepared_player = {
        'SeasonID': SeasonID,
        'PlayerID': player['personId'],
        'Name': player['name'],
        'NameInitial': player['nameI'],
        'NameFirst': player['firstName'],
        'NameLast': player['familyName'],
        'Number': player['jerseyNum'],
        'Position': player.get('position'),
        }

    return prepared_player


def FormatPlayerBox(player: dict, game_data_payload: dict, team_data: dict) -> dict:
    atr = player['statistics']['assists'] / player['statistics']['turnovers'] if player['statistics']['turnovers'] != 0 else player['statistics']['assists']

    Minutes = player['statistics']['minutes'].replace('PT', '').replace('M', ':').replace('S', '')
    min_split = Minutes.split(':')
    m_calc = int(min_split[0])
    s_calc = float(min_split[1])
    MinutesCalculated = round(m_calc + (s_calc/60), 2)
    
    prepared_playerbox = {
        'SeasonID': game_data_payload['SeasonID'],
        'GameID': game_data_payload['GameID'],
        'TeamID': team_data['teamId'],
        'MatchupID': game_data_payload['MatchupID'],
        'PlayerID': player['personId'],
        'Status':player['status'],
        'Starter': int(player['starter']) if player.get('starter') != None else None,
        'Position': player.get('position'),
        'Minutes': Minutes,
        'MinutesCalculated': MinutesCalculated,
        'Points': player['statistics']['points'],
        'Assists': player['statistics']['assists'],
        'ReboundsTotal': player['statistics']['reboundsTotal'],
        'FG2M': player['statistics']['twoPointersMade'],
        'FG2A': player['statistics']['twoPointersAttempted'],
        'FG2%': player['statistics']['twoPointersPercentage'],
        'FG3M': player['statistics']['threePointersMade'],
        'FG3A': player['statistics']['threePointersAttempted'],
        'FG3%': player['statistics']['threePointersPercentage'],
        'FGM': player['statistics']['fieldGoalsMade'],
        'FGA': player['statistics']['fieldGoalsAttempted'],
        'FG%': player['statistics']['fieldGoalsPercentage'],
        'FTM': player['statistics']['freeThrowsMade'],
        'FTA': player['statistics']['freeThrowsAttempted'],
        'FT%': player['statistics']['freeThrowsPercentage'],
        'ReboundsDefensive': player['statistics']['reboundsDefensive'],
        'ReboundsOffensive': player['statistics']['reboundsOffensive'],
        'Blocks': player['statistics']['blocks'],
        'BlocksReceived': player['statistics']['blocksReceived'],
        'Steals': player['statistics']['steals'],
        'Turnovers': player['statistics']['turnovers'],
        'AssistsTurnoverRatio': atr,
        'Plus': player['statistics']['plus'],
        'Minus': player['statistics']['minus'],
        'PlusMinusPoints': player['statistics']['plusMinusPoints'],
        'PtsFastBreak': player['statistics']['pointsFastBreak'],
        'PtsInThePaint': player['statistics']['pointsInThePaint'],
        'PtsSecondChance': player['statistics']['pointsSecondChance'],
        'FoulsOffensive': player['statistics']['foulsOffensive'],
        'FoulsDrawn': player['statistics']['foulsDrawn'],
        'FoulsPersonal': player['statistics']['foulsPersonal'],
        'FoulsTechnical': player['statistics']['foulsTechnical'],
        'StatusReason': player.get('notPlayingReason'),
        'StatusDescription': player.get('notPlayingDescription')
    }
    return prepared_playerbox


def FormatStartingLineups(player: dict, game_data_payload: dict, team_data: dict):
    bp = 'here'
    Unit = 'Starters' if player['starter'] == '1' else 'Bench'
    formatted_lineup = {
        'SeasonID': game_data_payload['SeasonID'],
        'GameID': game_data_payload['GameID'],
        'TeamID': game_data_payload['TeamID'],
        'MatchupID': game_data_payload['MatchupID'],
        'PlayerID': player['personId'],
        'Unit': Unit,
        'Position': player.get('position')

    }
    return formatted_lineup

#endregion Player data


#region Arena data
def FormatArena(arena: dict, SeasonID: int, HomeTeamID: int | None) -> dict:
    formatted_arena = {
        'SeasonID': SeasonID,
        'ArenaID': arena['arenaId'],
        'TeamID': HomeTeamID,
        'City': arena['arenaCity'],
        'Country': arena['arenaCountry'],
        'Name': arena['arenaName'],
        'PostalCode': arena.get('arenaPostalCode'),
        'State': arena['arenaState'],
        'StreetAddress': arena.get('arenaStreetAddress'),
        'Timezone': arena['arenaTimezone'],
    }
    return formatted_arena

#endregion Arena data


#region Official data
def FormatOfficial(officials: list) -> list:
    prepared_officials = []
    for official in officials:
        prepared_officials.append({
            'OfficialID': official['personId'],
            'Name': official['name'],
            'NameInitial': official['nameI'],
            'NameFirst': official['firstName'],
            'NameLast': official['familyName'],
            'Number': official['jerseyNum'],
            'Assignment': official['assignment'],
        })
    return prepared_officials

#endregion Official