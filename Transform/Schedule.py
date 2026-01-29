from datetime import datetime, timedelta
import pandas as pd



def TransformSchedule(schedule: list):
    scheduleGames = ParseDates(schedule)
    dfSchedule = pd.DataFrame(data=scheduleGames)
    dfSchedule = ParseSchedule(dfSchedule)
    return dfSchedule





def ParseDates(schedule: list):
    scheduleGames = []
    now = datetime.now()
    today = datetime.now().date()
    for date in schedule:
        gDate = datetime.strptime(date['gameDate'], '%m/%d/%Y %H:%M:%S').date()
        if gDate < datetime(2025, 10, 21).date():  #Start of 2025-26 Season
            continue
        for game in date['games']:
            gameDateTime = datetime.strptime(game['gameDateTimeEst'], '%Y-%m-%dT%H:%M:%SZ')
            if gameDateTime > now:
                continue
            scheduleGames.append(game)
        if gDate > today:
            break
    return scheduleGames


def ParseSchedule(dfSchedule: pd.DataFrame):
    try:
        dfSchedule = dfSchedule[[
        'gameId',
        'gameCode',
        'gameStatus',
        'gameStatusText',
        'gameDateTimeUTC',
        'gameDateTimeEst',
        'ifNecessary',
        'seriesGameNumber',
        'gameLabel',
        'gameSubLabel',
        'seriesText',
        'gameSubtype',
        'isNeutral',
        'homeTeam',
        'awayTeam',        
    ]].rename(columns={
        'gameId': 'GameID',
        'gameCode': 'GameCode',
        'gameStatus': 'GameStatus',
        'gameStatusText': 'GameStatusText',
        'gameDateTimeUTC': 'GameDateTimeUTC',
        'gameDateTimeEst': 'GameDateTimeEST',
        'regulationPeriods': 'RegulationPeriods',
        'ifNecessary': 'IfNecessary',
        'seriesGameNumber': 'SeriesGameNumber',
        'gameLabel': 'GameLabel',
        'gameSubLabel': 'GameSubLabel',
        'seriesText': 'SeriesText',
        'gameSubtype': 'GameSubtype',
        'isNeutral': 'IsNeutral',
        'homeTeam': 'HomeTeam',
        'awayTeam': 'AwayTeam',
    }).astype({
        'GameID': int
    })
        dfSchedule['HomeTeam'] = dfSchedule['HomeTeam'].apply(FormatTeamDicts)
        dfSchedule['AwayTeam'] = dfSchedule['AwayTeam'].apply(FormatTeamDicts)
    except Exception as e:
        print(e)
        test = e
        a = 1

    return dfSchedule


def FormatTeamDicts(team):
    return {
        'TeamID': team['teamId'],
        'TeamName': team['teamName'],
        'TeamCity': team['teamCity'],
        'Wins': team['wins'],
        'Losses': team['losses'],
        'Score': team['score'],
        'Seed': team['seed']
    }
