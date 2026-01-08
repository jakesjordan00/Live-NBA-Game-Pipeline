from typing import TypedDict



def InitiateBox(game: dict) -> dict:
    '''
    Formats all data to be derived from the Game's BoxScore.
    
    :param game: Game BoxScore data and Extreneous info
    :type game: dict
    :return BoxData: Formatted data for the following tables

            * **Game, GameExt, TeamBox, PlayerBox, StartingLineups**
            * *Team, Player, Arena, Official*
    :rtype: tuple[dict[Any, Any], dict[Any, Any]]
    '''
    print(f'     Formatting...')
    arena = game['arena']
    officials = game['officials']
    home = game['homeTeam']
    away = game['awayTeam']    
           
    Game, GameExt = FormatGame(game)
    Arena = FormatArena(Game['SeasonID'], Game['HomeID'], arena)
    Official = FormatOfficial(Game['SeasonID'], officials)
    Team, TeamBox, Player, PlayerBox, StartingLineups = BoxscoreLoop(Game['SeasonID'], Game['GameID'], Game['HomeID'], Game['AwayID'], [home, away])

    BoxData = {
        'Game': Game,
        'GameExt': GameExt,
        'Team': Team,
        'TeamBox': TeamBox,
        'Player': Player,
        'PlayerBox': PlayerBox,
        'StartingLineups': StartingLineups,
        'Arena': Arena,
        'Official': Official
    }
    #Return status message of some sort
    return BoxData

#region Game, Arena and Official
def FormatGame(game: dict) -> tuple[dict, dict]:
    '''
    Formats game dictionary into Game and GameExt    

    :param game: Unformatted game dictionary
    :type game: dict
    :return Game: Formatted data for Game table
    :return GameExt: Formatted data for GameExt table
    :rtype: tuple[dict[Any, Any], dict[Any, Any]]
    '''
    SeasonID = int(f'20{game['gameId'][3:5]}')
    GameID = int(game['gameId'])
    Date = game['gameEt'].split('T')[0]
    Datetime = game['gameEt'][:-6]
    HomeID = int(game['homeTeam']['teamId'])
    HScore = game['homeTeam']['score']
    AwayID = int(game['awayTeam']['teamId'])
    AScore = game['awayTeam']['score']
    if HScore >= AScore:
        WinnerID = HomeID
        WScore = HScore
        LoserID = AwayID
        LScore = AScore
    else:
        WinnerID = AwayID
        WScore = AScore
        LoserID = HomeID
        LScore = HScore
    gType = int(game['gameId'][2])
    GameType = 'RS' if gType == 2 else 'PRE' if gType == 1 else 'PS' if gType == 4 else 'PI' if gType == 5 else 'CUP'
    SeriesID = str(GameID)[:7] if GameType == 'PS' else None

    Game = {
        'SeasonID': SeasonID,
        'GameID': GameID,
        'Date': Date,
        'GameType': GameType,
        'HomeID': HomeID,
        'HScore': HScore,
        'AwayID': AwayID,
        'AScore': AScore,
        'WinnerID': WinnerID,
        'WScore': WScore,
        'LoserID': LoserID,
        'LScore': LScore,
        'SeriesID': SeriesID,
        'Datetime': Datetime,        
    }

    ArenaID     = game['arena']['arenaId']
    Attendance  = game['attendance']
    Sellout     = int(game['sellout'])
    Label       = None
    LabelDetail = None
    Status = game['gameStatusText']
    Periods = game['period']
    Officials = [ref['personId'] for ref in game['officials']]
    officialAssignments = {ref['assignment']: ref['personId'] for ref in game['officials']}
    OfficialID = officialAssignments.get('OFFICIAL1')
    Official2ID = officialAssignments.get('OFFICIAL2')
    Official3ID = officialAssignments.get('OFFICIAL3')
    OfficialAlternateID = officialAssignments.get('ALTERNATE') 

    GameExt = {
        'SeasonID': SeasonID,
        'GameID': GameID,
        'ArenaID':ArenaID,
        'Attendance':  Attendance,
        'Sellout':  Sellout,
        'Label':  Label,
        'LabelDetail':  LabelDetail,
        'OfficialID': Officials[0],
        'Official2ID': Officials[1],
        'Official3ID': Officials[2],
        'OfficialAlternateID': Officials[3] if len(Officials) == 4 else None,
        'Status': Status,
        'Periods': Periods
    }
    
    return Game, GameExt


