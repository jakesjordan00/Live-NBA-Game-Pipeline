import logging
from dataclasses import dataclass
from tracemalloc import start

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


class StintProcessor:
    def __init__(self, playbyplay_data: list, boxscore_data: dict, sub_groups: list, start_action: int = 0, current_sub_group_index: int = 0):
        self.playbyplay_data = playbyplay_data
        self.boxscore_data = boxscore_data
        self.sub_groups = sub_groups
        self.start_action = start_action
        self.current_sub_group_index = current_sub_group_index
        
        self.SeasonID = boxscore_data['Game']['SeasonID']
        self.GameID = boxscore_data['Game']['GameID']
        self.HomeID = boxscore_data['Game']['HomeID']
        self.AwayID = boxscore_data['Game']['AwayID']

        self.logger = logging.getLogger(f'StintProcessor.{self.GameID}')


    def process(self):
        self.logger.info(f'Processing Stints for {self.GameID}')

        team_stints = []
        player_stints = []
        tp_stints = []

        if self.start_action == 0:
            home, away = self._get_starting_lineups()
            home_stats, away_stats = self._create_initial_stats_dict(home, away)
            current_sub_group = {'PointInGame': 99, 'NextActionNumber': 9999, 'SubTime': "", 'Period': 1, 'Clock': "0"}

        else:
            #Need to get the lineup as of the start action.
            #If start_action != 0, we should get it from the sub group proior to the current
            bp = 'here'
        
        processed_stints = StintResult(team_stints = team_stints, player_stints = player_stints, team_player_stints=tp_stints)
        bp = 'here'
        return processed_stints













    def _get_starting_lineups(self)-> tuple[list, list]:
        """
        Returns the starting lineups for home and away teams.
        
        :returns tuple[home, away]: Two-element tuple containing:
            
            * **home** (*list*): Home team starter PlayerIDs
            * **away** (*list*): Away team starter PlayerIDs
        """
        lineups = self.boxscore_data['StartingLineups']
        home = [player['PlayerID'] for player in lineups if player['TeamID'] == self.HomeID and player['Unit'] == 'Starters']
        away = [player['PlayerID'] for player in lineups if player['TeamID'] == self.AwayID and player['Unit'] == 'Starters']
        return home, away
    
    
    def _create_initial_stats_dict(self, home, away): 
        teamStats = {
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
        home_stats = teamStats.copy()
        home_stats['TeamID'] = self.HomeID
        home_stats['Lineup'] = {PlayerID: self._create_player_stats(self.HomeID, 1, PlayerID) for PlayerID in home}
        away_stats = teamStats.copy()
        home_stats['TeamID'] = self.AwayID
        away_stats['Lineup'] = {PlayerID: self._create_player_stats(self.AwayID, 1, PlayerID) for PlayerID in away}


        return home_stats, away_stats
    
    def _create_player_stats(self, TeamID, StintID, PlayerID):
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
    
        

