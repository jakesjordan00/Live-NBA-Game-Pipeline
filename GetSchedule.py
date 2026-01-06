from datetime import datetime, timedelta
from pathlib import Path
import requests
import pandas as pd  
from Headers import scoreboard
import urllib3
import json



def GetTodaysScoreboard():
    try:
        response = requests.get('https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_1.json')
        data = response.json()
        columns = data['scoreboard']['games']
        dfSchedule = pd.DataFrame(data['scoreboard']['games'])
    except Exception as e:
        dfScoreboard = pd.DataFrame()
        print(f"Error downloading PlayerGameLogs: {e}")

    return dfScoreboard