def FormatArena(SeasonID: int, TeamID: int, arena: dict) -> dict:
    '''
    Recieves arena dictionary and SeasonID and TeamID. Formats for SQL table
    
    :param SeasonID: SeasonID of Game
    :type SeasonID: int
    :param TeamID: TeamID of Team that Arena belongs to
    :type TeamID: int
    :param arena: Unformatted arena dictionary
    :type arena: dict
    :return Arena: Formatted Arena data for SQL table
    :rtype: dict[Any, Any]
    '''
    ArenaID = arena['arenaId']
    Name = arena['arenaName']
    City = arena['arenaCity']
    State = arena['arenaState']
    Country = arena['arenaCountry']
    Timezone = arena['arenaTimezone']
    
    Arena = {
        'SeasonID': SeasonID,
        'ArenaID': ArenaID,
        'TeamID': TeamID,
        'City': City,
        'Country': Country,
        'Name': Name,
        'PostalCode': None,
        'State': State,
        'StreetAddress': None,
        'Timezone': Timezone,
    }
    return Arena

def FormatOfficial(SeasonID: int, officials: list) -> list[dict]:
    Official = []
    for official in officials:            
        Official.append({
            'SeasonID': SeasonID,
            'OfficialID': official['personId'],
            'Name': official['name'],
            'Number': official['jerseyNum']
        })
    return Official
#endregion Game, Arena and Officials


#region Boxscore - Team, TeamBox, Player, PlayerBox, StartingLineups
def BoxscoreLoop(SeasonID: int, GameID: int, HomeID: int, AwayID: int, teams: list) -> tuple[list, list, list, list, list]:
    '''
    Function to format all Box data requiring the same iteration structure
    
    :param SeasonID: SeasonID of Game
    :type SeasonID: int
    :param GameID:  GameID of Game
    :type GameID: int
    :param HomeID: TeamID of Home Team
    :type HomeID: int
    :param AwayID: TeamID of Away Team
    :type AwayID: int
    :param teams: Unformatted dictionary with Team data
    :type teams: list
    :return Team: Description
    :rtype: tuple[list[Any], list[Any], list[Any], list[Any], list[Any]]
    '''
    Team = []
    TeamBox = []
    TeamBoxExt = []
    Player = []
    PlayerBox = []
    StartingLineups = []
    for index, team in enumerate(teams): 
        opTeam = teams[1- index]
        TeamID = team['teamId'] 
        Team.append(FormatTeam(SeasonID, TeamID, team))
        
        isHome = team['teamId'] == HomeID
        MatchupID = AwayID if isHome else HomeID
        TeamBox.append(FormatTeamBox(SeasonID, GameID, TeamID, MatchupID, team))        
        for i, qtr in enumerate(team['periods']):            
            TeamBoxExt.append(FormatTeamBoxExt(SeasonID, GameID, TeamID, MatchupID, qtr, opTeam['periods'][i]))

        for player in team['players']:                
            PlayerID = player['personId']
            Position = player['position'] if 'position' in player.keys() else None
            Player.append(FormatPlayer(SeasonID, PlayerID, Position, player))
            PlayerBox.append(FormatPlayerBox(SeasonID, GameID, TeamID, MatchupID, PlayerID, Position, player))
            StartingLineups.append(FormatStartingLineups(SeasonID, GameID, TeamID, MatchupID, PlayerID, Position, player))

        test = 1
    test = 1

    return Team, TeamBox, Player, PlayerBox, StartingLineups


