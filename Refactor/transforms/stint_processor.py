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
    def __init__(self, playbyplay_data: list, sub_groups: list, boxscore_data: dict, start_action: int = 0):
        self.playbyplay_data = playbyplay_data
        self.boxscore_data = boxscore_data
        self.sub_groups = sub_groups
        self.start_action = start_action
        
        self.SeasonID = boxscore_data['Game']['SeasonID']
        self.GameID = boxscore_data['Game']['GameID']
        self.HomeID = boxscore_data['Game']['HomeID']
        self.AwayID = boxscore_data['Game']['AwayID']

        self.logger = logging.getLogger(f'StintProcessor.{self.GameID}')
    
    def process(self):

        return StintResult