import logging
from dataclasses import dataclass
from tracemalloc import start
from typing import Any

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
        last_possession = 0

        for i, action in enumerate(self.playbyplay_data[self.start_action:]):
            if action['actionNumber'] == self.current_sub_group['NextActionNumber'] or action['actionNumber'] == self.last_action['actionNumber']:
                self._switch_stint(action)
            bp = 'here'

        processed_stints = StintResult(team_stints = self.team_stints, player_stints = self.player_stints, team_player_stints=self.tp_stints)
        bp = 'here'
        return processed_stints



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

        return 
    


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