#region Team - Team, TeamBox
def FormatTeam(SeasonID: int, TeamID: int, team: dict) -> dict:
    '''
    Formats team dictionary
    
    :param SeasonID: SeasonID of Game
    :type SeasonID: int
    :param TeamID: TeamID of Team
    :type TeamID: int
    :param team: Unformatted dictionary containing Team data
    :type team: dict
    :return Team: Formatted Team data for SQL table
    :rtype: dict[Any, Any]
    ''' 
    City = team['teamCity']
    Name = team['teamName']
    Tricode = team['teamTricode'] 
    if TeamID in   [1610612738, 1610612751, 1610612752, 1610612755, 1610612761]:
        Division = 'Atlantic'
        Conference = 'East'
    elif TeamID in [1610612741, 1610612739, 1610612765, 1610612754, 1610612749]:
        Division = 'Central'
        Conference = 'East'
    elif TeamID in [1610612737, 1610612766, 1610612748, 1610612753, 1610612764]:
        Division = 'Southeast'
        Conference = 'East'
    elif TeamID in [1610612743, 1610612750, 1610612760, 1610612757, 1610612762]:
        Division = 'Northwest'
        Conference = 'West'
    elif TeamID in [1610612744, 1610612746, 1610612747, 1610612756, 1610612758]:
        Division = 'Pacific'
        Conference = 'West'
    elif TeamID in [1610612742, 1610612745, 1610612763, 1610612740, 1610612759]:
        Division = 'Southwest'
        Conference = 'West'

    Team = {
        'SeasonID': SeasonID,
        'TeamID': TeamID,
        'City': City,
        'Name': Name,
        'Tricode': Tricode,
        'Wins': None,
        'Losses': None,
        'FullName': f'({Tricode}) {City} {Name}',
        'Conference': Conference,
        'Division': Division
    }
    return Team

