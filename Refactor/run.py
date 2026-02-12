from pipelines.base import Pipeline
from pipelines.scoreboard import ScoreboardPipeline
from pipelines.boxscore import BoxscorePipeline
from pipelines.playbyplay import PlayByPlayPipeline
import polars as pl

#Will replace the iterations with something better
iterations = 0 

scoreboard_pipeline = ScoreboardPipeline('Production', iterations).run()
print(scoreboard_pipeline)
scoreboard_data = scoreboard_pipeline['loaded']

bp = 'here'

for scoreboard in scoreboard_data.iter_rows(named=True):    
    boxscore_pipeline = BoxscorePipeline(scoreboard, 'Production', iterations).run()
    boxscore_data = boxscore_pipeline['loaded']
    
    pbp_start_action = 0
    playbyplay_pipeline = PlayByPlayPipeline(scoreboard, boxscore_data, pbp_start_action, 'Production', iterations).run()
    playbyplay_data = playbyplay_pipeline['loaded']
    bp = 'here'


bp = 'here'
