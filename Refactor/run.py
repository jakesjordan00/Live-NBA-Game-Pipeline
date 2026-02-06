from pipelines.base import Pipeline
from pipelines.scoreboard import ScoreboardPipeline
from pipelines.boxscore import BoxscorePipeline
from pipelines.playbyplay import PlayByPlayPipeline

pipeline = ScoreboardPipeline()
result = pipeline.run()
bp = 'here'
print(result)

pipeline2 = BoxscorePipeline(result['loaded']).run()

bp = 'here'