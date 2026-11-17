import numpy
import pybaseball

from pybaseball import playerid_lookup
from pybaseball import statcast_batter
from pybaseball import statcast_pitcher
from pybaseball import pitching_stats_bref

#ranger suarez stats
# player_id = playerid_lookup('Suarez', 'Ranger')
# print(player_id)

# suarez_bio = statcast_pitcher('2026-01-01', '2026-12-31', player_id = 624133)
# suarez_stats = suarez_bio.groupby('pitch_type').release_speed.agg("mean").sort_values(ascending=False)
# print(suarez_stats)

def pitches_per_bf(start_year=2010, end_year=2019):
    """
    Get the top 10 pitchers in terms of pitches per batter faced for each season from 2008 to 2019.
    Only includes pitchers with at least 15 batters faced.
    """
    for year in range(start_year, end_year + 1):
        pitching_stats = pitching_stats_bref(year)
        pitching_stats = pitching_stats[['Name','Tm','G','BF','Pit']]
        pitching_stats['Pit/BF'] = pitching_stats['Pit'] / pitching_stats['BF']
        pitching_stats = pitching_stats[pitching_stats['BF'] >= 15]
        print(f"Top 10 pitchers in {year} by pitches per batter faced:")
        print(pitching_stats.sort_values(by='Pit/BF', ascending=False).head(10))

pitches_per_bf()


#future questions
#what are the longest at bats ever? what are the outcomes of those at bats? who were the pitchers and batters involved?
#what batters have historically owned certain pitchers? what pitchers have historically owned certain batters? what are the best matchups in baseball history? what are the worst matchups in baseball history?