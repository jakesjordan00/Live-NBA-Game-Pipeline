if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sqlalchemy.exc

from pipelines import Pipeline
from connectors.sql import SQLConnector, Query
import polars as pl

class ScheduleForAPI(Pipeline):
    def __init__(self, schema: str | None = None, tracking_measure: str | None = None, player_team: str | None = None):
        self.pipeline_name = f'schedule_for_api'
        self.pipeline_tag = 'schedule'
        self.schema = schema
        self.tracking_measure = tracking_measure
        self.player_team = player_team
        super().__init__(self.pipeline_name, self.pipeline_tag, 'SQL')
        self.source = self.destination
        
    def extract(self):
        if self.player_team:
            if self.player_team == 'Team':
                schema_query = self.source.queries.schedule_api_team_check.query.format(schema=self.schema, table=f'{self.player_team}{self.tracking_measure}')
                backfill_query = self.source.queries.schedule_api_team_backfill.query
            elif self.player_team == 'Player':
                schema_query = self.source.queries.schedule_api_player_check.query.format(schema=self.schema, table=f'{self.player_team}{self.tracking_measure}')
                backfill_query = self.source.queries.schedule_api_player_backfill.query
        else:
            schema_query = self.source.queries.schedule_api_player_check.query.format(schema=self.schema, table='PlayerBox')
            backfill_query = self.source.queries.schedule_api_player_backfill.query

        query = Query(name=f'{self.pipeline_name}_{self.schema}', query = schema_query)
        try:
            data_extract = self.source.query_to_dataframe(query=query)
        except sqlalchemy.exc.ProgrammingError as e:
            assert e.orig is not None
            error_msg = e.orig.args[1].replace('[42S02] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]', '')
            # test2 = test(0)
            self.logger.error(error_msg)
            self.logger.warning(f'Running backfill query so we can debug')
            query = Query(name=f'{self.pipeline_name}_{self.schema}', query = backfill_query)
            data_extract = self.source.query_to_dataframe(query=query)
        return {'data_extract': data_extract}
    

    def transform(self, data_extract):
        data_extract = pl.DataFrame(data_extract['data_extract'])
        db_schedule = data_extract.with_columns([
            (pl.col('GameTimeEST').dt.strftime('%m/%d/%Y')).alias('Date')
        ])
        #TODO
        if self.player_team == None or self.player_team != 'Team':
            db_schedule = db_schedule.group_by([
                'SeasonID',
                'GameID',
                'GameTimeEST',
                'Date',
                'HomeID',
                'AwayID'
            ]).agg([
                pl.col('PlayerID').filter(pl.col('HomeAway') == 'Home').alias('home_players'),
                pl.col('PlayerID').filter(pl.col('HomeAway') == 'Away').alias('away_players')  
            ]).sort(['GameTimeEST', 'GameID'])
        distinct_dates = db_schedule.sql('select distinct Date from self').to_series().to_list()

        dates_with_game_data = []

        for date in distinct_dates:
            games = db_schedule.sql(f"select * from self where Date = '{date}'").to_dicts()
            dates_with_game_data.append({
                'date': date,
                'games': games
            })
        data_transformed = dates_with_game_data
        return data_transformed

    def load(self, data_transformed):
        return data_transformed




if __name__ == '__main__':
    pipe = ScheduleForAPI('adv')
    go = pipe.run()
    bp = 'here'