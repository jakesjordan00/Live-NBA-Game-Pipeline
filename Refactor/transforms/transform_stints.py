import pandas as pd

#region Substitution Groups
def DetermineSubstitutions(data_extract_full: dict, boxscore_data: dict):
    static_data_extract = data_extract_full['static_data_extract']
    # api_data_extract = data_extract_full['api_data_extract']
    playbyplay_static_data = static_data_extract['game']['actions']
    # playbyplay_api_data = api_data_extract['game']['actions']

    sub_in_actions = 0
    sub_out_actions = 0
    home_in = 0
    home_out = 0
    away_in = 0
    away_out = 0
    sub_groups = []
    
    Periods = 4 if boxscore_data['GameExt']['Periods'] <= 4 else boxscore_data['GameExt']['Periods']
    for i, action in enumerate(playbyplay_static_data):
        Qtr = action['period']
        Clock = action['clock'].replace('PT', '').replace('M', ':').replace('S', '')
        PointInGame, MinElapsed = CalculatePointInGame(Clock, Qtr, Periods)
        action['PointInGame'] = PointInGame
        action['MinElapsed'] = MinElapsed
        action['Clock'] = Clock


        # item['descriptionAPI'] = next((api['description'] for api in playbyplay_api_data if item['actionNumber'] == api['actionNumber']), None)
        if action['actionType'] == 'substitution' or (action['actionType'] == 'game' and action['subType'] == 'end'):
            SubTime = f'Q{Qtr} {Clock}'
            game_end = 1 if action['actionType'] == 'game' and action['subType'] == 'end' else 0
            NextActionNumber = playbyplay_static_data[i+1]['actionNumber'] if game_end == 0 else action['actionNumber']
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



    for action in playbyplay_static_data:
        if action['actionType'] == 'substitution':
            bp = 'here'
            if action['subType'] == 'in':
                subs_type = 'SubIn'
                opp_subs_type = 'SubOut'
            else:
                subs_type = 'SubOut'
                opp_subs_type = 'SubIn'
            action['CorrespondingSubActionNumber'] = next(
                (p['actionNumber'] for p in playbyplay_static_data
                if p['actionNumber'] != action['actionNumber']  # don't match itself
                and action[f'{subs_type}Number'] == p[f'{opp_subs_type}Number']
                and action[f'Team{subs_type}Number'] == p[f'Team{opp_subs_type}Number']),
                None  # default if no match found
            )
            bp = 'here'


    return playbyplay_static_data, sub_groups

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
def Stints(playbyplay_data: list, transformed_playbyplay: list, sub_groups: list, start_action: int, boxscore_data: dict):
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
    current_sub_group = sub_groups[current_sub_group_index]
    if start_action != 0:
        currectAction = playbyplay_data[start_action]
        current_sub_group_index = [i for i, s in enumerate(sub_groups) if s['PointInGame'] <= currectAction['PointInGame']][::-1][0]
        current_sub_group = sub_groups[current_sub_group_index]
        start_sub_group = sub_groups[current_sub_group_index-1] #left off here 2/11



    home_copy = home.copy()
    away_copy = away.copy()
    bp = 'here'
    for i, action in enumerate(playbyplay_data[start_action:]):
        #End Stint if Substitutions are done
        if action['actionNumber'] == current_sub_group['NextActionNumber']:
            do_home = home != home_copy
            do_away = away != away_copy
            stat_list = [homeStats, awayStats]
            stat_dict_list = [{
                'home_away': 'Home',
                'stats': homeStats,
                'sub_needed': do_home,
                'team_id': HomeID
            },{
                'home_away': 'Away',
                'stats': awayStats,
                'sub_needed': do_away,
                'team_id': AwayID
            }]
            #End Stint logic
            team_stints, player_stints = StintEnding(action, stat_dict_list, team_stints, player_stints, team_player_stints, gameStatus)
            StintStarting()
            #If we arent at the last action, iterate:
            if action['actionNumber'] != final_action['actionNumber']:
                current_sub_group_index += 1
                current_sub_group = sub_groups[current_sub_group_index]
        

        #begin Stint parsing
        TeamID = action.get('teamId')
        if TeamID == None:
            continue
        isHome = TeamID == HomeID
        teamStats = homeStats if isHome and TeamID != None else awayStats
        opStats = awayStats if isHome and TeamID != None else homeStats
        actionType = action['actionType']

        if actionType == 'substitution':
            home_copy, away_copy = InitiateSubstitution(action, playbyplay_data, HomeID, AwayID, home_copy, away_copy)

        elif actionType != 'substitution':
            teamStats, opStats = IncrementStats(action, teamStats, opStats, HomeID, AwayID)


    return


