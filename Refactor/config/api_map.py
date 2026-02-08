


stats_header = {
    'accept': "*/*",
    'accept-encoding': "gzip, deflate, br, zstd",
    'accept-language': "en-US,en;q=0.9",
    'cache-control': "no-cache",
    'connection': 'keep-alive',
    "pragma": "no-cache",
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'sec-ch-ua-mobile': '?0',
    'host': 'stats.nba.com',
    'origin': 'https://www.nba.com',
    'referer': 'https://www.nba.com/',
    'sec-ch-ua-platform': 'Windows',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true'
}

common_box_params = {    
    'StartPeriod': 1,
    'EndPeriod': 10,
    'StartRange': 1200,
    'EndRange': 24000,
    'RangeType': 0,
    'Season': '2025-26',
    'SeasonType': 'Regular Season',
    'GameID': 0
}


nba_stats_endpoints ={
############################
#region Play-By-Play
#####################
    'playbyplayv2': {
        'url': 'https://stats.nba.com/stats/playbyplayv3',
        'header': stats_header,
        'params': {
            'StartPeriod': 1,
            'EndPeriod': 1,
            'GameID': None,
        }
    },
    'playbyplayv3': {
        'url': 'https://stats.nba.com/stats/playbyplayv3',
        'header': stats_header,
        'params': {
            'StartPeriod': 1,
            'EndPeriod': 1,
            'GameID': None,
        }
    },
#endregion Play-ByPlay

############################
#region Box Score
#####################
    'boxscoretraditionalv2':{
        'url': 'https://stats.nba.com/stats/boxscoretraditionalv2',
        'header': stats_header,
        'params': common_box_params
    },
    'boxscoreadvancedv3':{
        'url': 'https://stats.nba.com/stats/boxscoreadvancedv3',
        'header': stats_header,
        'params': common_box_params
    },
    'boxscoremiscv3':{
        'url': 'https://stats.nba.com/stats/boxscoremiscv3',
        'header': stats_header,
        'params': common_box_params
    },
    'boxscorehustlev2':{
        'url': 'https://stats.nba.com/stats/boxscorehustlev2',
        'header': stats_header,
        'params': {
            'GameID': None
        }
    },
    'boxscoreplayertrackv3':{
        'url': 'https://stats.nba.com/stats/boxscoreplayertrackv3',
        'header': stats_header,
        'params': {
            'GameID': None
        }
    },
#endregion Box Score



############################
#region Standings
#####################
    'leaguestandingsv3':{
        'url': 'https://stats.nba.com/stats/leaguestandingsv3',
        'header': stats_header,
        'params': {
            'SeasonType': 'Regular Season' #'Regular Season' or 'Pre Season', potentially Playoffs...not sure if that works
        }
    },
#endregion Standings


############################
#region Teams
#####################
    'teamindex':{
        'url': 'https://stats.nba.com/stats/teamindex',
        'header': stats_header,
        'params': {
            'LeagueID': '00', #00 = NBA, 10 = WNBA
            'Season': 2025
        }
    },
#endregion Teams


############################
#region Players
#####################
    'playerindex':{
        'url': 'https://stats.nba.com/stats/playerindex',
        'header': stats_header,
        'params': {
            'LeagueID': '00', #00 = NBA, 10 = WNBA
            'Season': 2025,
            'Historical': 1, #0 or 1
        }
    },
#endregion Players


}