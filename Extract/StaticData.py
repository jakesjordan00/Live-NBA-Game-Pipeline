
import requests



def FetchData(url: str, sender: str):
    try:
        response = requests.get(url)
        jsonResponse = response.json()
    except Exception as e:
        print(f"Error: {e}")
    try:
        if url == 'https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_1.json': #Schedule            
            data = jsonResponse['leagueSchedule']['gameDates']
        elif url == 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json': #Scoreboard            
            data = jsonResponse['scoreboard']['games']
        elif 'boxscore' in url: #BoxScore            
            data = jsonResponse['game']
        elif 'playbyplay' in url: #PlayByPlay            
            data = jsonResponse['game']['actions']

            
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