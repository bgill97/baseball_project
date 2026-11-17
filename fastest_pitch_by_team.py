from pybaseball import statcast
from pybaseball.playerid_lookup import get_lookup_table

all_pitches = statcast('2026-03-26', '2026-09-28')
all_pitches.reset_index(drop=True,inplace=True)

grouped = all_pitches.groupby('pitch_name').agg({'release_speed':['mean','min','max']})
print(grouped)

#group by pitcher instead, and bring in the pitcher name from the player lookup table, then group by pitcher and pitch type to get the average speed of each pitch type for each pitcher. Then sort by average speed to see which pitchers are throwing the fastest pitches.    


# pitches_grouped = all_pitches.groupby('pitch_name').agg({'release_speed':'mean'})

# print(pitches_grouped)