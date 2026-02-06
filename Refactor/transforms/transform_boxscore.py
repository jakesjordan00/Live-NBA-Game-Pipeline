

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

    teams = [
        (box_data['homeTeam'], scoreboard_data['HomeTeam'], 'homeTeam'), 
        (box_data['awayTeam'], scoreboard_data['AwayTeam'], 'awayTeam')
    ]

    for teamBox, teamScoreboard, selector in teams:
        name = teamBox['teamName']
        city = teamBox['teamCity']
        tri = teamBox['teamTricode']
        prepared_team = {
            # **teamBox,
            'TeamID': teamBox['teamId'],
            'City': city,
            'Name': name,
            'Tricode': tri,
            'Wins': teamScoreboard['wins'],
            'Losses': teamScoreboard['losses'],
            'FullName': f'({tri}) {city} {name}',
            'Seed': teamScoreboard['seed'],
            'Win': 1 if teamBox['statistics']['points'] > teamBox['statistics']['pointsAgainst'] and box_data['gameStatus'] == 3 else 
                   0 if teamBox['statistics']['points'] < teamBox['statistics']['pointsAgainst'] and box_data['gameStatus'] == 3 else None,
            'Score': teamBox['score'],
            'InBonus': teamBox['inBonus'],
            'Timeouts': teamBox['timeoutsRemaining'],
            'Players': PreparePlayer(teamBox['players'], box_data, team_data=teamBox),
            'Statistics': teamBox['statistics'],
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






#region Player
def PreparePlayer(players: list, box_data: dict, team_data: dict):
    prepared_players = []
    for player in players:
        Player = FormatPlayer(player, box_data['SeasonID'])
        PlayerBox = FormatPlayerBox(player, box_data, team_data)
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
        'Position': player['position'],
        

    }
    bp = 'here'

    return prepared_player


def FormatPlayerBox(player: dict, box_data: dict, team_data: dict):
    MatchupID = box_data['awayTeam']['teamId'] if team_data['teamId'] == box_data['homeTeam']['teamId'] else box_data['homeTeam']['teamId']
    
    Minutes = player['statistics']['minutes'].replace('PT', '').replace('M', ':').replace('S', '')

    min_split = Minutes.split(':')
    m_calc = int(min_split[0])
    s_calc = float(min_split[1])
    MinutesCalculated = round(m_calc + (s_calc/60), 2)
    bp = 'here'
    prepared_playerbox = {
        'SeasonID': box_data['SeasonID'],
        'GameID': box_data['GameID'],
        'TeamID': team_data['teamId'],
        'PlayerID': player['personId'],
        'Status':player['status'],
        'Starter': player['starter'],
        'Position': player['position'],
        'Minutes': Minutes,
        'MinutesCalculated': MinutesCalculated,
        '': player['statistics'][''],
        '': player['statistics'][''],
        '': player['statistics'][''],
        '': player['statistics'][''],
        '': player['statistics']['']
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