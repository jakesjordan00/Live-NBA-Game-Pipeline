import pandas as pd


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


        # item['descriptionAPI'] = next((api['description'] for api in playbyplay_api_data if item['actionNumber'] == api['actionNumber']), None)
        if action['actionType'] == 'substitution':
            SubTime = f'Q{Qtr} {Clock}'
            NextActionNumber = playbyplay_static_data[i+1]['actionNumber']
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

def Stints(playbyplay_data: list, transformed_playbyplay: list, sub_groups: list, start_action: int, boxscore_data: dict):
    
    for i, action in enumerate(playbyplay_data[start_action:]):
        print(f'Point In Game: {action['PointInGame']}          Clock: {action['clock']}')
    final_action = playbyplay_data[-1]
    if start_action == 0:
        HomeID = boxscore_data['Game']['HomeID']
        AwayID = boxscore_data['Game']['AwayID']
        lineups = boxscore_data['StartingLineups']
        home = [player['PlayerID'] for player in lineups if player['TeamID'] == HomeID and player['Unit'] == 'Starters']
        away = [player['PlayerID'] for player in lineups if player['TeamID'] == AwayID and player['Unit'] == 'Starters']
        bp = 'here'
    
    current_sub_group_index = 0
    if start_action != 0:
        currectAction = playbyplay_data[start_action]
        current_sub_group_index = [i for i, s in enumerate(sub_groups) if s['PointInGame'] <= currectAction['PointInGame']][::-1][0]

    current_sub_group = sub_groups[current_sub_group_index]
    bp = 'here'
    home_copy = home.copy()
    away_copy = away.copy()
    for i, action in enumerate(playbyplay_data[start_action:]):
        if action['actionType'] == 'substitution':
            home_copy, away_copy = Stint(action, playbyplay_data, HomeID, AwayID, home_copy, away_copy)
        elif action['actionNumber'] == current_sub_group['NextActionNumber']:
            bp = 'here'
            h = home
            hc = home_copy

            a = away
            ac = away_copy
            bp = 'here'

            #End Stint logic


            current_sub_group_index += 1
            current_sub_group = sub_groups[current_sub_group_index]
            bp = 'here'

    return





def Stint(action: dict,  playbyplay_data: list, HomeID: int, AwayID: int, home: list, away: list):
    if action['actionNumber'] > action['CorrespondingSubActionNumber']:
        otherPlayerID = next((a['personId'] for a in playbyplay_data if a['actionNumber'] == action['CorrespondingSubActionNumber']), None)
        if action['teamId'] == HomeID:
            home = SubstitutePlayers(action['subType'], action['personId'], otherPlayerID, home)
        elif action['teamId'] == AwayID:
            away = SubstitutePlayers(action['subType'], action['personId'], otherPlayerID, away)
        bp = 'here'
    return home, away


def SubstitutePlayers(SubType: str, PlayerID: int, otherPlayerID: int, lineup: list):
    
    if SubType == 'in':
        lineup_copy = lineup.copy()
        index_out = lineup.index(otherPlayerID)
        lineup[index_out] = PlayerID
        test = lineup
        bp = 'here'
    elif SubType == 'out':
        lineup.remove(PlayerID)
        lineup.add(otherPlayerID)

    return lineup


def CalculatePointInGame(Clock: str, Period: int, Periods: int):
    cMinutes = int(Clock[0:2])
    cSeconds = float(Clock[-5:])
    MinElapsed = round(12 - (cMinutes + (cSeconds / 60)) + ((Period - 1) * 12), 4)
    minCalc = (cMinutes + (cSeconds / 60))


    total_game_time = (12 * 4) + ((Periods - Period) * 5)
    PointInGame = round(((MinElapsed / total_game_time) * 100), 4)
    return PointInGame, MinElapsed