def FormatTeamBox(SeasonID: int, GameID: int, TeamID: int, MatchupID: int, team: dict) -> dict:
    '''
    Formats TeamBox data for SQL
    
    :param SeasonID: SeasonID of Game
    :type SeasonID: int
    :param GameID: GameID of Game
    :type GameID: int
    :param TeamID: TeamID of Team
    :type TeamID: int
    :param MatchupID: TeamID of opponent
    :type MatchupID: int
    :param team: Unformatted team dictionary
    :type team: dict
    :return TeamBox: Formatted TeamBox data
    :rtype: dict[Any, Any]
    '''
    Win = team['statistics']['points'] > team['statistics']['pointsAgainst']
    BiggestLeadScore = team['statistics']['biggestLeadScore'] if team['statistics']['biggestLeadScore'] in team['statistics'].keys() else None
    TeamBox = {
        'SeasonID': SeasonID,
        'GameID': GameID,
        'TeamID': TeamID,
        'MatchupID': MatchupID,
        'Points': team['statistics']['points'],
        'PointsAgainst': team['statistics']['pointsAgainst'],
        'FG2M': team['statistics']['twoPointersMade'],
        'FG2A': team['statistics']['twoPointersAttempted'],
        'FG2%': team['statistics']['twoPointersPercentage'],
        'FG3M': team['statistics']['threePointersMade'],
        'FG3A': team['statistics']['threePointersAttempted'],
        'FG3%': team['statistics']['threePointersPercentage'],
        'FGM': team['statistics']['fieldGoalsMade'],
        'FGA': team['statistics']['fieldGoalsAttempted'],
        'FG%': team['statistics']['fieldGoalsPercentage'],
        'FieldGoalsEffectiveAdjusted': team['statistics']['fieldGoalsEffectiveAdjusted'],
        'FTM': team['statistics']['freeThrowsMade'],
        'FTA': team['statistics']['freeThrowsAttempted'],
        'FT%': team['statistics']['freeThrowsPercentage'],
        'SecondChancePointsMade': team['statistics']['secondChancePointsMade'],
        'SecondChancePointsAttempted': team['statistics']['secondChancePointsAttempted'],
        'SecondChancePointsPercentage': team['statistics']['secondChancePointsPercentage'],
        'TrueShootingAttempts': team['statistics']['trueShootingAttempts'],
        'TrueShootingPercentage': team['statistics']['trueShootingPercentage'],
        'PointsFromTurnovers': team['statistics']['pointsFromTurnovers'],
        'PointsSecondChance': team['statistics']['pointsSecondChance'],
        'PointsInThePaint': team['statistics']['pointsInThePaint'],
        'PointsInThePaintMade': team['statistics']['pointsInThePaintMade'],
        'PointsInThePaintAttempted': team['statistics']['pointsInThePaintAttempted'],
        'PointsInThePaintPercentage': team['statistics']['pointsInThePaintPercentage'],
        'PointsFastBreak': team['statistics']['pointsFastBreak'],
        'FastBreakPointsMade': team['statistics']['fastBreakPointsMade'],
        'FastBreakPointsAttempted': team['statistics']['fastBreakPointsAttempted'],
        'FastBreakPointsPercentage': team['statistics']['fastBreakPointsPercentage'],
        'BenchPoints': team['statistics']['benchPoints'],
        'ReboundsDefensive': team['statistics']['reboundsDefensive'],
        'ReboundsOffensive': team['statistics']['reboundsOffensive'],
        'ReboundsPersonal': team['statistics']['reboundsPersonal'],
        'ReboundsTeam': team['statistics']['reboundsTeam'],
        'ReboundsTeamDefensive': team['statistics']['reboundsTeamDefensive'],
        'ReboundsTeamOffensive': team['statistics']['reboundsTeamOffensive'],
        'ReboundsTotal': team['statistics']['reboundsTotal'],
        'Assists': team['statistics']['assists'],
        'AssistsTurnoverRatio': team['statistics']['assistsTurnoverRatio'],
        'BiggestLead': team['statistics']['biggestLead'],
        'BiggestLeadScore': BiggestLeadScore,
        'BiggestScoringRun': team['statistics']['biggestScoringRun'],
        'BiggestScoringRunScore': team['statistics']['biggestScoringRunScore'],
        'TimeLeading': team['statistics']['timeLeading'],
        'TimesTied': team['statistics']['timesTied'],
        'LeadChanges': team['statistics']['leadChanges'],
        'Steals': team['statistics']['steals'],
        'Turnovers': team['statistics']['turnovers'],
        'TurnoversTeam': team['statistics']['turnoversTeam'],
        'TurnoversTotal': team['statistics']['turnoversTotal'],
        'Blocks': team['statistics']['blocks'],
        'BlocksReceived': team['statistics']['blocksReceived'],
        'FoulsDrawn': team['statistics']['foulsDrawn'],        
        'FoulsOffensive': team['statistics']['foulsOffensive'],
        'FoulsPersonal': team['statistics']['foulsPersonal'],
        'FoulsTeam': team['statistics']['foulsTeam'],
        'FoulsTeamTechnical': team['statistics']['foulsTeamTechnical'],
        'FoulsTechnical': team['statistics']['foulsTechnical'],
        'Wins': None,
        'Losses': None,
        'Win': Win,
        'Seed': None,
    }
    return TeamBox

def FormatTeamBoxExt(SeasonID: int, GameID: int, TeamID: int, MatchupID: int, qtr: dict, opQtr: dict) -> dict:
    TeamBoxExt = {
        'SeasonID': SeasonID,
        'GameID': GameID,
        'TeamID': TeamID,
        'MatchupID': MatchupID,
        'Qtr': qtr['period'],
        'Points': qtr['score'],
        'PointsAgainst': opQtr['score']
    }
    return TeamBoxExt
#endregion Team


#region Player - Player, PlayerBox, StartingLineups
def FormatPlayer(SeasonID: int, PlayerID: int, Position: str | None, player: dict) -> dict:
    '''
    Formats Player data for SQL
    
    :param SeasonID: SeasonID of Game
    :type SeasonID: int
    :param PlayerID: PlayerID of Player
    :type PlayerID: int
    :param Position: Position of Player
    :type Position: str | None
    :param player: Unformatted dictionary with Player data
    :type player: dict
    :return Player: Formatted Player data
    :rtype: dict[Any, Any]
    '''
    Player = {
        'SeasonID': SeasonID,
        'PlayerID': PlayerID,
        'Name': player['name'],
        'Number': player['jerseyNum'],
        'Position': Position,
        'NameInitial': player['nameI'],
        'NameLast': player['familyName'],
        'NameFirst': player['firstName']
    }
    return Player

