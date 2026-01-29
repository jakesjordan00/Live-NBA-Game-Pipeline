
import sys
import os

from sqlalchemy import false
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from GetScoreboard import GetTodaysScoreboard
from Directions import GetGamesInProgress, Wait
from SQL_Reads import FirstIteration
from GetDataNBA import GetBox, GetPlayByPlay, InsertBox, InsertPbp, UpdateBox
from FirstRunCoDriver import NewGameData, ExistingGameData



import time
from datetime import datetime




def MainFunction(iterations: int, dbGames: list, sender: str, programMap: str):



    return 1