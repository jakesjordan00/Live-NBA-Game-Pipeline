from pipelines.base import Pipeline
from pipelines.scoreboard import ScoreboardPipeline
from pipelines.boxscore import BoxscorePipeline
from pipelines.playbyplay import PlayByPlayPipeline
import polars as pl

iterations = 1

scoreboard_pipeline = ScoreboardPipeline('Development', iterations)
completed_scoreboard_pipeline = scoreboard_pipeline.run()
print(completed_scoreboard_pipeline)
scoreboard_data = completed_scoreboard_pipeline['loaded']

bp = 'here'

for scoreboard in scoreboard_data.iter_rows(named=True):    
    boxscore_pipeline = BoxscorePipeline(scoreboard, 'Development', iterations)
    completed_boxscore_pipeline = boxscore_pipeline.run()
    boxscore_data = completed_boxscore_pipeline['loaded']
    
    pbp_start_action = 0
    playbyplay_pipeline = PlayByPlayPipeline(scoreboard, boxscore_data, pbp_start_action, 'Development', iterations)
    completed_playbyplay_pipeline = playbyplay_pipeline.run()
    playbyplay_data = completed_playbyplay_pipeline['loaded']
    bp = 'here'


bp = 'here'
