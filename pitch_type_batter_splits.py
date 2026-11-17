from pybaseball import statcast, playerid_lookup, cache, statcast_batter
from pybaseball.playerid_lookup import get_lookup_table
import pandas as pd

cache.enable()
everyone_df = get_lookup_table()
everyone_df = everyone_df[everyone_df['mlb_played_last'] == 2026.0]
print(everyone_df)

player_info_batter = playerid_lookup('harper', 'bryce', fuzzy=True)

atbat_outcomes = statcast_batter('2026-03-26', '2026-12-31', player_info_batter['key_mlbam'][0])
atbat_outcomes.reset_index(drop=True,inplace=True)
atbat_outcomes = atbat_outcomes.dropna(subset=['events'])
#print(data)
atbat_outcomes = pd.merge(atbat_outcomes, everyone_df, left_on='pitcher', right_on='key_mlbam', how='left')
atbat_outcomes = atbat_outcomes.drop(columns=['pitcher'])

ev = atbat_outcomes['events']
atbat_outcomes['H'] = ev.isin(['single','double','triple','home_run']).astype(int)
atbat_outcomes['BB'] = ev.isin(['walk','intent_walk']).astype(int)
atbat_outcomes['HBP'] = ev.isin(['hit_by_pitch']).astype(int)
atbat_outcomes['SF']  = ev.isin(['sac_fly', 'sac_fly_double_play']).astype(int)
non_ab = ev.isin(['walk', 'intent_walk', 'hit_by_pitch', 'sac_fly', 'sac_fly_double_play',
                  'sac_bunt', 'sac_bunt_double_play', 'catcher_interf'])
atbat_outcomes['AB'] = (~non_ab).astype(int)
atbat_outcomes['TB'] = ev.map({'single': 1, 'double': 2, 'triple': 3, 'home_run': 4}).fillna(0).astype(int)


grouped = atbat_outcomes.groupby('pitch_type').agg({'H':'sum','BB':'sum','HBP':'sum','SF':'sum','AB':'sum','TB':'sum'})

#define aggregations for each column
grouped['AVG'] = grouped['H'] / grouped['AB']
grouped['OBP'] = (grouped['H'] + grouped['BB'] + grouped['HBP'])/(grouped['AB'] + grouped['BB'] + grouped['HBP'] + grouped['SF'])
grouped['SLG'] = grouped['TB'] / grouped['AB']
grouped['OPS'] = grouped['OBP'] + grouped['SLG']
print(grouped)