#region Stint Start/End
def StintEnding(action: dict, stat_dict_list: list, team_stints: list, player_stints: list, team_player_stints: list, gameStatus: str):
    '''
    Docstring for StintEnding
    
    :param action: Description
    :type action: dict
    :param stat_dict_list: Description
    :type stat_dict_list: list
    :param team_stints: Description
    :type team_stints: list
    :param player_stints: Description
    :type player_stints: list
    :param team_player_stints: Description
    :type team_player_stints: list
    :param gameStatus: Description
    :type gameStatus: str
    ''' 

    for dict in stat_dict_list:
        sub_needed = dict['sub_needed']
        #If we don't need a sub, don't do anything
        #
        if sub_needed == False: 
            continue
        stat_dict = dict['stats']
        stat_dict['MinutesPlayed'] = round(action['MinElapsed'] - stat_dict['MinElapsedStart'], 2)
        if 'Final' not in gameStatus and action['actionType'] != 'substitution':
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

    # home_stats = stat_dict_list[0]['stats']
    # away_stats = stat_dict_list[1]['stats']

    return team_stints, player_stints

def StintStarting():


    return

#endregion Stint Start/End


def IncrementStats(action: dict, teamStats: dict, opStats: dict, HomeID: int, AwayID: int):
    actionType = action['actionType']

    if actionType in ['2pt', '3pt', 'freethrow']:
        teamStats, opStats = ParseFieldGoals(action, teamStats, opStats)


    return teamStats, opStats



def ParseFieldGoals(action: dict, teamStats: dict, opStats: dict):
    try:
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
            teamStats['Lineup'][action['personId']]['PTS'] += ShotValue
            teamStats['Lineup'][action['personId']][ShotType] += 1
        if ShotValue == 1:
            teamStats['FTA'] += 1
            teamStats['Lineup'][action['personId']]['FTA'] += 1
        elif ShotValue == 2:
            teamStats['FG2A'] += 1
            teamStats['Lineup'][action['personId']]['FG2A'] += 1
        elif ShotValue == 3:
            teamStats['FG3A'] += 1
            teamStats['Lineup'][action['personId']]['FG3A'] += 1

        teamStats['FGM'] = teamStats['FG2M'] + teamStats['FG3M']
        teamStats['FGA'] = teamStats['FG2A'] + teamStats['FG3A']
        teamStats['Lineup'][action['personId']]['FGM'] = teamStats['Lineup'][action['personId']]['FG2M'] + teamStats['Lineup'][action['personId']]['FG3M']
        teamStats['Lineup'][action['personId']]['FGA'] = teamStats['Lineup'][action['personId']]['FG2A'] + teamStats['Lineup'][action['personId']]['FG3A']
        bp = 'here'
    except Exception as e:
        err = e
        raise


    return teamStats, opStats
#endregion Stint Parsing







#region Substitution Logic
def InitiateSubstitution(action: dict,  playbyplay_data: list, HomeID: int, AwayID: int, home: list, away: list):
    if action['actionNumber'] > action['CorrespondingSubActionNumber']:
        otherPlayerID = next((a['personId'] for a in playbyplay_data if a['actionNumber'] == action['CorrespondingSubActionNumber']), None)
        if action['teamId'] == HomeID:
            home = SubstitutePlayers(action['subType'], action['personId'], otherPlayerID, home)
        elif action['teamId'] == AwayID:
            away = SubstitutePlayers(action['subType'], action['personId'], otherPlayerID, away)
        bp = 'here'
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
        'F': 0
    }
    homeStats = teamStats.copy()
    homeStats['TeamID'] = HomeID
    homeStats['Lineup'] = {player: CreatePlayerStats(player, HomeID, Game['SeasonID'], Game['GameID'], stintID) for player in homeLineup}
    awayStats = teamStats.copy()
    awayStats['TeamID'] = AwayID
    awayStats['Lineup'] = {player: CreatePlayerStats(player, AwayID, Game['SeasonID'], Game['GameID'], stintID) for player in awayLineup}
    return homeStats, awayStats


def CreateTeamStats(Game: dict, HomeID, AwayID, homeLineup, awayLineup, stintID):
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
        'F': 0
    }
    homeStats = teamStats.copy()
    homeStats['TeamID'] = HomeID
    homeStats['Lineup'] = {player: CreatePlayerStats(player, HomeID, Game['SeasonID'], Game['GameID'], stintID) for player in homeLineup}
    awayStats = teamStats.copy()
    awayStats['TeamID'] = AwayID
    awayStats['Lineup'] = {player: CreatePlayerStats(player, AwayID, Game['SeasonID'], Game['GameID'], stintID) for player in awayLineup}
    return homeStats, awayStats
def CreatePlayerStats(playerID, teamID, SeasonID, GameID, stintID):
        return {
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
        'F': 0
    }

#endregion Stat Dictionaries