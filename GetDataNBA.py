from URLs import BoxScore, PlayByPlay
import requests
import pandas as pd


def GetBox(GameID):
    try:
        response = requests.get(f'{BoxScore}00{GameID}.json')
        data = response.json()
        columns = data['game']
        dfBox = pd.DataFrame(data['game'])
    except Exception as e:
        dfBox = pd.DataFrame()
        print(f"Error downloading PlayerGameLogs: {e}")

    return dfBox

    return 1




def GetPlayByPlay():

    return 1