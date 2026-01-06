


def InitiateBox(game: dict):
    '''
    Docstring for InitiateBox
    
    :param game: Game BoxScore data and Extreneous info
    :type game: dict
    '''
    arena = game['arena']
    officials = game['officials']
    home = game['homeTeam']
    away = game['awayTeam']

    Game, GameExt = FormatGame(game)

    Arena = FormatArena(Game['SeasonID'], Game['HomeID'], arena)

    Team = FormatTeam(Game['SeasonID'], Game['GameID'], Game['HomeID'], Game['AwayID'], [home, away])

    #Return status message of some sort
    return 1



def FormatGame(game: dict):
    SeasonID = int(f'20{game['gameId'][3:5]}')
    GameID = int(game['gameId'])
    Date = game['gameEt'].split('T')[0]
    Datetime = game['gameEt'][:-6]
    HomeID = int(game['homeTeam']['teamId'])
    hScore = game['homeTeam']['score']
    AwayID = int(game['awayTeam']['teamId'])
    aScore = game['awayTeam']['score']
    if hScore >= aScore:
        WinnerID = HomeID
        WScore = hScore
        LoserID = AwayID
        LScore = aScore
    else:
        WinnerID = AwayID
        WScore = aScore
        LoserID = HomeID
        LScore = hScore
    gType = int(game['gameId'][2])
    GameType = 'RS' if gType == 2 else 'PRE' if gType == 1 else 'PS' if gType == 4 else 'PI' if gType == 5 else 'CUP'
    SeriesID = str(GameID)[:7] if GameType == 'PS' else None

    Game = {
        'SeasonID': SeasonID,
        'GameID': GameID,
        'Date': Date,
        'GameType': GameType,
        'HomeID': HomeID,
        'hScore': hScore,
        'AwayID': AwayID,
        'aScore': aScore,
        'WinnerID': WinnerID,
        'WScore': WScore,
        'LoserID': LoserID,
        'LScore': LoserID,
        'SeriesID': SeriesID,
        'Datetime': Datetime,        
    }

    ArenaID     = game['arena']['arenaId']
    Attendance  = game['attendance']
    Sellout     = int(game['sellout'])
    Label       = None
    LabelDetail = None
    Officials = [ref['personId'] for ref in game['officials']]
    Status = game['gameStatusText']
    Periods = game['period']

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


def FormatArena(SeasonID: int, TeamID: int, arena: dict):
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



    
def FormatTeam(SeasonID: int, GameID: int, HomeID: int, AwayID: int, 
               teams: list):

    for team in teams:
        # for key in team['statistics']:            
            # print(f"'{key[0].upper()}{key[1:]}': team['statistics']['{key}'],")
 
        isHome = team['teamId'] == HomeID
        TeamID = HomeID if isHome else AwayID
        MatchupID = AwayID if isHome else HomeID

        TeamBox = FormatTeamBox(SeasonID, GameID, TeamID, MatchupID, team)

        test= 1

        
        PlayerBox = FormatPlayerBox(SeasonID, GameID, TeamID, MatchupID, team['players'])

        test = 1




    Team = {


    }
    return Team



def FormatTeamBox(SeasonID: int, GameID: int, TeamID: int, MatchupID: int, team: dict):


    test = 1
    Win = team['statistics']['points'] > team['statistics']['pointsAgainst']
    TeamBox = {
        'SeasonID': SeasonID,
        'GameID': 'GameID',
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
        'BiggestLeadScore': team['statistics']['biggestLeadScore'],
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



def FormatPlayerBox(SeasonID: int, GameID: int, TeamID: int, MatchupID: int, players: list):
    print('\n')
    PlayerBoxes = []
    for player in players:

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


        Position = player['position'] if 'position' in player.keys() else None
        StatusReason = player['notPlayingReason'] if 'notPlayingReason' in player.keys() else None
        StatusDescription = player['notPlayingDescription'] if 'notPlayingDescription' in player.keys() else None

       
        PlayerBox = {
            'SeasonID': SeasonID,
            'GameID': GameID,
            'TeamID': TeamID,
            'MatchupID': MatchupID,
            'PlayerID': player['personId'],
            'Status': player['status'],
            'Starter': int(player['starter']),
            'Position': Position,
            'Minutes': player['statistics']['minutes'],
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
        PlayerBoxes.append(PlayerBox)

    return PlayerBoxes