def FormatPlayerBox(SeasonID: int, GameID: int, TeamID: int, MatchupID: int, PlayerID: int, Position: str | None, player: dict) -> dict:
    '''
    Formats PlayerBox data for SQL
    
    :param SeasonID: SeasonID of Game
    :type SeasonID: int
    :param GameID: GameID of Game
    :type GameID: int
    :param TeamID: TeamID of Player's Team
    :type TeamID: int
    :param MatchupID: TeamID of opposing Team
    :type MatchupID: int
    :param PlayerID: PlayerID of Player
    :type PlayerID: int
    :param Position: Position of Player
    :type Position: str | None
    :param player: Unformatted dictionary with Player data
    :type player: dict
    :return PlayerBox: Formatted PlayerBox data
    :rtype: dict[Any, Any]
    '''
    Min = player['statistics']['minutes']
    Minutes = Min.replace('PT', '')[:2]
    Seconds = Min[5:].replace('S', '')
    SecCalc = float(Seconds)/60
    MinCalc = int(Minutes) + SecCalc
    if player['statistics']['assists'] != 0 and player['statistics']['turnovers'] == 0:
        atr = player['statistics']['assists']
    elif player['statistics']['assists'] != 0 and player['statistics']['turnovers'] != 0:
        atr = player['statistics']['assists'] / player['statistics']['turnovers']
    else:
        atr = 0

    StatusReason = player['notPlayingReason'] if 'notPlayingReason' in player.keys() else None
    StatusDescription = player['notPlayingDescription'] if 'notPlayingDescription' in player.keys() else None
    Minutes = player['statistics']['minutes'].replace('PT', '').replace('M', ':').replace('S', '')
    PlayerBox = {
        'SeasonID': SeasonID,
        'GameID': GameID,
        'TeamID': TeamID,
        'MatchupID': MatchupID,
        'PlayerID': PlayerID,
        'Status': player['status'],
        'Starter': int(player['starter']),
        'Position': Position,
        'Minutes': Minutes,
        'MinutesCalculated': MinCalc,
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
        'PointsFastBreak': player['statistics']['pointsFastBreak'],
        'PointsInThePaint': player['statistics']['pointsInThePaint'],
        'PointsSecondChance': player['statistics']['pointsSecondChance'],
        'FoulsOffensive': player['statistics']['foulsOffensive'],
        'FoulsDrawn': player['statistics']['foulsDrawn'],
        'FoulsPersonal': player['statistics']['foulsPersonal'],
        'FoulsTechnical': player['statistics']['foulsTechnical'],
        'Status': player['status'],
        'StatusReason': StatusReason,
        'StatusDescription': StatusDescription
    }
    return PlayerBox

def FormatStartingLineups(SeasonID: int, GameID: int, TeamID: int, MatchupID: int, PlayerID: int, Position: str | None, player: dict) -> dict:
    '''
    Formats StartingLineup data for SQL
    
    :param SeasonID: SeasonID of Game
    :type SeasonID: int
    :param GameID: GameID of Game
    :type GameID: int
    :param TeamID: TeamID of Player's Team
    :type TeamID: int
    :param MatchupID: TeamID of opposing Team
    :type MatchupID: int
    :param PlayerID: PlayerID of Player
    :type PlayerID: int
    :param Position: Position of Player
    :type Position: str | None
    :param player: Unformatted dictionary with Player data
    :type player: dict
    :return: Description
    :rtype: dict[Any, Any]
    '''
    Unit = 'Starters' if player['starter'] == '1' else 'Bench'
    LineupRecord = {
        'SeasonID': SeasonID,
        'GameID': GameID,
        'TeamID': TeamID,
        'MatchupID': MatchupID,
        'PlayerID': PlayerID,
        'Unit': Unit,
        'Position': Position
    }
    return LineupRecord
#endregion Player


#endregion Boxscore - Team, TeamBox, Player, PlayerBox, StartingLineups




