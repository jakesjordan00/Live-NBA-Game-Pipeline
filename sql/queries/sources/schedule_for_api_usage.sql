with DatesToDo as(
select distinct cast(s.GameTimeEST as date) Date
from Schedule s
left join PlayerBox b on s.SeasonID = b.SeasonID and s.GameID = b.GameID
left join adv.PlayerBox a on b.SeasonID = a.SeasonID and b.GameID = a.GameID and b.TeamID = a.TeamID and b.MatchupID = a.MatchupID and b.PlayerID = a.PlayerID
where b.SeasonID = 2025 and left(b.GameID, 1) not in(1, 3, 6) and b.[Minutes] != '00:00.00'
and a.PlayerID is null
)
select s.*
	 , pb.PlayerID
	 , case when pb.TeamID = s.HomeID then 'Home' else 'Away' end HomeAway
	 , pb.Minutes
	 , pb.MinutesCalculated
from Schedule s
left join PlayerBox pb on s.SeasonID = pb.SeasonID and s.GameID = pb.GameID
where s.SeasonID = 2025 and s.GameType not in('PRE', 'CUP', 'AS') and s.GameTimeEST <= getdate()
and cast(s.GameTimeEST as date) in (select Date from DatesToDo)
order by s.GameTimeEst, s.GameID