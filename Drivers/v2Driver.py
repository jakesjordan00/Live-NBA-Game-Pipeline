
import sys
import os
from sqlalchemy import false
import time
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GetScoreboard import GetTodaysScoreboard
from Directions import GetGamesInProgress, Wait
from SQL_Reads import FirstIteration
from GetDataNBA import GetBox, GetPlayByPlay, InsertBox, InsertPbp, UpdateBox
from FirstRunCoDriver import NewGameData, ExistingGameData

import Extract.StaticData as e
import Transform.Schedule as ts



schedule = e.FetchData('https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_1.json', 'Schedule')
schedule = ts.TransformSchedule(schedule)


def MainFunction(iterations: int, dbGames: list, sender: str):



    
    return 1, 1, 1, 1



iterations = 0
dbGames, iterations, allStartTimes, programMap = MainFunction(iterations, [], 'Default', )