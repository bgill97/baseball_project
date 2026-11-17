#aggregated season long statistics at the player level
from pybaseball import batting_stats_bref

# get all of this season's batting data so far
data = batting_stats_bref()

# retrieve data on the 2009 season
data = batting_stats_bref(2009)
print(data)