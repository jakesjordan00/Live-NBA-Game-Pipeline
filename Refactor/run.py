from pipelines.base import Pipeline
from pipelines.scoreboard import ScoreboardPipeline
from pipelines.boxscore import BoxscorePipeline
from pipelines.playbyplay import PlayByPlayPipeline
import polars as pl

scoreboard_pipeline = ScoreboardPipeline().run()
print(scoreboard_pipeline)
scoreboard_data = scoreboard_pipeline['loaded']

bp = 'here'

for scoreboard in scoreboard_data.iter_rows(named=True):    
    boxscore_pipeline = BoxscorePipeline(scoreboard).run()
    boxscore_data = boxscore_pipeline['loaded']
    bp = 'here'
    playbyplay_pipeline = PlayByPlayPipeline(scoreboard, boxscore_data).run()
    bp = 'here'


bp = 'here'
