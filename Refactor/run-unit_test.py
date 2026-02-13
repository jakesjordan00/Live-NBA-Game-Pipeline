from pipelines.base import Pipeline
from pipelines.scoreboard import ScoreboardPipeline
from pipelines.boxscore import BoxscorePipeline
from pipelines.playbyplay import PlayByPlayPipeline
import polars as pl

iterations = 2

scoreboard_pipeline = ScoreboardPipeline('Development', iterations).run()
print(scoreboard_pipeline)
scoreboard_data = scoreboard_pipeline['loaded']

bp = 'here'

for scoreboard in scoreboard_data.iter_rows(named=True):    
    boxscore_pipeline = BoxscorePipeline(scoreboard, 'Development', iterations).run()
    boxscore_data = boxscore_pipeline['loaded']
    
    pbp_start_action = 0
    playbyplay_pipeline = PlayByPlayPipeline(scoreboard, boxscore_data, pbp_start_action, 'Development', iterations).run()
    playbyplay_data = playbyplay_pipeline['loaded']
    bp = 'here'


bp = 'here'
