from pybaseball import statcast_pitcher_spin
from pybaseball import playerid_lookup

# find Chris Sale's player id (mlbam_key)
playerid_lookup('darvish','yu')

# get all available data within date range
data = statcast_pitcher_spin('2019-07-01', '2019-07-31', player_id = 506433)

# get data for July 15th, 2017
data = statcast_pitcher_spin('2019-05-03', player_id = 543294)
print(data)