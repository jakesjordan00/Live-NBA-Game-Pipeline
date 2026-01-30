
import requests



def FetchData(url: str, sender: str):
    try:
        response = requests.get(url)
        jsonResponse = response.json()
    except Exception as e:
        print(f"Error: {e}")
    try:
        if sender == 'Schedule': #Schedule            
            data = jsonResponse['leagueSchedule']['gameDates']
        elif sender == 'Scoreboard': #Scoreboard
            data = jsonResponse['scoreboard']['games']
        elif sender == 'Box': #Boxscore
            data = jsonResponse['game']
        elif sender == 'PlayByPlay': #PlayByPlay    
            data = jsonResponse['game']['actions']
        
        
    except Exception as e:
        print(f"Error: {e}")
    return data