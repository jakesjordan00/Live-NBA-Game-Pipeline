from tracemalloc import start
import pandas as pd
import polars as pl
#region Substitution Groups
def DetermineSubstitutions(data_extract: dict, boxscore_data: dict):
    # api_data_extract = data_extract_full['api_data_extract']
    playbyplay_data = data_extract['game']['actions']
    # playbyplay_api_data = api_data_extract['game']['actions']

    sub_in_actions = 0
    sub_out_actions = 0
    home_in = 0
    home_out = 0
    away_in = 0
    away_out = 0
    sub_groups = []
    
    Periods = 4 if boxscore_data['GameExt']['Periods'] <= 4 else boxscore_data['GameExt']['Periods']
    for i, action in enumerate(playbyplay_data):
        Qtr = action['period']
        Clock = action['clock'].replace('PT', '').replace('M', ':').replace('S', '')
        PointInGame, MinElapsed = CalculatePointInGame(Clock, Qtr, Periods)
        action['PointInGame'] = PointInGame
        action['MinElapsed'] = MinElapsed
        action['Clock'] = Clock

        game_end = 1 if action['actionType'] == 'game' and action['subType'] == 'end' else 0
        #This is where i need to handle if the most recent action is a substitution.
        if action['actionType'] == 'substitution' or (game_end == 1):
            SubTime = f'Q{Qtr} {Clock}'
            game_end = 1 if action['actionType'] == 'game' and action['subType'] == 'end' else 0
            NextActionNumber = playbyplay_data[i+1]['actionNumber'] if game_end == 0 and i+1 < len(playbyplay_data) else action['actionNumber']
            test  = [s['SubTime'] for s in sub_groups]
            if SubTime not in [s['SubTime'] for s in sub_groups]:
                sub_groups.append({
                    'PointInGame': PointInGame,
                    'NextActionNumber': NextActionNumber,
                    'SubTime': SubTime,
                    'Period': Qtr,
                    'Clock': Clock
                })
                bp = 'here'
            else:
                existing = next(s for s in sub_groups if s['SubTime'] == SubTime)
                existing['NextActionNumber'] = NextActionNumber
                bp = 'here'

            if action['subType'] == 'in':
                sub_in_actions += 1
                action['SubInNumber'] = sub_in_actions
                action['SubOutNumber'] = None
                if action['teamId'] == boxscore_data['Game']['HomeID']:
                    home_in += 1
                    team_in_actions = home_in
                elif action['teamId'] == boxscore_data['Game']['AwayID']:
                    away_in += 1
                    team_in_actions = away_in
                action['TeamSubInNumber'] = team_in_actions
                action['TeamSubOutNumber'] = None

            elif action['subType'] == 'out':
                sub_out_actions += 1
                action['SubInNumber'] = None
                action['SubOutNumber'] = sub_out_actions
                if action['teamId'] == boxscore_data['Game']['HomeID']:
                    home_out += 1
                    team_out_actions = home_out
                elif action['teamId'] == boxscore_data['Game']['AwayID']:
                    away_out += 1
                    team_out_actions = away_out
                action['TeamSubInNumber'] = None
                action['TeamSubOutNumber'] = team_out_actions
        else:
            action['SubInNumber'] = None
            action['SubOutNumber'] = None
            action['TeamSubInNumber'] = None
            action['TeamSubOutNumber'] = None



    for action in playbyplay_data:
        if action['actionType'] == 'substitution':
            bp = 'here'
            if action['subType'] == 'in':
                subs_type = 'SubIn'
                opp_subs_type = 'SubOut'
            else:
                subs_type = 'SubOut'
                opp_subs_type = 'SubIn'
            action['CorrespondingSubActionNumber'] = next(
                (p['actionNumber'] for p in playbyplay_data
                if p['actionNumber'] != action['actionNumber']  # don't match itself
                and action[f'{subs_type}Number'] == p[f'{opp_subs_type}Number']
                and action[f'Team{subs_type}Number'] == p[f'Team{opp_subs_type}Number']),
                None  # default if no match found
            )
            bp = 'here'


    return playbyplay_data, sub_groups

def CalculatePointInGame(Clock: str, Period: int, Periods: int):
    cMinutes = int(Clock[0:2])
    cSeconds = float(Clock[-5:])
    MinElapsed = round(12 - (cMinutes + (cSeconds / 60)) + ((Period - 1) * 12), 4)
    minCalc = (cMinutes + (cSeconds / 60))


    total_game_time = (12 * 4) + ((Periods - Period) * 5)
    PointInGame = round(((MinElapsed / total_game_time) * 100), 4)
    return PointInGame, MinElapsed

