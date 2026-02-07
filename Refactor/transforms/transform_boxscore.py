

from re import Match
import select


class Transform:


    def __init__(self, pipeline):
        self.pipeline = pipeline
        pass
    
    def box(self, data_extract):
        box_data = data_extract['game']
        scoreboard_data = self.pipeline.Data

        prepared_data = PrepareBox(box_data, scoreboard_data)


        home_scoreboard = scoreboard_data['HomeTeam']
        away_scoreboard = scoreboard_data['AwayTeam']


        return 1
    

def PrepareBox(box_data, scoreboard_data):
    SeasonID = 2000 + int(box_data['gameId'][3:5])
    box_data['SeasonID'] = SeasonID
    box_data['GameID'] = scoreboard_data['GameID']
    HomeID = box_data['homeTeam']['teamId']
    AwayID = box_data['awayTeam']['teamId']

    teams = [
        (box_data['homeTeam'], scoreboard_data['HomeTeam'], HomeID, AwayID, 'homeTeam'), 
        (box_data['awayTeam'], scoreboard_data['AwayTeam'], AwayID, HomeID, 'awayTeam')
    ]

    for teamBox, teamScoreboard, TeamID, MatchupID, selector in teams:
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
            'GameID': scoreboard_data['GameID'],
            'TeamID': TeamID,
            'MatchupID': MatchupID,
            'Home': Home
        }

        prepared_team = {
            'TeamID': teamBox['teamId'],
            'City': city,
            'Name': name,
            'Tricode': tri,
            'Wins': teamScoreboard['wins'],
            'Losses': teamScoreboard['losses'],
            'FullName': f'({tri}) {city} {name}',
            'Seed': teamScoreboard['seed'],
            'Win': Win,
            'Score': teamBox['score'],
            'InBonus': teamBox['inBonus'],
            'Timeouts': teamBox['timeoutsRemaining'],
            'Players': PreparePlayer(teamBox['players'], game_data_payload, team_data=teamBox),
            'Statistics': FormatTeamBox(teamBox, game_data_payload),
            'Periods': teamBox['periods']
        }
        box_data[selector] = prepared_team

    
    prepared_box_data = {
        'SeasonID': 2000 + int(box_data['gameId'][3:5]),
        'GameID': scoreboard_data['GameID'],
        'Home': box_data['homeTeam'],
        'Away': box_data['awayTeam'],
        'Officials': FormatOfficial(box_data['officials']),
        'Arena': box_data['arena'],
        'Label': scoreboard_data['GameLabel'],
        'LabelDetail': scoreboard_data['GameSubLabel'],
        'SeriesText': scoreboard_data['SeriesText'],
    }

    return box_data



def FormatTeamBox(team_data: dict, game_data_payload: dict):

    prepared_teambox = {
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
        'FTM': team_data['statistics']['ftm'],
        'FTA': team_data['statistics']['fta'],
        'FT%': team_data['statistics']['ft%'],
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
    }

    return prepared_teambox




#region Player
def PreparePlayer(players: list, game_data_payload: dict, team_data: dict):
    prepared_players = []
    for player in players:
        Player = FormatPlayer(player, game_data_payload['SeasonID'])
        PlayerBox = FormatPlayerBox(player, game_data_payload, team_data)
        prepared_players.append({
            'Player': Player,
            'PlayerBox': PlayerBox
        })

    return prepared_players


def FormatPlayer(player: dict, SeasonID: int):
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
    bp = 'here'

    return prepared_player


def FormatPlayerBox(player: dict, game_data_payload: dict, team_data: dict):
    atr = player['statistics']['assists'] / player['statistics']['turnovers'] if player['statistics']['turnovers'] != 0 else player['statistics']['assists']


    Minutes = player['statistics']['minutes'].replace('PT', '').replace('M', ':').replace('S', '')
    min_split = Minutes.split(':')
    m_calc = int(min_split[0])
    s_calc = float(min_split[1])
    MinutesCalculated = round(m_calc + (s_calc/60), 2)
    

    bp = 'here'
    prepared_playerbox = {
        'SeasonID': game_data_payload['SeasonID'],
        'GameID': game_data_payload['GameID'],
        'TeamID': team_data['teamId'],
        'MatchupID': game_data_payload['MatchupID'],
        'PlayerID': player['personId'],
        'Status':player['status'],
        'Starter': player['starter'],
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
    bp = 'here'

    return prepared_playerbox
#endregion Player






#region Official
def FormatOfficial(officials: list):
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