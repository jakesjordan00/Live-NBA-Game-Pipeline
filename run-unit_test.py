from pipelines import Pipeline, ScoreboardPipeline, BoxscorePipeline, PlayByPlayPipeline
from connectors import SQLConnector
import polars as pl


scoreboard_pipeline = ScoreboardPipeline('Development')
completed_scoreboard_pipeline = scoreboard_pipeline.run()
scoreboard_data = completed_scoreboard_pipeline['loaded']


gameIDs_in_progress = [game['GameID'] for game in scoreboard_data]
print(f'\nGames in Progress: {', '.join(str(game) for game in gameIDs_in_progress)}\n------------------------------------')

for scoreboard in scoreboard_data: 
    print(f'\n                                                 {scoreboard['GameID']}\n                                   -------------------------------------')

    boxscore_pipeline = BoxscorePipeline(scoreboard, 'Production')
    completed_boxscore_pipeline = boxscore_pipeline.run()
    boxscore_data = completed_boxscore_pipeline['loaded']
    
    start_action = boxscore_pipeline.destination.cursor_query('PlayByPlay', boxscore_data['start_action_keys'])['actions']
    home_stats, away_stats = (None, None) if start_action == 0 else boxscore_pipeline.destination.stint_cursor(boxscore_data['lineup_keys'])
    playbyplay_pipeline = PlayByPlayPipeline(boxscore_data, start_action, home_stats, away_stats, 'Production')
    completed_playbyplay_pipeline = playbyplay_pipeline.run()
    playbyplay_data = completed_playbyplay_pipeline['loaded']
    bp = 'here'


bp = 'here'
