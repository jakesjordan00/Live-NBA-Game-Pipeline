from pipelines.base import Pipeline
from pipelines.scoreboard import ScoreboardPipeline
from pipelines.boxscore import BoxscorePipeline
from pipelines.playbyplay import PlayByPlayPipeline
from connectors.sql import SQLConnector
import polars as pl

iterations = 5

scoreboard_pipeline = ScoreboardPipeline('Development', iterations)
completed_scoreboard_pipeline = scoreboard_pipeline.run()
print(completed_scoreboard_pipeline)
scoreboard_data = completed_scoreboard_pipeline['loaded']

bp = 'here'

for scoreboard in scoreboard_data.iter_rows(named=True):    
    boxscore_pipeline = BoxscorePipeline(scoreboard, 'Development', iterations)
    completed_boxscore_pipeline = boxscore_pipeline.run()
    boxscore_data = completed_boxscore_pipeline['loaded']
    bp = 'here'
    start_action = boxscore_pipeline.destination.cursor_query('PlayByPlay', boxscore_data['start_action_keys'])
    home_stats, away_stats = (None, None) if start_action == 0 else boxscore_pipeline.destination.stint_cursor(boxscore_data['lineup_keys'])
    playbyplay_pipeline = PlayByPlayPipeline(scoreboard, boxscore_data, start_action, home_stats, away_stats, 'Development', iterations)
    completed_playbyplay_pipeline = playbyplay_pipeline.run()
    playbyplay_data = completed_playbyplay_pipeline['loaded']
    bp = 'here'


bp = 'here'
