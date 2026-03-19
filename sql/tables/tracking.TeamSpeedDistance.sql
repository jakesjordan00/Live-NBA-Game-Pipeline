if not exists(
select *
from sys.schemas s
where s.name = 'tracking'
)
exec('create schema tracking');
if not exists(
select *
from sys.tables t
inner join sys.schemas s on t.schema_id = s.schema_id
where t.name = 'TeamSpeedDistance' and s.name = 'tracking'
)
begin
create table tracking.TeamSpeedDistance(
SeasonID          int,
GameID            int,
TeamID            int,
MatchupID         int,
DistFeet          int,
DistMiles         int,
DistMilesOff      int,
DistMilesDef      int,
AvgSpeed          int,
AvgSpeedOff       int,
AvgSpeedDef       int,
Primary Key(SeasonID, GameID, TeamID, MatchupID),
Foreign Key (SeasonID, GameID) references Game(SeasonID, GameID),
Foreign Key (SeasonID, TeamID) references Team(SeasonID, TeamID),
Foreign Key (SeasonID, MatchupID) references Team(SeasonID, TeamID),
Foreign Key (SeasonID, GameID, TeamID, MatchupID) references TeamBox(SeasonID, GameID, TeamID, MatchupID))
end