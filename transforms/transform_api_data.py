import logging


class Transform:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.logger = logging.getLogger(f'{pipeline.pipeline_name}.transform')
        self.data = pipeline.data if pipeline.data else None
        pass



    def start_transform(self, data_extract):
        self.data_extract = data_extract
        if data_extract['parameters']['MeasureType'] == 'Advanced':
            self.measure_advanced()


    def measure_advanced(self):
        data_extract = self.data_extract
        games_on_date = self.data if self.data else []
        if len(data_extract['resultSets']) > 1:
            self.logger.warning(f'Multiple result sets returned! Only configured to handle one!')
        results = data_extract['resultSets'][0]
        for i, column in enumerate(results['headers']):
            print(f"                '{column}': player[{i}],")
        result_dicts = []
        for player in results['rowSet']:
            matching_game = next((game for game in games_on_date if player[3] in[game['HomeID'], game['AwayID']]), {})
            SeasonID = matching_game.get('SeasonID')
            GameID = matching_game.get('GameID')
            MatchupID = matching_game.get('HomeID') if player[3] == matching_game.get('AwayID') else matching_game.get('AwayID') if player[3] == matching_game.get('HomeID') else 0
            player = {
                'SeasonID': SeasonID,
                'GameID': GameID,
                'TeamID': player[3],
                'MatchupID': MatchupID,
                'PlayerID': player[0],
                'Minutes': player[10],
                'OffRTG': player[12],
                'DefRTG': player[15],
                'NetRTG': player[18],
                'AstPct': player[20],
                'ATR': player[21],
                'AstRtio': player[22],
                'ORebPct': player[23],
                'DRebPct': player[24],
                'RebPct': player[25],
                'TeamTOPct': player[26],
                'EFGPct': player[28],
                'TSPct': player[29],
                'UsagePct': player[30],
                'Pace': player[33],
                'PacePer40': player[34],
                'PIE': player[36],
                'POSS': player[37],
                'FGM': player[38],
                'FGA': player[39],
                'FGPct': player[42],
            }
            result_dicts.append(player)
        bp = 'here'