
import sys
import os
from sqlalchemy import false
import time
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import Extract as e
import Transform as t



schedule = e.StaticData.FetchData('https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_1.json', 'Schedule')
schedule = t.Schedule.Transform(schedule)


def MainFunction(iterations: int, dbGames: list, sender: str):

    scoreboard = e.StaticData.FetchData('https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json', 'Scoreboard')


    
    return 1, 1, 1



iterations = 0
dbGames, iterations, allStartTimes = MainFunction(iterations, [], 'Default', )