#endregion Substitution Groups


#region Stint Parsing
def Stints(playbyplay_data: list, sub_groups: list, start_action: int, boxscore_data: dict):
    StintID = 1
    final_action = playbyplay_data[-1]

    HomeID = boxscore_data['Game']['HomeID']
    AwayID = boxscore_data['Game']['AwayID']
    gameStatus = boxscore_data['GameExt']['Status']
    team_stints = []
    player_stints = []
    team_player_stints = []
    if start_action == 0:
        lineups = boxscore_data['StartingLineups']
        home = [player['PlayerID'] for player in lineups if player['TeamID'] == HomeID and player['Unit'] == 'Starters']
        away = [player['PlayerID'] for player in lineups if player['TeamID'] == AwayID and player['Unit'] == 'Starters']
        bp = 'here'   
    
    homeStats, awayStats = CreateFirstTeamStatsDict(boxscore_data['Game'], HomeID, AwayID, home, away, StintID)
    
    current_sub_group_index = 0
    if len(sub_groups) > 0:
        current_sub_group = sub_groups[current_sub_group_index]
    else:
        current_sub_group = {
            'PointInGame': 99,
            'NextActionNumber': 9999,
            'SubTime': "",
            'Period': 1,
            'Clock': "0"
        }
    if start_action != 0:
        currectAction = playbyplay_data[start_action]
        current_sub_group_index = [i for i, s in enumerate(sub_groups) if s['PointInGame'] <= currectAction['PointInGame']][::-1][0]
        current_sub_group = sub_groups[current_sub_group_index]
        start_sub_group = sub_groups[current_sub_group_index-1]



    home_copy = home.copy()
    away_copy = away.copy()
    bp = 'here'    
    lastPossession = 0
    for i, action in enumerate(playbyplay_data[start_action:]):
        #End Stint if Substitutions are done
        if action['actionNumber'] == current_sub_group['NextActionNumber'] or action['actionNumber'] == final_action['actionNumber']:
            do_home = home != home_copy
            do_away = away != away_copy
            stat_list = [homeStats, awayStats]
            stat_dict_list = [{
                'home_away': 'Home',
                'stats': homeStats,
                'sub_needed': do_home,
                'team_id': HomeID,
                'old_lineup': home,
                'new_lineup': home_copy
            },{
                'home_away': 'Away',
                'stats': awayStats,
                'sub_needed': do_away,
                'team_id': AwayID,
                'old_lineup': away,
                'new_lineup': away_copy
            }]
            #End Stint logic
            team_stints, player_stints, team_player_stints = StintEnding(action, final_action, stat_dict_list, team_stints, player_stints, team_player_stints, gameStatus)
            if do_home:
                homeStats = StintStarting(homeStats, action, stat_dict_list[0])
                home = [PlayerID for PlayerID in homeStats['Lineup'].keys()]
                bp = 'here'
            if do_away:
                awayStats = StintStarting(awayStats, action, stat_dict_list[1])
                away = [PlayerID for PlayerID in awayStats['Lineup'].keys()]
                bp = 'here'
            #If we arent at the last action, iterate:
            if action['actionNumber'] != final_action['actionNumber']:
                current_sub_group_index += 1
                sub_groups.append({
                            'PointInGame': 999,
                            'NextActionNumber': final_action['actionNumber'],
                            'SubTime': "",
                            'Period': 1,
                            'Clock': "0"
                        })
                current_sub_group = sub_groups[current_sub_group_index]
        

        #begin Stint parsing
        TeamID = action.get('teamId')
        if TeamID == None:
            continue
        isHome = TeamID == HomeID
        teamStats = homeStats if isHome and TeamID != None else awayStats
        opStats = awayStats if isHome and TeamID != None else homeStats
        actionType = action['actionType']
        lastPossession = playbyplay_data[start_action + i-1]['possession'] if i > 0 else 0

        if actionType == 'substitution':
            if action['actionNumber'] != final_action['actionNumber']:
                home_copy, away_copy = InitiateSubstitution(action, playbyplay_data, HomeID, AwayID, home_copy, away_copy)
            else:
                bp = 'here'

        elif actionType != 'substitution':
            teamStats, opStats = IncrementStats(action, teamStats, opStats, HomeID, AwayID, lastPossession)

    stints = {
        'team_stints': team_stints,
        'player_stints': player_stints,
        'team_player_stints': team_player_stints
    }
    return stints


