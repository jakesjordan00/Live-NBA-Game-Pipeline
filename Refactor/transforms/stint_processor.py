import logging
from dataclasses import dataclass
from tracemalloc import start
from typing import Any
import pandas as pd

@dataclass
class StintError:
    action_number: int
    error_msg: str
    last10: list

@dataclass
class StintResult:
    team_stints: list
    player_stints: list
    team_player_stints: list
    error: StintError | None = None

#region StintProcessor
class StintProcessor:
    def __init__(self, playbyplay_data: list, boxscore_data: dict, sub_groups: list, start_action: int = 0, current_sub_group_index: int = 0):
        self.playbyplay_data = playbyplay_data
        self.boxscore_data = boxscore_data
        self.sub_groups = sub_groups
        self.start_action = start_action
        self.last_action = playbyplay_data[-1]
        self.current_sub_group_index = current_sub_group_index
        
        self.SeasonID = boxscore_data['Game']['SeasonID']
        self.GameID = boxscore_data['Game']['GameID']
        self.HomeID = boxscore_data['Game']['HomeID']
        self.AwayID = boxscore_data['Game']['AwayID']
        self.GameStatus = boxscore_data['GameExt']['Status']

        self.logger = logging.getLogger(f'StintProcessor.{self.GameID}')


    def process(self):
        self.logger.info(f'Processing Stints for {self.GameID}')

        self.team_stints = []
        self.player_stints = []
        self.tp_stints = []


        if self.start_action == 0:
            self.home, self.away = self._get_starting_lineups()
            self.home_stats, self.away_stats = self._create_initial_stats_dict(self.home, self.away)
            self.current_sub_group = {'PointInGame': 99, 'NextActionNumber': 9999, 'SubTime': "", 'Period': 1, 'Clock': "0"}
        else:
            #Need to get the lineup as of the start action.
            #If start_action != 0, we should get it from the sub group proior to the current
            pass
        
        self.home_copy = self.home.copy()
        self.away_copy = self.away.copy()

        for i, action in enumerate(self.playbyplay_data[self.start_action:]):
            action_number = action['actionNumber']
            action_type = action['actionType'] 
            if action_number == self.current_sub_group['NextActionNumber'] or action_number == self.last_action['actionNumber']:
                self._switch_stint(action)

            TeamID = action.get('teamId')
            if TeamID == None:
                continue
            is_home = TeamID == self.HomeID
            self.team_stats = self.home_stats if is_home else self.away_stats
            self.op_stats = self.away_stats if is_home else self.home_stats

            last_possession = self.playbyplay_data[self.start_action+i-1]['possession'] if i > 0 else 0

            if action_type == 'substitution':
                if action_number != self.last_action['actionNumber']:
                    self._initiate_substitution(action)
            elif action_type != 'substitution':
                self._increment_stats(action, last_possession)

            bp = 'here'

        processed_stints = StintResult(team_stints = self.team_stints, player_stints = self.player_stints, team_player_stints=self.tp_stints)
        bp = 'here'
        return processed_stints


    #region Stint Changing
    def _switch_stint(self, action: dict):
        do_home = self.home != self.home_copy
        do_away = self.away != self.away_copy
        stat_list = [self.home_stats, self.away_stats]
        stat_dict_list = [{
            'home_away': 'Home',
            'stats': self.home_stats,
            'sub_needed': do_home,
            'team_id': self.HomeID,
            'old_lineup': self.home,
            'new_lineup': self.home_copy
        },{
            'home_away': 'Away',
            'stats': self.away_stats,
            'sub_needed': do_away,
            'team_id': self.AwayID,
            'old_lineup': self.away,
            'new_lineup': self.away_copy
        }]
        self._stint_end(action, stat_dict_list)

        if do_home:
            self.home_stats = self._create_team_stats(self.home_stats, action, stat_dict_list[0]['new_lineup'])
            self.home = list(self.home_stats['Lineup'].keys())
        if do_away:
            self.away_stats = self._create_team_stats(self.away_stats, action, stat_dict_list[1]['new_lineup'])
            self.away = list(self.away_stats['Lineup'].keys())
            
        if action['actionNumber'] != self.last_action['actionNumber']:
            self.current_sub_group_index += 1
            self.sub_groups.append({
                        'PointInGame': 999,
                        'NextActionNumber': self.last_action['actionNumber'],
                        'SubTime': "",
                        'Period': 1,
                        'Clock': "0"
                    })
            self.current_sub_group = self.sub_groups[self.current_sub_group_index]

    


    def _stint_end(self, action: dict, stat_dict_list: list):
        for dict in stat_dict_list:
            sub_needed = dict['sub_needed'] or action['actionNumber'] == self.last_action['actionNumber']
            #If we don't need a sub, don't do anything
            if sub_needed == False: 
                continue
            stat_dict = dict['stats']
            stat_dict['MinutesPlayed'] = round(action['MinElapsed'] - stat_dict['MinElapsedStart'], 2)
            if 'Final' not in self.GameStatus and action['actionType'] != 'substitution' and self.last_action['actionType'] != 'substitution':
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
                self.player_stints.append(playerStats.copy())

            team_stint = {key: value for key, value in stat_dict.items() if key != 'Lineup'}
            self.team_stints.append(team_stint)
            self.tp_stints.append(stat_dict)
    
    #endregion Stint Changing


    #region Action Parsing
    def _initiate_substitution(self, action: dict):
        try:
            if(action['actionNumber'] > action['CorrespondingSubActionNumber']):
                other_PlayerID = next((act['personId'] for act in self.playbyplay_data if act['actionNumber'] == action['CorrespondingSubActionNumber']), None)
                if action['teamId'] == self.HomeID:
                    SubstitutePlayers(action['subType'], action['personId'], other_PlayerID, self.home_copy)
                if action['teamId'] == self.AwayID:
                    SubstitutePlayers(action['subType'], action['personId'], other_PlayerID, self.away_copy)
        except TypeError as e:
            error = 'Subbing was not complete when data was pulled, no corresponding Player to sub in.'



    def _increment_stats(self, action: dict, last_possession: int):
        try:
            action_type = action['actionType'].lower()
            player_id = action['personId']

            #Possession    
            if action.get('possession') and action.get('possession') != 0:
                self._parse_possession(action, last_possession)
            #Field Goal or Freethrow
            if action_type in ['2pt', '3pt', 'freethrow']:
                self._parse_fieldgoal(action)
                #Assist
                if action.get('assistPersonId'):
                    PlayerIDAst = action['assistPersonId']
                    self._parse_assist(action)

            
            #Rebound
            if action_type == 'rebound':
                self._parse_rebound(action)


            #Block
            if action_type == 'block':
                self._parse_block(player_id)

            #Steal
            if action_type == 'rebound':
                self._parse_steal(player_id)

            #Turnover
            if action_type == 'rebound':
                self._parse_turnover(player_id)

            #Foul
            if action_type == 'foul':
                self._parse_foul(action)


            
        except Exception as e:
            bp = 'here'
        
        return last_possession
        

    
    def _parse_possession(self, action: dict, last_possession: int):
        current_possession = action['possession']
        if pd.notna(current_possession) and current_possession != last_possession:
            if current_possession == self.team_stats['TeamID']:
                self.team_stats['Possessions'] += 1
            last_possession = current_possession

    def _parse_fieldgoal(self, action: dict):
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
                self.team_stats[ShotType] += 1
                self.team_stats['PtsScored'] += ShotValue
                self.op_stats['PtsAllowed'] += ShotValue
                self.team_stats['Lineup'][PlayerID]['PTS'] += ShotValue
                self.team_stats['Lineup'][PlayerID][ShotType] += 1
            elif ' - blocked' in action['description']:
                self.team_stats['Lineup'][PlayerID]['BLKd'] += 1

            if ShotValue == 1:
                self.team_stats['FTA'] += 1
                self.team_stats['Lineup'][PlayerID]['FTA'] += 1
            elif ShotValue == 2:
                self.team_stats['FG2A'] += 1
                self.team_stats['Lineup'][PlayerID]['FG2A'] += 1
            elif ShotValue == 3:
                self.team_stats['FG3A'] += 1
                self.team_stats['Lineup'][PlayerID]['FG3A'] += 1

            self.team_stats['FGM'] = self.team_stats['FG2M'] + self.team_stats['FG3M']
            self.team_stats['FGA'] = self.team_stats['FG2A'] + self.team_stats['FG3A']
            self.team_stats['Lineup'][PlayerID]['FGM'] = self.team_stats['Lineup'][PlayerID]['FG2M'] + self.team_stats['Lineup'][PlayerID]['FG3M']
            self.team_stats['Lineup'][PlayerID]['FGA'] = self.team_stats['Lineup'][PlayerID]['FG2A'] + self.team_stats['Lineup'][PlayerID]['FG3A']
        except Exception as e:
            err = e
            raise


    def _parse_assist(self, PlayerIDAst):
        self.team_stats['Lineup'][PlayerIDAst]['AST'] += 1


    def _parse_rebound(self, action:dict):
        PlayerID = action['personId']
        self.team_stats['REB'] += 1
        reb_type = f'{action['subType'][0].upper()}REB'
        self.team_stats[reb_type] += 1
        if PlayerID not in [None, 0]:
            self.team_stats['Lineup'][PlayerID]['REB'] += 1
            self.team_stats['Lineup'][PlayerID][reb_type] += 1

    def _parse_block(self, PlayerID: int):
        self.team_stats['BLK'] += 1
        self.team_stats['Lineup'][PlayerID]['BLK'] += 1
        self.op_stats['BLKd'] += 1

    def _parse_steal(self, PlayerID: int):
        self.team_stats['STL'] += 1
        self.team_stats['Lineup'][PlayerID]['STL'] += 1


    def _parse_turnover(self, PlayerID: int):
        self.team_stats['TOV'] += 1
        if PlayerID != 0:
            self.team_stats['Lineup'][PlayerID]['TOV'] += 1


    def _parse_foul(self, action:dict):
        self.team_stats['F'] +=1

        PlayerID = action['personId']
        if PlayerID != 0:
            self.team_stats['Lineup'][PlayerID]['F'] += 1
        PlayerIDFoulDrawn = action.get('foulDrawnPersonId')
        if PlayerIDFoulDrawn:
            self.op_stats['FDrwn'] += 1
            self.op_stats['Lineup'][PlayerIDFoulDrawn]['FDrwn'] += 1



    #endregion Action Parsing






    #region pre-processing

    def _pre_process_existing_games(self) -> tuple[int, int, dict, dict]:
        '''
        Determines starting position of Stint Processor when data already exists for game. Part of pre-processing function group

        :returns current_action, current_sub_group_index, current_sub_group, start_sub_group: Four-element tuple containing:

            * **current_action** (*dict*): Action found at index of start_action

            * **current_sub_group_index** (*int*): Index of the current_sub_group (where the next sub occurs)

            * **current_sub_group** (*dict*): Details of when to perform the next substitution

            * **start_sub_group** (*dict*): We should get the sub group prior to the one we're on and start from their NextActionNumber value
        '''
        current_action = self.playbyplay_data[self.start_action]
        current_sub_group_index = [i for i, sub in enumerate(self.sub_groups) if sub['PointInGame'] <= current_action['PointInGame']][::-1][0]
        current_sub_group = self.sub_groups[self.current_sub_group_index]
        start_sub_group = self.sub_groups[self.current_sub_group_index - 1]

        sub_group_start_action_Number = start_sub_group['NextActionNumber']


        return current_action, current_sub_group_index, current_sub_group, start_sub_group


    def _get_starting_lineups(self) -> tuple[list, list]:
        '''
        Returns the starting lineups for home and away teams. Part of pre-processing function group

        :returns home, away: Two-element tuple containing:

            * **home** (*list*): Home team starter PlayerIDs

            * **away** (*list*): Away team starter PlayerIDs
        '''
        lineups = self.boxscore_data['StartingLineups']
        home = [player['PlayerID'] for player in lineups if player['TeamID'] == self.HomeID and player['Unit'] == 'Starters']
        away = [player['PlayerID'] for player in lineups if player['TeamID'] == self.AwayID and player['Unit'] == 'Starters']
        return home, away
    
    
    def _create_initial_stats_dict(self, home, away) -> tuple[dict, dict]:
        '''
        If game has yet to be loaded, create an emtpy Team Stats dictionary for each team. Part of pre-processing function group
        
        :returns home_stats, away_stats: Two-element tuple containing:

            * **home_stats** (*list*): Stats dictionary for Home Team, containing all Home Players' stat dictionaries

            * **away_stats** (*list*): Stats dictionary for Away Team, containing all Away Players' stat dictionaries
        '''
        team_stats = {
            'SeasonID': self.SeasonID,
            'GameID': self.GameID,
            'TeamID': 0,
            'StintID': 1,
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
        home_stats = team_stats.copy()
        home_stats['TeamID'] = self.HomeID
        home_stats['Lineup'] = {PlayerID: self._create_player_stats(self.HomeID, 1, PlayerID) for PlayerID in home}
        away_stats = team_stats.copy()
        away_stats['TeamID'] = self.AwayID
        away_stats['Lineup'] = {PlayerID: self._create_player_stats(self.AwayID, 1, PlayerID) for PlayerID in away}


        return home_stats, away_stats
    #endregion pre-processing




    #region stat dictionaries

    def _create_team_stats(self, current_stint: dict, action: dict, new_lineup: list):
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
                PlayerID: self._create_player_stats(PlayerID, TeamID, StintID)
                for PlayerID in new_lineup
                }
        }
        return team_stats

    def _create_player_stats(self, TeamID, StintID, PlayerID) -> dict:
        '''
        Generates Stats dictionary for each Player currently on court.
        
        :param TeamID: Unique ID of Team Player is playing for
        :param StintID: Unique ID of the Stint the player is partaking in 
        :param PlayerID: Unique ID of the Player stats are being recorded for

        :return player_stats (*dict*): Dictionary containing each player's stats for each stint
        '''
        player_stats = {
            'SeasonID': self.SeasonID,
            'GameID': self.GameID,
            'TeamID': TeamID,
            'StintID': StintID,
            'PlayerID': PlayerID,
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

    #endregion stat dictionaries



#endregion StintProcessor


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