#region Stint Start/End
def StintEnding(action: dict, last_action: dict, stat_dict_list: list, team_stints: list, player_stints: list, team_player_stints: list, gameStatus: str):

    for dict in stat_dict_list:
        sub_needed = dict['sub_needed'] or action['actionNumber'] == last_action['actionNumber']
        #If we don't need a sub, don't do anything
        #
        if sub_needed == False: 
            continue
        stat_dict = dict['stats']
        stat_dict['MinutesPlayed'] = round(action['MinElapsed'] - stat_dict['MinElapsedStart'], 2)
        if 'Final' not in gameStatus and action['actionType'] != 'substitution' and last_action['actionType'] != 'substitution':
            stat_dict['QtrEnd'] = None
            stat_dict['ClockEnd'] = None
            stat_dict['MinElapsedEnd'] = None
        else:
            stat_dict['QtrEnd'] = action['period']
            stat_dict['ClockEnd'] = action['Clock']
            stat_dict['MinElapsedEnd'] = action['MinElapsed']
        for playerStats in stat_dict['Lineup'].values():
            playerStats['MinutesPlayed'] = stat_dict['MinutesPlayed']
            playerStats['PlusMinus'] = stat_dict['PtsScored'] - stat_dict['PtsAllowed']
            player_stints.append(playerStats.copy())

        team_stint = {key: value for key, value in stat_dict.items() if key != 'Lineup'}
        team_stints.append(team_stint)
        team_player_stints.append(stat_dict)


    return team_stints, player_stints, team_player_stints

def StintStarting(stint_team_dict: dict, action: dict, team_dict: dict):
    new_stint_team_dict = stint_team_dict.copy()
    new_lineup = team_dict['new_lineup']
    new_stint_team_dict = CreateTeamStats(new_stint_team_dict, action, new_lineup)
    return new_stint_team_dict

#endregion Stint Start/End


def IncrementStats(action: dict, team_stats: dict, op_stats: dict, HomeID: int, AwayID: int, last_possession: int):
    try:
        action_type = action['actionType'].lower()
        player_id = action['personId']
        #Field Goals & Freethrows
        if action_type in ['2pt', '3pt', 'freethrow']:
            team_stats, op_stats = ParseFieldGoal(action, team_stats, op_stats)

        #Possessions
        if action.get('possession') and action.get('possession') != 0:
            team_stats, current_possession, last_possession = ParsePossession(action, team_stats, last_possession)
        #Assists
        if action.get('assistPersonId'):
            PlayerIDAst = action['assistPersonId']
            team_stats = ParseAssist(PlayerIDAst, team_stats)
        #Rebounds
        if action_type == 'rebound':
            team_stats = ParseRebound(action, team_stats)
        
        #Blocks
        if action_type == 'block':
            ParseBlock(player_id, team_stats, op_stats)

        #Steals
        if action_type == 'steal':
            team_stats = ParseSteal(player_id, team_stats)

        #Turnovers
        if action_type == 'turnover':
            team_stats = ParseTurnover(player_id, team_stats)


        if action_type == 'foul':
            team_stats, op_stats = ParseFoul(action, team_stats, op_stats)
            
    except Exception as e:
        bp = 'here'


    return team_stats, op_stats


def ParseFieldGoal(action: dict, teamStats: dict, opStats: dict):
    try:
        PlayerID = action['personId']
        shot_type = action['actionType']
        shot_result = action['shotResult']
        result_short = 'M' if shot_result == 'Made' else 'A'
        is_fieldgoal = action['isFieldGoal']
        made = shot_result == 'Made'
        if is_fieldgoal == 1:
            ShotType = f'FG{shot_type[0]}{result_short}'
            ShotValue = int(shot_type[0]) 
        else:
            ShotType = f'FT{result_short}'
            ShotValue = 1

        if made:
            teamStats[ShotType] += 1
            teamStats['PtsScored'] += ShotValue
            opStats['PtsAllowed'] += ShotValue
            teamStats['Lineup'][PlayerID]['PTS'] += ShotValue
            teamStats['Lineup'][PlayerID][ShotType] += 1
        elif ' - blocked' in action['description']:
            teamStats['Lineup'][PlayerID]['BLKd'] += 1

        if ShotValue == 1:
            teamStats['FTA'] += 1
            teamStats['Lineup'][PlayerID]['FTA'] += 1
        elif ShotValue == 2:
            teamStats['FG2A'] += 1
            teamStats['Lineup'][PlayerID]['FG2A'] += 1
        elif ShotValue == 3:
            teamStats['FG3A'] += 1
            teamStats['Lineup'][PlayerID]['FG3A'] += 1

        teamStats['FGM'] = teamStats['FG2M'] + teamStats['FG3M']
        teamStats['FGA'] = teamStats['FG2A'] + teamStats['FG3A']
        teamStats['Lineup'][PlayerID]['FGM'] = teamStats['Lineup'][PlayerID]['FG2M'] + teamStats['Lineup'][PlayerID]['FG3M']
        teamStats['Lineup'][PlayerID]['FGA'] = teamStats['Lineup'][PlayerID]['FG2A'] + teamStats['Lineup'][PlayerID]['FG3A']
        bp = 'here'
    except Exception as e:
        err = e
        raise


    return teamStats, opStats


def ParsePossession(action: dict, team_stats: dict, last_possession: int):
    current_possession = action['possession']
    if pd.notna(current_possession) and current_possession != last_possession:
        if current_possession == team_stats['TeamID']:
            team_stats['Possessions'] += 1
        last_possession = current_possession
    return team_stats, current_possession, last_possession

def ParseAssist(PlayerIDAst: int, team_stats: dict) -> dict:
    team_stats['AST'] += 1
    team_stats['Lineup'][PlayerIDAst]['AST'] += 1
    
    return team_stats

def ParseRebound(action: dict, team_stats: dict):
    PlayerID = action['personId']
    team_stats['REB'] +=1
    reb_type = f'{action['subType'][0].upper()}REB'
    team_stats[reb_type] += 1
    if PlayerID not in [None, 0]:
        team_stats['Lineup'][PlayerID]['REB'] += 1
        team_stats['Lineup'][PlayerID][reb_type] += 1

    return team_stats


def ParseBlock(PlayerID: int, team_stats: dict, op_stats: dict):
    team_stats['BLK'] += 1
    team_stats['Lineup'][PlayerID]['BLK'] += 1
    op_stats['BLKd'] += 1
    return team_stats, op_stats


def ParseTurnover(PlayerID: int, team_stats: dict) -> dict:
    team_stats['TOV'] += 1
    if PlayerID != 0:
        team_stats['Lineup'][PlayerID]['TOV'] += 1
    return team_stats

def ParseSteal(PlayerID: int, team_stats: dict) -> dict:
    team_stats['STL'] += 1
    team_stats['Lineup'][PlayerID]['STL'] += 1

    return team_stats

def ParseFoul(action: dict, team_stats: dict, op_stats: dict):
    team_stats['F'] +=1

    PlayerID = action['personId']
    if PlayerID != 0:
        team_stats['Lineup'][PlayerID]['F'] += 1
    PlayerIDFoulDrawn = action.get('foulDrawnPersonId')
    if PlayerIDFoulDrawn:
        op_stats['FDrwn'] += 1
        op_stats['Lineup'][PlayerIDFoulDrawn]['FDrwn'] += 1

    return team_stats, op_stats

#endregion Stint Parsing







#region Substitution Logic
def InitiateSubstitution(action: dict,  playbyplay_data: list, HomeID: int, AwayID: int, home: list, away: list):
    try:
        if action['actionNumber'] > action['CorrespondingSubActionNumber']:
            otherPlayerID = next((a['personId'] for a in playbyplay_data if a['actionNumber'] == action['CorrespondingSubActionNumber']), None)
            if action['teamId'] == HomeID:
                home = SubstitutePlayers(action['subType'], action['personId'], otherPlayerID, home)
            elif action['teamId'] == AwayID:
                away = SubstitutePlayers(action['subType'], action['personId'], otherPlayerID, away)
            bp = 'here'
    except TypeError as e:
        error = 'Subbing was not complete when data was pulled, no corresponding Player to sub in.'
    return home, away


def SubstitutePlayers(SubType: str, PlayerID: int, otherPlayerID: int | None, lineup: list):
    if otherPlayerID == None:
        bp = 'here'
    if SubType == 'in':
        lineup_copy = lineup.copy()
        index_out = lineup.index(otherPlayerID)
        lineup[index_out] = PlayerID
        test = lineup
        bp = 'here'
    elif SubType == 'out':
        lineup_copy = lineup.copy()
        index_out = lineup.index(PlayerID)
        lineup[index_out] = otherPlayerID
        test = lineup
        bp = 'here'


    return lineup
#endregion Substitution Logic








#region Stat Dictionaries
def CreateFirstTeamStatsDict(Game: dict, HomeID, AwayID, homeLineup, awayLineup, stintID):
    #Contents of a row in Stints table     
    teamStats = {
        'SeasonID': Game['SeasonID'],
        'GameID': Game['GameID'],
        'TeamID': 0,
        'StintID': stintID,
        'QtrStart': 1,
        'QtrEnd': 0,
        'ClockStart': '12:00.00',
        'ClockEnd': None,
        'MinElapsedStart': 0, 
        'MinElapsedEnd': None,
        'MinutesPlayed': None,
        'Possessions': 0,
        'PtsScored': 0,
        'PtsAllowed': 0,
        'FG2M': 0,
        'FG2A': 0,
        'FG3M': 0,
        'FG3A': 0,
        'FGM': 0,
        'FGA': 0,
        'FTM': 0,
        'FTA': 0,
        'AST': 0,
        'OREB': 0,
        'DREB': 0,
        'REB': 0,
        'TOV': 0,
        'STL': 0,
        'BLK': 0,
        'BLKd': 0,
        'F': 0,
        'FDrwn': 0
    }
    homeStats = teamStats.copy()
    homeStats['TeamID'] = HomeID
    homeStats['Lineup'] = {player: CreatePlayerStats(player, HomeID, Game['SeasonID'], Game['GameID'], stintID) for player in homeLineup}
    awayStats = teamStats.copy()
    awayStats['TeamID'] = AwayID
    awayStats['Lineup'] = {player: CreatePlayerStats(player, AwayID, Game['SeasonID'], Game['GameID'], stintID) for player in awayLineup}
    return homeStats, awayStats
 

def CreateTeamStats(current_stint: dict, action: dict, new_lineup: list):
    #Contents of a row in Stints table
    SeasonID = current_stint['SeasonID']
    GameID = current_stint['GameID']
    TeamID = current_stint['TeamID']
    StintID = current_stint['StintID'] + 1
    Clock = action['clock'].replace('PT', '').replace('M', ':').replace('S', '')
    team_stats = {
        'SeasonID': SeasonID,
        'GameID': GameID,
        'TeamID': TeamID,
        'StintID': StintID,
        'QtrStart': action['period'],
        'QtrEnd': 0,
        'ClockStart': Clock,
        'ClockEnd': None,
        'MinElapsedStart': current_stint['MinElapsedEnd'], 
        'MinElapsedEnd': None,
        'MinutesPlayed': 0,
        'Possessions': 0,
        'PtsScored': 0,
        'PtsAllowed': 0,
        'FG2M': 0,
        'FG2A': 0,
        'FG3M': 0,
        'FG3A': 0,
        'FGM': 0,
        'FGA': 0,
        'FTM': 0,
        'FTA': 0,
        'AST': 0,
        'OREB': 0,
        'DREB': 0,
        'REB': 0,
        'TOV': 0,
        'STL': 0,
        'BLK': 0,
        'BLKd': 0,
        'F': 0,
        'FDrwn': 0,
        'Lineup': {
            PlayerID: CreatePlayerStats(PlayerID, TeamID, SeasonID, GameID, StintID)
            for PlayerID in new_lineup
            }
    }
    return team_stats
def CreatePlayerStats(playerID, teamID, SeasonID, GameID, stintID):
    player_stats = {
        'SeasonID': SeasonID,
        'GameID': GameID,
        'TeamID': teamID,
        'StintID': stintID,
        'PlayerID': playerID,
        'MinutesPlayed': 0,
        'PlusMinus': 0,
        'PTS': 0,
        'AST': 0,
        'REB': 0,
        'FG2M': 0,
        'FG2A': 0,
        'FG3M': 0,
        'FG3A': 0,
        'FGM': 0,
        'FGA': 0,
        'FTM': 0,
        'FTA': 0,
        'OREB': 0,
        'DREB': 0,
        'TOV': 0,
        'STL': 0,
        'BLK': 0,
        'BLKd': 0,
        'F': 0,
        'FDrwn': 0
    }
    return player_stats
#endregion Stat Dictionaries